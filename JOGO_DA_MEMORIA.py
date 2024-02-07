import tkinter as tk
import tkinter.messagebox
import random
import time

try:
    import pygame
except ImportError:
    import subprocess

    subprocess.call(['pip', 'install', 'pygame'])
    import pygame


class Genius:
    def __init__(self, master):
        self.master = master
        self.colors = ['red', 'green', 'blue', 'yellow']
        self.sounds = [pygame.mixer.Sound(color + '.mp3') for color in self.colors]
        self.buttons = [tk.Button(master, bg=color, width=18, height=10) for color in self.colors]
        for i, button in enumerate(self.buttons):
            button.grid(row=i //  2, column=i %  2)
        self.sequence = []
        self.user_sequence = []

    def start_game(self):
        self.sequence.append(random.choice(list(enumerate(self.buttons))))
        self.show_sequence()
        self.master.after(1000, self.get_user_input)

    def show_sequence(self):
        for i, button in self.sequence:
            self.sounds[i].play()
            button.config(bg=self.colors[i])
            self.master.update()
            time.sleep(0.5)
            self.master.update()
            time.sleep(0.5)

    def get_user_input(self):
        for i, button in enumerate(self.buttons):
            button.config(command=lambda i=i, button=button: self.check_user_input(i, button))

    def check_user_input(self, i, button):
        self.user_sequence.append((i, button))
        index = len(self.user_sequence) -  1
        if self.user_sequence[index] != self.sequence[index]:
            for button in self.buttons:
                button.config(bg="black")
            self.master.after(1000, self.game_over)
        elif len(self.user_sequence) == len(self.sequence):
            self.user_sequence = []
            self.master.after(1000, self.start_game)

    def game_over(self):
        tk.messagebox.showinfo("Game over", "You Loose!")
        self.master.quit()

def main():
    pygame.mixer.init()
    window = tk.Tk()
    game = Genius(window)
    start_button = tk.Button(window, text="Start", command=game.start_game)
    start_button.grid(row=2, column=0, columnspan=2)
    window.mainloop()

main()
