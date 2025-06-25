# 🎙️ Voice Journal – Daily Audio Diary App (Python Desktop GUI)

A simple yet powerful voice journaling desktop application built using Python. This offline tool allows you to record your thoughts, add titles and tags, and revisit your past entries through audio playback—all saved locally, organized by date.

## 🧰 Features

- 🎤 Record voice entries with one click  
- 📝 Add custom titles and optional tags/notes  
- 🗂 Auto-organized by date and time  
- 🔁 Playback any past entry directly from the app  
- 📁 Stores entries as `.wav` + `.txt` files (offline, no cloud needed)  
- 🔄 Refresh to load new entries anytime  

## 📦 Tech Stack

| Library        | Purpose                     |
|----------------|-----------------------------|
| `Tkinter`      | GUI Interface                |
| `sounddevice`  | Real-time microphone recording |
| `numpy` + `scipy` | Handling & saving audio data |
| `pygame`       | Playback of audio recordings |
| `datetime`     | Timestamping and folder organization |
| `os`           | File I/O and folder structure |
