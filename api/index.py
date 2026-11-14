"""Vercel serverless entry point for the GridZero FastAPI backend.

On Vercel, set the server-side environment variables in
Project Settings -> Environment Variables:

    GEMINI_API_KEY = <your Gemini API key>   (never commit it, never expose it to the frontend)
    GEMINI_MODEL   = gemini-3.8-flash        (optional)

Then redeploy — environment variables only apply to new deployments.
The key is read by backend/main.py from os.environ at request time.

Why the middleware below exists: Vercel `rewrites` forward the DESTINATION
path to the function, not the path the browser asked for. With a catch-all
rewrite to this file, FastAPI receives every request as `/api/index.py`
and 404s every route. vercel.json therefore carries the original path in
a `__gz_path` query parameter, and RestoreOriginalPathMiddleware puts it
back into the ASGI scope before FastAPI routes the request. It also strips
a `/api/index(.py)` prefix and honours Vercel's original-path headers as
fallbacks. Locally (uvicorn) none of this triggers.
"""

import os
import sys
from urllib.parse import parse_qsl, urlencode

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "backend"))

from main import app  # noqa: E402


class RestoreOriginalPathMiddleware:
    """Pure ASGI middleware: restore the pre-rewrite request path."""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope.get("type") == "http":
            path = scope.get("path", "") or "/"
            query_string = scope.get("query_string", b"").decode("utf-8", "ignore")
            params = parse_qsl(query_string, keep_blank_values=True)
            carried = [v for k, v in params if k == "__gz_path"]

            if carried:
                restored = carried[0]
                if not restored.startswith("/"):
                    restored = "/" + restored
                scope["path"] = restored
                remaining = [(k, v) for k, v in params if k != "__gz_path"]
                scope["query_string"] = urlencode(remaining).encode()
            else:
                stripped = False
                for prefix in ("/api/index.py", "/api/index"):
                    if path == prefix:
                        scope["path"] = "/"
                        stripped = True
                        break
                    if path.startswith(prefix + "/"):
                        scope["path"] = path[len(prefix):]
                        stripped = True
                        break
                if not stripped and path in ("/api/index.py", "/api/index"):
                    headers = {
                        k.decode("utf-8", "ignore").lower(): v.decode("utf-8", "ignore")
                        for k, v in scope.get("headers", [])
                    }
                    original = (
                        headers.get("x-original-pathname")
                        or headers.get("x-vercel-original-pathname")
                        or headers.get("x-matched-path")
                    )
                    if original:
                        scope["path"] = original
            scope["raw_path"] = scope["path"].encode()
        await self.app(scope, receive, send)


app.add_middleware(RestoreOriginalPathMiddleware)
