import tkinter as tk
import random
from tawer_defense import MapLoader, Monster1, Monster2, Monster3, Tower
from PIL import Image, ImageTk

class Game:
    def __init__(self, txt_path="first_map.txt"):
        self.root = tk.Tk()
        self.root.title("Tower Defense Game")

        self.root.geometry("800x600")

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.map_frame = tk.Frame(self.main_frame, width=600)
        self.map_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.map_loader = MapLoader(self.map_frame, txt_path)
        self.map_loader.canvas.pack(fill=tk.BOTH, expand=True) 

        self.create_tower_panel()

        self.monsters = []
        self.spawn_multiplier = 1
        self.spawn_initial_monsters()

        self.root.mainloop()
        

    def spawn_monster_delayed(self, monster_class, delay):
        """ สร้างมอนสเตอร์โดยมีการหน่วงเวลาตาม delay (มิลลิวินาที) """
        self.root.after(delay, lambda: self.spawn_monster(monster_class))


    def spawn_monster(self, monster_class):
        """ สร้างมอนสเตอร์ 1 ตัว และให้มันเคลื่อนที่ """
        monster = monster_class(self.map_loader.canvas, self.map_loader.path_list)
        self.monsters.append(monster)
        monster.move()

    def spawn_initial_monsters(self):
        """ เริ่มต้นเกมโดยให้ Monster1 เกิดทีละตัว พร้อม delay """
        spawn_delay = 500  # เวลาห่างกัน 500 มิลลิวินาที (0.5 วินาที)
        for i in range(4):  # สร้าง Monster1 ทีละตัว
            self.spawn_monster_delayed(Monster1, i * spawn_delay)

        # ตั้งเวลาให้ Monster1 และ Monster2 เกิดหลัง 6 วิ
        self.root.after(7000, lambda: self.spawn_monster(Monster1))
        self.root.after(7000, lambda: self.spawn_monster(Monster2))

        # ตั้งเวลาให้ Monster1, Monster2 เกิดหลัง 10 วิ
        self.root.after(10000, lambda: self.spawn_monster(Monster1))
        self.root.after(10000, lambda: self.spawn_monster(Monster2))

        # print("เริ่มตั้งค่าให้เกิดการสุ่มมอนสเตอร์หลังจาก 15 วิ")
        self.root.after(17000, self.random_spawn)

    def random_spawn(self):
        """ สุ่มเกิดมอนสเตอร์ และจำนวนเพิ่มขึ้น 2 เท่าทุก 5 วินาที """

        if self.spawn_multiplier == 0:
            self.spawn_multiplier = 1
        else:
            self.spawn_multiplier *= 2

        count = int(self.spawn_multiplier) 
        monster_types = [Monster1, Monster2, Monster3] 

        for _ in range(count):
            random_monster = random.choice(monster_types)
            self.spawn_monster(random_monster)
        self.root.after(7000, self.random_spawn)


    def create_tower_panel(self):

        self.money = 1000
        self.money_label = tk.Label(self.main_frame, text=f"Money: ${self.money}", font=("Arial", 14))
        self.money_label.pack(side=tk.TOP, fill=tk.X)



        self.tower_panel = tk.Frame(self.main_frame, bg='gray', width=200, height=600)
        self.tower_panel.pack(side=tk.RIGHT, fill=tk.Y, expand=False)

        tk.Label(self.tower_panel, text="Select Tower:", font=("Arial", 14), bg='gray', fg='white').pack(pady=10)


        self.tower_images = {}

        towers = {
            "Tower1": {"cost": 100, "image": "./towerImage/1.png", "id": 10},
            "Tower2": {"cost": 200, "image": "./towerImage/2.png", "id": 20},
            "Tower3": {"cost": 300, "image": "./towerImage/3.png", "id": 30},
        }


        for name, data in towers.items():
            
            image = Image.open(data["image"]).resize((50, 50), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            self.tower_images[name] = photo  

            btn = tk.Button(self.tower_panel, text=f"{name} (${data['cost']})", font=("Arial", 12),
                            image=photo, compound="top", command=lambda t=data["id"]: self.select_tower(t))
            btn.pack(pady=5, fill=tk.X)

    def select_tower(self, id):
        """ ✅ ฟังก์ชันเลือก Tower ที่ต้องการวาง """
        self.selected_tower = id
        self.map_loader.set_towerId(id)

    

# เริ่มเกม
Game("first_map.txt")