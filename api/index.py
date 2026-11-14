"""Vercel serverless entry point for the GridZero FastAPI backend.

On Vercel, set the server-side environment variable in
Project Settings -> Environment Variables:

    GEMINI_API_KEY = <your Gemini API key>   (never commit it, never expose it to the frontend)
    GEMINI_MODEL   = gemini-2.5-flash        (optional)

Then redeploy — environment variables only apply to new deployments.
The key is read by backend/main.py from os.environ at request time.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "backend"))

from main import app  # noqa: E402,F401  (Vercel's Python runtime serves the ASGI `app`)
