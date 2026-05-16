"""Utility helpers for JARVIS application."""

import os
import platform
import subprocess


def get_local_ip() -> str:
    """Get the local IP address."""
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "N/A"


def open_url(url: str) -> None:
    """Open a URL in the default browser."""
    try:
        if platform.system() == "Linux":
            subprocess.Popen(["xdg-open", url])
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", url])
        elif platform.system() == "Windows":
            os.startfile(url)
    except Exception:
        pass


def format_bytes(bytes_val: int) -> str:
    """Format bytes to human-readable string."""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if bytes_val < 1024:
            return f"{bytes_val:.1f} {unit}"
        bytes_val /= 1024
    return f"{bytes_val:.1f} PB"
