# J.A.R.V.I.S. - Just A Rather Very Intelligent System

<p align="center">
  <strong>A desktop AI assistant inspired by Tony Stark's JARVIS, powered by Google Gemini.</strong>
</p>

---

## Features

- **AI Chat Interface** — Natural language conversation powered by Google Gemini 2.0 Flash
- **Futuristic UI** — Dark themed, JARVIS-inspired desktop interface built with CustomTkinter
- **System Monitoring** — Real-time CPU, RAM, disk usage monitoring
- **Text-to-Speech** — JARVIS can speak responses aloud
- **Quick Commands** — One-click system reports, IP info, and suggestions
- **Bilingual** — Supports Turkish and English conversation
- **Chat History** — Maintains conversation context within a session

## Screenshots

The application features a dark, futuristic interface with:
- Left sidebar: System status, performance metrics, date/time, and quick commands
- Main panel: Chat terminal with user and JARVIS message bubbles
- Header: Voice toggle and chat clear controls

## Requirements

- Python 3.10+
- Google Gemini API key ([Get one here](https://aistudio.google.com/app/apikey))

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Sasuke084/jarvis-desktop.git
cd jarvis-desktop
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set your API key:
```bash
export GOOGLE_GEMINI_API_KEY=your_api_key_here
```

## Usage

```bash
python main.py
```

Or pass the API key directly:
```bash
python main.py --api-key your_api_key_here
```

## Project Structure

```
jarvis-desktop/
├── main.py                 # Entry point
├── requirements.txt        # Python dependencies
├── README.md               # Documentation
├── core/
│   ├── gemini_engine.py    # Google Gemini AI integration
│   ├── system_monitor.py   # System resource monitoring
│   └── voice.py            # Text-to-speech engine
├── gui/
│   ├── app.py              # Main application window
│   ├── chat_panel.py       # Chat interface
│   ├── sidebar.py          # System info sidebar
│   └── theme.py            # JARVIS theme colors & fonts
└── utils/
    └── helpers.py           # Utility functions
```

## Tech Stack

- **GUI**: CustomTkinter (Modern themed Tkinter)
- **AI**: Google Gemini 2.0 Flash
- **TTS**: pyttsx3
- **System Monitoring**: psutil
- **Language**: Python 3.12

## License

MIT License
