import tkinter as tk
from PIL import Image, ImageTk
import math



class MapLoader:
    def __init__(self, root, txt_path="first_map.txt", block_size=20, row_length=30):
        self.root = root
        self.txt_path = txt_path
        self.block_size = block_size
        self.row_length = row_length
        self.grid = []
        self.path_list = []
        self.tower_lit = 0  # ✅ เก็บ ID ของ Tower ที่เลือก
        self.towers = []  # ✅ เก็บออบเจ็กต์ของ Tower ที่สร้าง

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
        """ ✅ อัปเดต ID ของ Tower ที่เลือก """
        self.tower_lit = tower_id

    def on_click(self, event):
        """ ✅ เมื่อคลิก ให้เปลี่ยน `self.grid` และวาง Tower ลงบน Canvas """
        x = event.x // self.block_size
        y = event.y // self.block_size

        print(event.x, event.y)

        if self.tower_lit == 0:
            print("Please select a Tower first!")
            return

        if self.grid[y][x] in [1, 2]:
            print("Cannot place tower on path or water!")
            return

        if self.grid[y][x] in [10, 20, 30]:
            print("Tower already placed here!")
            return

        self.grid[y][x] = self.tower_lit
        
        img = ImageTk.PhotoImage(self.textures[self.tower_lit])
        self.towers.append(img)
        self.canvas.create_image(x * self.block_size, y * self.block_size, image=img, anchor=tk.NW)

    



class Monster:
    def __init__(self, canvas, path_list, image_path, speed, block_size=20, hp=00):
        self.canvas = canvas
        self.path_list = path_list
        self.current_step = 0
        self.block_size = block_size
        self.speed = speed
        self.hp = hp

        self.x, self.y = self.path_list[0] if self.path_list else (0, 0)

        self.image = Image.open(image_path).resize((self.block_size, self.block_size))
        self.image_tk = ImageTk.PhotoImage(self.image)

        # self.monster_obj = self.canvas.create_image(self.x * self.block_size, self.y * self.block_size, image=self.image_tk, anchor=tk.NW)
        self.monster_obj = self.canvas.create_image(self.x * self.block_size, self.y * self.block_size, image=self.image_tk, anchor=tk.NW)
        self.canvas.addtag_withtag('monster', self.monster_obj)


    def move(self):
            if self.current_step < len(self.path_list) - 1:
                target_x, target_y = self.path_list[self.current_step + 1]
                
                dx = (target_x - self.x) * self.block_size
                dy = (target_y - self.y) * self.block_size

                # อัปเดตตำแหน่ง
                self.canvas.move(self.monster_obj, dx, dy)

                # อัปเดตค่าพิกัดใหม่
                self.x, self.y = target_x, target_y
                self.current_step += 1

                # เคลื่อนที่ต่อไปหลังจากเวลาที่กำหนด
                self.canvas.after(self.speed, self.move)



class Monster1(Monster): 
    def __init__(self, canvas, path_list, block_size=20):
        super().__init__(canvas, path_list, "./mosterImage/Monster1.png", speed=300, block_size=block_size, hp=50)


class Monster2(Monster):
    def __init__(self, canvas, path_list, block_size=20):
        super().__init__(canvas, path_list, "./mosterImage/Monster2.png", speed=200, block_size=block_size, hp=150)

class Monster3(Monster):
    def __init__(self, canvas, path_list,block_size=20):
        super().__init__(canvas, path_list, "./mosterImage/MonsterBig.png", speed=100, block_size=block_size, hp=300)
        
class Tower:
    def __init__(self, radius, canvas, x, y):
        self.canvas = canvas
        self.x = x
        self.y = y  
        self.radius = radius


        