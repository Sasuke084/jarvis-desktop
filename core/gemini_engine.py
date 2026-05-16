"""Gemini AI Engine - Handles communication with Google Gemini API."""

import os
from google import genai
from google.genai import types


JARVIS_SYSTEM_PROMPT = """Sen J.A.R.V.I.S. (Just A Rather Very Intelligent System) adlı gelişmiş bir yapay zekâ asistanısın.
Tony Stark tarafından geliştirildin. Aşağıdaki özelliklere sahipsin:

1. Kibar, zeki ve profesyonel bir şekilde konuşursun.
2. Kullanıcıya "Efendim" veya ismiyle hitap edersin.
3. Kısa, öz ve bilgilendirici cevaplar verirsin.
4. Teknik konularda uzman gibi konuşabilirsin.
5. Mizah anlayışın vardır ama her zaman saygılı kalırsın.
6. Türkçe ve İngilizce konuşabilirsin - kullanıcı hangi dilde yazarsa o dilde cevap ver.
7. Sistem durumu, hava durumu, tarih/saat gibi sorulara da cevap verebilirsin.
8. Gerektiğinde uyarılar ve öneriler sunarsın.

Cevaplarına bazen "Efendim, " diye başla ama her seferinde değil - doğal ol.
Çok uzun cevaplar verme, özet ve net ol."""


class GeminiEngine:
    """Manages Gemini AI model interactions."""

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.environ.get("GOOGLE_GEMINI_API_KEY", "")
        self.client = None
        self.chat = None
        self.is_configured = False
        self._configure()

    def _configure(self) -> None:
        if not self.api_key:
            return
        try:
            self.client = genai.Client(api_key=self.api_key)
            self.chat = self.client.chats.create(
                model="gemini-2.0-flash",
                config=types.GenerateContentConfig(
                    system_instruction=JARVIS_SYSTEM_PROMPT,
                ),
            )
            self.is_configured = True
        except Exception as e:
            print(f"Gemini configuration error: {e}")
            self.is_configured = False

    def send_message(self, message: str) -> str:
        if not self.is_configured or not self.chat:
            return "⚠ Gemini API bağlantısı kurulamadı. Lütfen API anahtarınızı kontrol edin."
        try:
            response = self.chat.send_message(message)
            return response.text
        except Exception as e:
            return f"⚠ Hata oluştu: {str(e)}"

    def reset_chat(self) -> None:
        if self.client:
            try:
                self.chat = self.client.chats.create(
                    model="gemini-2.0-flash",
                    config=types.GenerateContentConfig(
                        system_instruction=JARVIS_SYSTEM_PROMPT,
                    ),
                )
            except Exception as e:
                print(f"Chat reset error: {e}")

    def get_status(self) -> str:
        if self.is_configured:
            return "ONLINE"
        return "OFFLINE"
