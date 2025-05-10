import tkinter as tk
from PIL import Image, ImageTk
import math
from tower import *


class MapLoader:
    def __init__(self, root, txt_path="first_map.txt", block_size=20, row_length=30, game=None):
        self.root = root
        self.txt_path = txt_path
        self.block_size = block_size
        self.row_length = row_length
        self.grid = []
        self.path_list = []
        self.tower_lit = 0  # ✅ เก็บ ID ของ Tower ที่เลือก
        self.towers = []  # ✅ เก็บออบเจ็กต์ของ Tower ที่สร้าง


        self.game = game

        self.load_map()
        self.load_images()

        self.canvas = tk.Canvas(self.root, width=self.row_length * self.block_size, height=len(self.grid) * self.block_size)
        self.canvas.pack()

        self.draw_map()
        self.canvas.bind("<Button-1>", self.on_click)

    def load_map(self):
        with open(self.txt_path, "r") as file: 
            data = list(map(int, file.read().split()))  
            self.grid = [data[i:i + self.row_length] for i in range(0, len(data), self.row_length)]
        self.path_list = self.find_path_order()

    def find_path_order(self):
        start = next(((x, y) for y, row in enumerate(self.grid) for x, block in enumerate(row) if block == 1), None)

        if not start : return []

        path_order = []
        queue = [start]
        visited = set(queue)

        while queue:
            x, y = queue.pop(0)
            path_order.append((x, y))

            directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

            for dx, dy in directions:
                nx, ny = x + dx, y + dy

                if (0 <= nx < len(self.grid[0]) and 0 <= ny < len(self.grid) and 
                    self.grid[ny][nx] == 1 and (nx, ny) not in visited):
                    
                    queue.append((nx, ny))
                    visited.add((nx, ny))

        return path_order
    
    def load_images(self):
        self.textures = {
            0: Image.open("./mapImage/NormalBlock.png").resize((self.block_size, self.block_size)),
            1: Image.open("./mapImage/PathBlock.png").resize((self.block_size, self.block_size)),
            2: Image.open("./mapImage/WaterBlock.png").resize((self.block_size, self.block_size)),
            10: Image.open("./towerImage/1.png").resize((self.block_size, self.block_size)),
            20: Image.open("./towerImage/2.png").resize((self.block_size, self.block_size)),
            30: Image.open("./towerImage/3.png").resize((self.block_size, self.block_size)),
        }

    def draw_map(self):
        self.image_refs = []
        self.canvas.delete("all")
        for y, row in enumerate(self.grid):
            for x, block in enumerate(row):
                img = ImageTk.PhotoImage(self.textures.get(block, self.textures[0]))
                self.canvas.create_image(x * self.block_size, y * self.block_size, image=img, anchor=tk.NW)
                self.image_refs.append(img)

    def set_towerId(self, tower_id):
        self.tower_lit = tower_id


    def on_click(self, event):
        x = event.x // self.block_size
        y = event.y // self.block_size

        if self.tower_lit == 0:
            return

        if self.grid[y][x] in [1, 2]:
            print("Cannot place tower on path or water!")
            return

        if self.grid[y][x] in [10, 20, 30]:
            print("Tower already placed here!")
            return

        tower_data = next((data for data in self.game.towers.values() if data["id"] == self.tower_lit), None)
        
        if self.game.money < tower_data["cost"]:
            print("เงินไม่พอ! ไม่สามารถวาง Tower ได้")
            return

        self.game.money -= tower_data["cost"]
        self.game.money_label.config(text=f"Money: ${self.game.money}")

        img = ImageTk.PhotoImage(self.textures[self.tower_lit])
        tower = None

        if self.tower_lit == 10:
            tower = Tower1(x=event.x, y=event.y, canvas=self.canvas)
        elif self.tower_lit == 20:
            tower = Tower2(x=event.x, y=event.y, canvas=self.canvas)
        elif self.tower_lit == 30:
            tower = Tower3(x=event.x, y=event.y, canvas=self.canvas)

        self.towers.append({
            "tower": tower,
            "tower_img": img,
        })

        self.canvas.create_image(x * self.block_size, y * self.block_size, image=img, anchor=tk.NW)

    def get_tower_list_on_map(self):
        return self.towers
    

    