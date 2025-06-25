import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import pygame
import os
from datetime import datetime

class VoiceJournalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎙️ Voice Journal - Daily Audio Diary")
        self.root.geometry("600x500")

        self.fs = 44100
        self.recording = False
        self.audio_data = []
        self.journal_dir = "voice_journal"

        os.makedirs(self.journal_dir, exist_ok=True)
        pygame.mixer.init()

        # Title label
        tk.Label(root, text="📔 Voice Journal", font=("Arial", 20, "bold")).pack(pady=10)

        # Buttons
        self.record_button = tk.Button(root, text="Start Recording", command=self.start_recording)
        self.record_button.pack(pady=5)

        self.stop_button = tk.Button(root, text="Stop Recording", state=tk.DISABLED, command=self.stop_recording)
        self.stop_button.pack(pady=5)

        self.play_button = tk.Button(root, text="Play Selected Entry", command=self.play_entry)
        self.play_button.pack(pady=5)

        self.entry_listbox = tk.Listbox(root, width=80)
        self.entry_listbox.pack(pady=10)

        self.refresh_button = tk.Button(root, text="🔄 Refresh Entry List", command=self.load_entries)
        self.refresh_button.pack(pady=5)

        self.load_entries()

    def start_recording(self):
        self.recording = True
        self.audio_data = []
        self.record_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.stream = sd.InputStream(samplerate=self.fs, channels=1, callback=self.audio_callback)
        self.stream.start()

    def audio_callback(self, indata, frames, time_info, status):
        if self.recording:
            self.audio_data.append(indata.copy())

    def stop_recording(self):
        self.recording = False
        self.record_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.stream.stop()

        audio_array = np.concatenate(self.audio_data, axis=0)
        now = datetime.now()
        date_folder = now.strftime("%Y-%m-%d")
        time_stamp = now.strftime("%H-%M")

        # Ask for title
        title = simpledialog.askstring("Entry Title", "Enter a title for this entry:")
        if not title:
            title = "Untitled"

        entry_folder = os.path.join(self.journal_dir, date_folder)
        os.makedirs(entry_folder, exist_ok=True)

        base_filename = f"{time_stamp}_{title.replace(' ', '_')}"
        wav_path = os.path.join(entry_folder, base_filename + ".wav")
        txt_path = os.path.join(entry_folder, base_filename + ".txt")

        write(wav_path, self.fs, audio_array)

        # Ask for notes/tags
        tags = simpledialog.askstring("Tags/Notes", "Enter any tags or notes (optional):")
        if tags:
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(tags)

        messagebox.showinfo("Saved", f"Entry saved as:\n{wav_path}")
        self.load_entries()

    def load_entries(self):
        self.entry_listbox.delete(0, tk.END)
        for root, dirs, files in os.walk(self.journal_dir):
            for file in sorted(files):
                if file.endswith(".wav"):
                    full_path = os.path.join(root, file)
                    display_name = os.path.relpath(full_path, self.journal_dir)
                    self.entry_listbox.insert(tk.END, display_name)

    def play_entry(self):
        selected = self.entry_listbox.curselection()
        if not selected:
            messagebox.showwarning("Select Entry", "Please select an entry to play.")
            return
        filename = self.entry_listbox.get(selected[0])
        full_path = os.path.join(self.journal_dir, filename)
        try:
            pygame.mixer.music.load(full_path)
            pygame.mixer.music.play()
        except Exception as e:
            messagebox.showerror("Playback Error", str(e))

# Launch the app
if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceJournalApp(root)
    root.mainloop()
