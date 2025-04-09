import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from game import Game
from analyze import GameDataAnalysis

root = tk.Tk()
root.title("Tower Defense - Main Menu")
root.geometry("800x600")
root.resizable(False, False)

bg_image = Image.open("bg.jpg").resize((800, 600))
bg_photo = ImageTk.PhotoImage(bg_image)

canvas = tk.Canvas(root, width=800, height=600, highlightthickness=0)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

canvas.create_text(400, 80, text="Tower Defense", font=("Arial", 36, "bold"), fill="white")
canvas.create_text(400, 150, text="เลือกแผนที่:", font=("Arial", 16), fill="white")

map_options = ["first_map.txt", "second_map.txt"]
map_var = tk.StringVar()
map_var.set(map_options[0])

style = ttk.Style()
style.theme_use("default")
style.configure(
    "Custom.TMenubutton",   
    background="#444",
    foreground="white",
    font=("Arial", 12),
    padding=5
)

option_menu = ttk.OptionMenu(root, map_var, map_options[0], *map_options)
option_menu.config(style="Custom.TMenubutton")
canvas.create_window(400, 200, window=option_menu)

# ปุ่ม Play
def on_play_click(event=None):
    selected_map = map_var.get()
    root.destroy()
    game_root = tk.Tk()
    Game(game_root, selected_map)
    game_root.mainloop()

play_rect = canvas.create_rectangle(300, 250, 500, 300, fill="#222", outline="white", width=2)
play_text = canvas.create_text(400, 275, text="Play", font=("Arial", 16), fill="white")
canvas.tag_bind(play_rect, "<Button-1>", on_play_click)
canvas.tag_bind(play_text, "<Button-1>", on_play_click)


def on_analyse_click(event=None):
    GameDataAnalysis(csv_path="history.csv")


analyse_rect = canvas.create_rectangle(300, 320, 500, 370, fill="#222", outline="white", width=2)
analyse_text = canvas.create_text(400, 345, text="Analyse", font=("Arial", 16), fill="white")
canvas.tag_bind(analyse_rect, "<Button-1>", on_analyse_click)
canvas.tag_bind(analyse_text, "<Button-1>", on_analyse_click)

root.mainloop()