import tkinter as tk
from tkvideo import tkvideo
import pygame

class TheEnd:
    def __init__(self):
        # Initialize Pygame for audio playback
        pygame.init()
        pygame.mixer.init()

        # Load the separated audio file as a Sound object
        audio_path = "club.mp3"  # Replace with the actual path or name of your audio file
        self.sound = pygame.mixer.Sound(audio_path)

        # Set up the Tkinter window for video playback
        self.root = tk.Tk()
        self.root.title("Video Player")

        self.lbl_video = tk.Label(self.root)
        self.lbl_video.pack()

        self.player = tkvideo("goodbye.mp4",
                              self.lbl_video,
                              loop=1,
                              size=(1400, 788))

        self.playing = True  # Flag to track playing state

    def play_video(self):
        # Play the video
        self.player.play()

        # Play the associated audio
        self.sound.play()

        # Schedule the exit after 27 seconds
        self.root.after(52000, self.exit_after_34_seconds)

        # Check for events to handle window closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.root.mainloop()

    def exit_after_34_seconds(self):
        # Stop playing the video and sound
        self.player.stop()
        pygame.mixer.stop()

        # Set the playing flag to False
        self.playing = False

        # Destroy the Tkinter window
        self.root.destroy()

    def on_close(self):
        # Handle window closing event
        self.exit_after_34_seconds()

    def is_playing(self):
        # Check whether the video is still playing
        return self.playing
