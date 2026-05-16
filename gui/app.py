"""Main Application Window - JARVIS Desktop Interface."""

import customtkinter as ctk
from gui.theme import BG_DARK, ACCENT_CYAN
from gui.sidebar import Sidebar
from gui.chat_panel import ChatPanel
from core.gemini_engine import GeminiEngine
from core.voice import VoiceEngine


class JarvisApp(ctk.CTk):
    """Main JARVIS desktop application window."""

    def __init__(self, api_key: str = ""):
        super().__init__()

        self.title("J.A.R.V.I.S. - AI Assistant")
        self.geometry("1200x750")
        self.minsize(900, 600)
        self.configure(fg_color=BG_DARK)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.gemini = GeminiEngine(api_key=api_key)
        self.voice = VoiceEngine()

        self._build_ui()

    def _build_ui(self) -> None:
        main_container = ctk.CTkFrame(self, fg_color=BG_DARK, corner_radius=0)
        main_container.pack(fill="both", expand=True)

        self.sidebar = Sidebar(
            main_container,
            gemini_status=self.gemini.get_status(),
        )
        self.sidebar.pack(side="left", fill="y")

        self.chat_panel = ChatPanel(
            main_container,
            gemini_engine=self.gemini,
            voice_engine=self.voice,
        )
        self.chat_panel.pack(side="left", fill="both", expand=True)

        self.sidebar.set_command_callback(self.chat_panel.send_command)

    def run(self) -> None:
        self.mainloop()
