"""Sidebar - System monitoring panel with JARVIS styling."""

import customtkinter as ctk
from gui.theme import (
    BG_SIDEBAR, BG_PANEL, ACCENT_BLUE, ACCENT_CYAN, ACCENT_GREEN,
    ACCENT_RED, ACCENT_ORANGE, ACCENT_YELLOW, TEXT_PRIMARY, TEXT_SECONDARY,
    TEXT_DIM, BORDER_COLOR, FONT_HEADER, FONT_BODY, FONT_SMALL, FONT_TINY,
    SIDEBAR_WIDTH, CORNER_RADIUS,
)
from core.system_monitor import SystemMonitor


class Sidebar(ctk.CTkFrame):
    """System information sidebar with real-time monitoring."""

    def __init__(self, parent, gemini_status: str = "OFFLINE"):
        super().__init__(
            parent,
            width=SIDEBAR_WIDTH,
            fg_color=BG_SIDEBAR,
            corner_radius=0,
            border_width=1,
            border_color=BORDER_COLOR,
        )
        self.pack_propagate(False)
        self.monitor = SystemMonitor()
        self.gemini_status = gemini_status
        self._build_ui()
        self._update_stats()

    def _build_ui(self) -> None:
        self._build_logo_section()
        self._build_status_section()
        self._build_system_section()
        self._build_datetime_section()
        self._build_quick_commands()

    def _build_logo_section(self) -> None:
        logo_frame = ctk.CTkFrame(self, fg_color="transparent", height=80)
        logo_frame.pack(fill="x", padx=15, pady=(15, 5))
        logo_frame.pack_propagate(False)

        ctk.CTkLabel(
            logo_frame,
            text="◆ J.A.R.V.I.S.",
            font=("Consolas", 20, "bold"),
            text_color=ACCENT_CYAN,
        ).pack(anchor="w")

        ctk.CTkLabel(
            logo_frame,
            text="Just A Rather Very\nIntelligent System",
            font=FONT_TINY,
            text_color=TEXT_DIM,
            justify="left",
        ).pack(anchor="w", pady=(2, 0))

    def _build_status_section(self) -> None:
        section = self._create_section("SİSTEM DURUMU")

        self.status_frame = ctk.CTkFrame(section, fg_color="transparent")
        self.status_frame.pack(fill="x")

        self.gemini_label = self._create_status_row(
            self.status_frame, "Gemini AI", self.gemini_status
        )
        self._create_status_row(self.status_frame, "Ses Motoru", "ONLINE")

    def _build_system_section(self) -> None:
        section = self._create_section("PERFORMANS")

        self.cpu_bar = self._create_progress_row(section, "CPU")
        self.mem_bar = self._create_progress_row(section, "RAM")
        self.disk_bar = self._create_progress_row(section, "DISK")

        self.cpu_label = self.cpu_bar[1]
        self.mem_label = self.mem_bar[1]
        self.disk_label = self.disk_bar[1]
        self.cpu_progress = self.cpu_bar[2]
        self.mem_progress = self.mem_bar[2]
        self.disk_progress = self.disk_bar[2]

    def _build_datetime_section(self) -> None:
        section = self._create_section("TARİH & SAAT")

        self.time_label = ctk.CTkLabel(
            section, text="--:--:--",
            font=("Consolas", 28, "bold"),
            text_color=ACCENT_CYAN,
        )
        self.time_label.pack(anchor="w")

        self.date_label = ctk.CTkLabel(
            section, text="---",
            font=FONT_SMALL,
            text_color=TEXT_SECONDARY,
        )
        self.date_label.pack(anchor="w")

        self.uptime_label = ctk.CTkLabel(
            section, text="Uptime: ---",
            font=FONT_TINY,
            text_color=TEXT_DIM,
        )
        self.uptime_label.pack(anchor="w", pady=(4, 0))

    def _build_quick_commands(self) -> None:
        section = self._create_section("HIZLI KOMUTLAR")

        commands = [
            ("📊 Sistem Raporu", "sistem raporu ver"),
            ("🌐 IP Bilgisi", "IP adresim nedir"),
            ("💡 Öneri", "bana günlük bir öneri ver"),
        ]

        self.command_callbacks = {}
        for label_text, cmd in commands:
            btn = ctk.CTkButton(
                section,
                text=label_text,
                font=FONT_SMALL,
                fg_color=BG_PANEL,
                hover_color="#1a2744",
                border_width=1,
                border_color=BORDER_COLOR,
                corner_radius=6,
                height=32,
                anchor="w",
            )
            btn.pack(fill="x", pady=2)
            self.command_callbacks[btn] = cmd

    def set_command_callback(self, callback) -> None:
        for btn, cmd in self.command_callbacks.items():
            btn.configure(command=lambda c=cmd: callback(c))

    def _create_section(self, title: str) -> ctk.CTkFrame:
        separator = ctk.CTkFrame(self, fg_color=BORDER_COLOR, height=1)
        separator.pack(fill="x", padx=15, pady=(10, 0))

        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(fill="x", padx=15, pady=(8, 0))

        ctk.CTkLabel(
            frame,
            text=f"▸ {title}",
            font=FONT_SMALL,
            text_color=TEXT_DIM,
        ).pack(anchor="w", pady=(0, 6))

        return frame

    def _create_status_row(self, parent, name: str, status: str) -> ctk.CTkLabel:
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", pady=1)

        ctk.CTkLabel(
            row, text=name, font=FONT_SMALL, text_color=TEXT_SECONDARY,
        ).pack(side="left")

        color = ACCENT_GREEN if status == "ONLINE" else ACCENT_RED
        label = ctk.CTkLabel(
            row, text=f"● {status}", font=FONT_SMALL, text_color=color,
        )
        label.pack(side="right")
        return label

    def _create_progress_row(self, parent, name: str) -> tuple:
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", pady=3)

        ctk.CTkLabel(
            row, text=name, font=FONT_SMALL, text_color=TEXT_SECONDARY, width=40,
        ).pack(side="left")

        pct_label = ctk.CTkLabel(
            row, text="0%", font=FONT_SMALL, text_color=TEXT_PRIMARY, width=45,
        )
        pct_label.pack(side="right")

        progress = ctk.CTkProgressBar(
            row, height=8, corner_radius=4,
            fg_color=BG_PANEL, progress_color=ACCENT_BLUE,
        )
        progress.pack(side="right", fill="x", expand=True, padx=(5, 5))
        progress.set(0)

        return (row, pct_label, progress)

    def update_gemini_status(self, status: str) -> None:
        self.gemini_status = status
        color = ACCENT_GREEN if status == "ONLINE" else ACCENT_RED
        self.gemini_label.configure(text=f"● {status}", text_color=color)

    def _update_stats(self) -> None:
        try:
            cpu = self.monitor.get_cpu_percent()
            mem = self.monitor.get_memory_info()
            disk = self.monitor.get_disk_info()
            dt = self.monitor.get_datetime_info()
            uptime = self.monitor.get_uptime()

            self.cpu_progress.set(cpu / 100)
            self.cpu_label.configure(text=f"{cpu:.0f}%")
            self._color_progress(self.cpu_progress, cpu)

            self.mem_progress.set(mem["percent"] / 100)
            self.mem_label.configure(text=f"{mem['percent']:.0f}%")
            self._color_progress(self.mem_progress, mem["percent"])

            self.disk_progress.set(disk["percent"] / 100)
            self.disk_label.configure(text=f"{disk['percent']:.0f}%")
            self._color_progress(self.disk_progress, disk["percent"])

            self.time_label.configure(text=dt["time"])
            self.date_label.configure(text=f"{dt['day']}, {dt['date']}")
            self.uptime_label.configure(text=f"Uptime: {uptime}")
        except Exception:
            pass

        self.after(2000, self._update_stats)

    def _color_progress(self, bar: ctk.CTkProgressBar, value: float) -> None:
        if value > 90:
            bar.configure(progress_color=ACCENT_RED)
        elif value > 70:
            bar.configure(progress_color=ACCENT_ORANGE)
        elif value > 50:
            bar.configure(progress_color=ACCENT_YELLOW)
        else:
            bar.configure(progress_color=ACCENT_BLUE)
