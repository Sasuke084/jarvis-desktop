#!/usr/bin/env python3
"""
J.A.R.V.I.S. - Just A Rather Very Intelligent System
=====================================================
A desktop AI assistant powered by Google Gemini.

Usage:
    python main.py
    python main.py --api-key YOUR_API_KEY

The API key can also be set via the GOOGLE_GEMINI_API_KEY environment variable.
"""

import argparse
import os
import sys


def main():
    parser = argparse.ArgumentParser(
        description="J.A.R.V.I.S. - AI Desktop Assistant powered by Google Gemini"
    )
    parser.add_argument(
        "--api-key",
        type=str,
        default="",
        help="Google Gemini API key (or set GOOGLE_GEMINI_API_KEY env var)",
    )
    args = parser.parse_args()

    api_key = args.api_key or os.environ.get("GOOGLE_GEMINI_API_KEY", "")

    if not api_key:
        print("=" * 60)
        print("  J.A.R.V.I.S. - API Key Required")
        print("=" * 60)
        print()
        print("  Please provide your Google Gemini API key:")
        print()
        print("  Option 1: Set environment variable")
        print("    export GOOGLE_GEMINI_API_KEY=your_key_here")
        print()
        print("  Option 2: Pass as argument")
        print("    python main.py --api-key your_key_here")
        print()
        print("  Get your API key at:")
        print("    https://aistudio.google.com/app/apikey")
        print("=" * 60)
        sys.exit(1)

    from gui.app import JarvisApp

    app = JarvisApp(api_key=api_key)
    app.run()


if __name__ == "__main__":
    main()
