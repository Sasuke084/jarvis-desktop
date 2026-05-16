"""Voice Engine - Text-to-speech capabilities for JARVIS."""

import threading
import pyttsx3


class VoiceEngine:
    """Handles text-to-speech output."""

    def __init__(self):
        self._engine = None
        self._is_speaking = False
        self._enabled = True
        self._init_engine()

    def _init_engine(self) -> None:
        try:
            self._engine = pyttsx3.init()
            self._engine.setProperty("rate", 175)
            self._engine.setProperty("volume", 0.9)
            voices = self._engine.getProperty("voices")
            turkish_voice = None
            english_voice = None
            for voice in voices:
                if voice.id == "trk/tr" or "turkish" in voice.name.lower():
                    turkish_voice = voice
                elif english_voice is None and (
                    "en-us" in voice.id.lower() or "en-gb" in voice.id.lower()
                ):
                    english_voice = voice
            if turkish_voice:
                self._engine.setProperty("voice", turkish_voice.id)
            elif english_voice:
                self._engine.setProperty("voice", english_voice.id)
        except Exception as e:
            print(f"Voice engine init error: {e}")
            self._engine = None

    def speak(self, text: str) -> None:
        if not self._enabled or not self._engine or self._is_speaking:
            return
        thread = threading.Thread(target=self._speak_thread, args=(text,), daemon=True)
        thread.start()

    def _speak_thread(self, text: str) -> None:
        try:
            self._is_speaking = True
            self._engine.say(text)
            self._engine.runAndWait()
        except Exception as e:
            print(f"Voice error: {e}")
        finally:
            self._is_speaking = False

    def stop(self) -> None:
        if self._engine and self._is_speaking:
            try:
                self._engine.stop()
            except Exception:
                pass
        self._is_speaking = False

    def toggle(self) -> bool:
        self._enabled = not self._enabled
        return self._enabled

    @property
    def is_enabled(self) -> bool:
        return self._enabled

    @property
    def is_available(self) -> bool:
        return self._engine is not None
