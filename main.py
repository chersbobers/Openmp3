from tkinter import *
from tkinter import filedialog
import pygame
import os

root = Tk()
root.title("RASPMP3")
root.geometry("600x400")
#programIcon = pygame.image.load('icon.png')
#pygame.display.set_icon(programIcon)


pygame.mixer.init()

menubar = Menu(root)
root.config(menu=menubar)

songs = []
current_song = ""
paused = False

def load_music():
    global current_song
    root.directory = filedialog.askdirectory()

    for song in os.listdir(root.directory):
        name, ext = os.path.splitext(song)
        if ext == ".mp3":
            songs.append(song)

    for song in songs:
        songList.insert(END, song)

    songList.selection_set(0)
    current_song = songs[songList.curselection()[0]]

def play_music():
    global current_song, paused

    if not paused:
        pygame.mixer.music.load(os.path.join(root.directory, current_song))
        pygame.mixer.music.play()
    else:
        pygame.mixer.music.unpause()
        paused = False

def pause_music():
    global paused
    pygame.mixer.music.pause()
    paused = True

def next_music():
    global current_song, paused
    try:
        songList.selection_clear(0, END)
        next_index = songs.index(current_song) + 1
        if next_index < len(songs):
            songList.selection_set(next_index)
            current_song = songs[songList.curselection()[0]]
            play_music()
        else:
            # Handle the case when the current song is the last in the list
            songList.selection_set(0)
            current_song = songs[0]
            play_music()
    except IndexError:
        pass

def previous_music():
    global current_song, paused
    try:
        songList.selection_clear(0, END)
        prev_index = songs.index(current_song) - 1
        if prev_index >= 0:
            songList.selection_set(prev_index)
            current_song = songs[songList.curselection()[0]]
            play_music()
        else:
            # Handle the case when the current song is the first in the list
            songList.selection_set(len(songs) - 1)
            current_song = songs[-1]
            play_music()
    except IndexError:
        pass

organize_menu = Menu(menubar, tearoff=False)
organize_menu.add_command(label="Open Folder", command=load_music)
menubar.add_cascade(label="Songs", menu=organize_menu)

songList = Listbox(root, bg="black", fg="white", width=100, height=15)
songList.pack()

control_frame = Frame(root)
control_frame.pack()
play_btn_img = PhotoImage(file="play.png")
pause_btn_img = PhotoImage(file="pause.png")
next_btn_img = PhotoImage(file="next.png")
previous_btn_img = PhotoImage(file="previous.png")

play_btn = Button(control_frame, image=play_btn_img, borderwidth=0, command=play_music)
pause_btn = Button(control_frame, image=pause_btn_img, borderwidth=0, command=pause_music)
next_btn = Button(control_frame, image=next_btn_img, borderwidth=0, command=next_music)
previous_btn = Button(control_frame, image=previous_btn_img, borderwidth=0, command=previous_music)

play_btn.grid(row=0, column=1, padx=7, pady=10)
pause_btn.grid(row=0, column=2, padx=7, pady=10)
next_btn.grid(row=0, column=3, padx=7, pady=10)
previous_btn.grid(row=0, column=0, padx=7, pady=10)

root.mainloop()
