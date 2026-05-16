"""Chat Panel - Main conversation interface with JARVIS."""

import threading
from datetime import datetime
import customtkinter as ctk
from gui.theme import (
    BG_DARK, BG_PANEL, BG_INPUT, BG_CHAT_BUBBLE_USER, BG_CHAT_BUBBLE_JARVIS,
    BG_BUTTON, BG_BUTTON_HOVER, BG_HEADER,
    ACCENT_BLUE, ACCENT_CYAN, ACCENT_GREEN,
    TEXT_PRIMARY, TEXT_SECONDARY, TEXT_DIM, TEXT_JARVIS,
    BORDER_COLOR, BORDER_GLOW,
    FONT_HEADER, FONT_BODY, FONT_SMALL, FONT_TINY, FONT_CHAT, FONT_INPUT,
    FONT_BUTTON, CORNER_RADIUS, INPUT_HEIGHT,
)
from core.gemini_engine import GeminiEngine
from core.voice import VoiceEngine


class ChatPanel(ctk.CTkFrame):
    """Main chat interface for interacting with JARVIS."""

    def __init__(self, parent, gemini_engine: GeminiEngine, voice_engine: VoiceEngine):
        super().__init__(parent, fg_color=BG_DARK, corner_radius=0)
        self.gemini = gemini_engine
        self.voice = voice_engine
        self.is_processing = False
        self._build_ui()
        self._show_welcome()

    def _build_ui(self) -> None:
        self._build_header()
        self._build_chat_area()
        self._build_input_area()

    def _build_header(self) -> None:
        header = ctk.CTkFrame(self, fg_color=BG_HEADER, height=50, corner_radius=0)
        header.pack(fill="x")
        header.pack_propagate(False)

        left = ctk.CTkFrame(header, fg_color="transparent")
        left.pack(side="left", padx=20)

        ctk.CTkLabel(
            left,
            text="JARVIS TERMINAL",
            font=FONT_HEADER,
            text_color=ACCENT_CYAN,
        ).pack(side="left")

        self.status_dot = ctk.CTkLabel(
            left,
            text="  ●",
            font=FONT_SMALL,
            text_color=ACCENT_GREEN,
        )
        self.status_dot.pack(side="left")

        right = ctk.CTkFrame(header, fg_color="transparent")
        right.pack(side="right", padx=20)

        self.voice_btn = ctk.CTkButton(
            right,
            text="🔊 Ses: Açık",
            font=FONT_SMALL,
            fg_color="transparent",
            hover_color=BG_BUTTON,
            width=100,
            height=30,
            command=self._toggle_voice,
        )
        self.voice_btn.pack(side="right", padx=5)

        self.clear_btn = ctk.CTkButton(
            right,
            text="🗑 Temizle",
            font=FONT_SMALL,
            fg_color="transparent",
            hover_color=BG_BUTTON,
            width=90,
            height=30,
            command=self._clear_chat,
        )
        self.clear_btn.pack(side="right", padx=5)

    def _build_chat_area(self) -> None:
        self.chat_container = ctk.CTkScrollableFrame(
            self,
            fg_color=BG_DARK,
            corner_radius=0,
            scrollbar_button_color=BORDER_COLOR,
            scrollbar_button_hover_color=ACCENT_BLUE,
        )
        self.chat_container.pack(fill="both", expand=True, padx=10, pady=5)

    def _build_input_area(self) -> None:
        input_frame = ctk.CTkFrame(
            self, fg_color=BG_PANEL, height=70, corner_radius=0,
            border_width=1, border_color=BORDER_COLOR,
        )
        input_frame.pack(fill="x", side="bottom")
        input_frame.pack_propagate(False)

        inner = ctk.CTkFrame(input_frame, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=15, pady=12)

        self.input_entry = ctk.CTkEntry(
            inner,
            placeholder_text="JARVIS'e bir komut yazın...",
            font=FONT_INPUT,
            fg_color=BG_INPUT,
            border_color=BORDER_COLOR,
            text_color=TEXT_PRIMARY,
            placeholder_text_color=TEXT_DIM,
            height=INPUT_HEIGHT,
            corner_radius=CORNER_RADIUS,
        )
        self.input_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.input_entry.bind("<Return>", self._on_send)

        self.send_btn = ctk.CTkButton(
            inner,
            text="Gönder ▸",
            font=FONT_BUTTON,
            fg_color=ACCENT_BLUE,
            hover_color=BG_BUTTON_HOVER,
            text_color="#ffffff",
            width=100,
            height=INPUT_HEIGHT,
            corner_radius=CORNER_RADIUS,
            command=self._on_send,
        )
        self.send_btn.pack(side="right")

    def _show_welcome(self) -> None:
        welcome_lines = [
            "J.A.R.V.I.S. Sistemi başlatılıyor...",
            "Tüm sistemler aktif.",
            "",
            "Merhaba Efendim, ben JARVIS.",
            "Size nasıl yardımcı olabilirim?",
        ]
        self._add_jarvis_message("\n".join(welcome_lines))

    def _on_send(self, event=None) -> None:
        message = self.input_entry.get().strip()
        if not message or self.is_processing:
            return

        self.input_entry.delete(0, "end")
        self._add_user_message(message)
        self._set_processing(True)

        thread = threading.Thread(
            target=self._process_message, args=(message,), daemon=True
        )
        thread.start()

    def _process_message(self, message: str) -> None:
        response = self.gemini.send_message(message)
        self.after(0, self._handle_response, response)

    def _handle_response(self, response: str) -> None:
        self._add_jarvis_message(response)
        self._set_processing(False)
        if self.voice.is_enabled:
            self.voice.speak(response)

    def _add_user_message(self, text: str) -> None:
        self._add_bubble(text, is_user=True)

    def _add_jarvis_message(self, text: str) -> None:
        self._add_bubble(text, is_user=False)

    def _add_bubble(self, text: str, is_user: bool) -> None:
        outer = ctk.CTkFrame(self.chat_container, fg_color="transparent")
        outer.pack(fill="x", pady=4, padx=5)

        anchor = "e" if is_user else "w"
        bg_color = BG_CHAT_BUBBLE_USER if is_user else BG_CHAT_BUBBLE_JARVIS
        text_color = TEXT_PRIMARY if is_user else TEXT_JARVIS
        sender = "Siz" if is_user else "JARVIS"
        sender_color = ACCENT_BLUE if is_user else ACCENT_CYAN

        bubble = ctk.CTkFrame(
            outer, fg_color=bg_color, corner_radius=12,
            border_width=1,
            border_color=BORDER_COLOR if is_user else "#0a2a3f",
        )
        bubble.pack(anchor=anchor, padx=10)

        header = ctk.CTkFrame(bubble, fg_color="transparent")
        header.pack(fill="x", padx=12, pady=(8, 2))

        ctk.CTkLabel(
            header, text=f"◆ {sender}",
            font=("Consolas", 11, "bold"),
            text_color=sender_color,
        ).pack(side="left")

        timestamp = datetime.now().strftime("%H:%M")
        ctk.CTkLabel(
            header, text=timestamp,
            font=FONT_TINY, text_color=TEXT_DIM,
        ).pack(side="right")

        msg_label = ctk.CTkLabel(
            bubble,
            text=text,
            font=FONT_CHAT,
            text_color=text_color,
            wraplength=500,
            justify="left",
            anchor="w",
        )
        msg_label.pack(fill="x", padx=12, pady=(2, 10))

        self.chat_container.after(100, self._scroll_to_bottom)

    def _scroll_to_bottom(self) -> None:
        self.chat_container._parent_canvas.yview_moveto(1.0)

    def _set_processing(self, processing: bool) -> None:
        self.is_processing = processing
        if processing:
            self.send_btn.configure(text="⟳ ...", state="disabled")
            self.status_dot.configure(text="  ◌", text_color=ACCENT_BLUE)
        else:
            self.send_btn.configure(text="Gönder ▸", state="normal")
            self.status_dot.configure(text="  ●", text_color=ACCENT_GREEN)

    def _toggle_voice(self) -> None:
        enabled = self.voice.toggle()
        if enabled:
            self.voice_btn.configure(text="🔊 Ses: Açık")
        else:
            self.voice_btn.configure(text="🔇 Ses: Kapalı")

    def _clear_chat(self) -> None:
        for widget in self.chat_container.winfo_children():
            widget.destroy()
        self.gemini.reset_chat()
        self.after(100, self._show_welcome)

    def send_command(self, command: str) -> None:
        self.input_entry.delete(0, "end")
        self.input_entry.insert(0, command)
        self._on_send()
