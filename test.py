import tkinter as tk
import random
from tawer_defense import MapLoader, Monster1, Monster2, Monster3, Tower

class Game:
    def __init__(self, txt_path="first_map.txt"):
        self.root = tk.Tk()
        self.root.title("Tower Defense Game")
        self.root.geometry("800x600")

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.map_frame = tk.Frame(self.main_frame, width=600, bg='black')  # ตั้งค่าพื้นหลังเป็นสีดำ
        self.map_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.map_loader = MapLoader(self.map_frame, txt_path)
        self.map_loader.canvas.pack(fill=tk.BOTH, expand=True)

        self.create_tower_panel()

        self.monsters = []
        self.spawn_multiplier = 1
        self.spawn_initial_monsters()

        self.root.mainloop()

    def create_tower_panel(self):
        self.tower_panel = tk.Frame(self.main_frame, bg='gray', width=200)
        self.tower_panel.pack(side=tk.RIGHT, fill=tk.Y, expand=False)

    def spawn_monster_delayed(self, monster_class, delay):
        """ สร้างมอนสเตอร์โดยมีการหน่วงเวลา """
        self.root.after(delay, lambda: self.spawn_monster(monster_class))

    def spawn_monster(self, monster_class):
        """ สร้างมอนสเตอร์ 1 ตัว และให้มันเคลื่อนที่ """
        monster = monster_class(self.map_loader.canvas, self.map_loader.path_list)
        self.monsters.append(monster)
        monster.move()

    def spawn_initial_monsters(self):
        """ เริ่มต้นเกมโดยให้ Monster1 เกิดทีละตัว พร้อม delay """
        spawn_delay = 500
        for i in range(4):
            self.spawn_monster_delayed(Monster1, i * spawn_delay)

        self.root.after(7000, lambda: self.spawn_monster(Monster1))
        self.root.after(7000, lambda: self.spawn_monster(Monster2))
        self.root.after(10000, lambda: self.spawn_monster(Monster1))
        self.root.after(10000, lambda: self.spawn_monster(Monster2))

        self.root.after(17000, self.random_spawn)

    def random_spawn(self):
        """ สุ่มเกิดมอนสเตอร์ และจำนวนเพิ่มขึ้น 2 เท่าทุก 5 วินาที """
        if self.spawn_multiplier == 0:
            self.spawn_multiplier = 1
        else:
            self.spawn_multiplier *= 2  # เพิ่มจำนวน *2

        count = int(self.spawn_multiplier)
        monster_types = [Monster1, Monster2, Monster3]

        for _ in range(count):
            random_monster = random.choice(monster_types)
            self.spawn_monster(random_monster)

        self.root.after(7000, self.random_spawn)

# เริ่มเกม
Game("first_map.txt")