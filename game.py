import tkinter as tk
import random
from maploader import MapLoader
from tower import Tower1, Tower
from PIL import Image, ImageTk
from monster import Monster1, Monster2, Monster3, Monster
import time


class Game:
    money = 100
    score = 0
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

        self.root.after(5, self.run_tower)
        self.root.mainloop()

    def spawn_monster_delayed(self, monster_class, delay):
        """ สร้างมอนสเตอร์โดยมีการหน่วงเวลาตาม delay (มิลลิวินาที) """
        self.root.after(delay, lambda: self.spawn_monster(monster_class))

    def spawn_monster(self, monster_class):
        print("Monster created")
        """ สร้างมอนสเตอร์ 1 ตัว และให้มันเคลื่อนที่ """
        monster = monster_class(self.map_loader.canvas, self.map_loader.path_list)
        self.monsters.append(monster)
        monster.move()

    def spawn_initial_monsters(self):
        """ เริ่มต้นเกมโดยให้ Monster1 เกิดทีละตัว พร้อม delay """
        spawn_delay = 500  # เวลาห่างกัน 500 มิลลิวินาที (0.5 วินาที)
        for i in range(2):  # สร้าง Monster1 ทีละตัว
            self.spawn_monster_delayed(Monster1, i * spawn_delay)

        # ตั้งเวลาให้ Monster1 และ Monster2 เกิดหลัง 6 วิ
        # self.root.after(7000, lambda: self.spawn_monster(Monster1))
        # self.root.after(7000, lambda: self.spawn_monster(Monster2))

        # # ตั้งเวลาให้ Monster1, Monster2 เกิดหลัง 10 วิ
        # self.root.after(10000, lambda: self.spawn_monster(Monster1))
        # self.root.after(10000, lambda: self.spawn_monster(Monster2))

        # print("เริ่มตั้งค่าให้เกิดการสุ่มมอนสเตอร์หลังจาก 15 วิ")
        # self.root.after(5000, self.random_spawn)

    def random_spawn(self):
        """ สุ่มเกิดมอนสเตอร์ และจำนวนเพิ่มขึ้น 2 เท่าทุก 5 วินาที """

        # if self.spawn_multiplier == 0:
        #     self.spawn_multiplier = 1
        # else:
        #     self.spawn_multiplier *= 2
        self.spawn_multiplier = 1
        count = int(self.spawn_multiplier) 
        monster_types = [Monster1, Monster2, Monster3] 

        for _ in range(count):
            random_monster = random.choice(monster_types)
            self.spawn_monster(random_monster)
        self.root.after(7000, self.random_spawn)


    def create_tower_panel(self):

        # self.money = 1000
        self.money_label = tk.Label(self.main_frame, text=f"Money: ${Game.money}", font=("Arial", 14))
        self.score_label = tk.Label(self.main_frame,text=f"Score: {Game.score}", font=("Arial", 14))
        self.money_label.pack(side=tk.TOP, fill=tk.X)
        self.score_label.pack(fill=tk.X)



        self.tower_panel = tk.Frame(self.main_frame, bg='gray', width=200, height=600)
        self.tower_panel.pack(side=tk.RIGHT, fill=tk.Y, expand=False)

        tk.Label(self.tower_panel, text="Select Tower:", font=("Arial", 14), bg='gray', fg='white').pack(pady=10)


        self.tower_images = {}

        self.towers = {
            "Tower1": {"cost": 100, "image": "./towerImage/1.png", "id": 10},
            "Tower2": {"cost": 200, "image": "./towerImage/2.png", "id": 20},
            "Tower3": {"cost": 300, "image": "./towerImage/3.png", "id": 30},
        }


        for name, data in self.towers.items():
            
            image = Image.open(data["image"]).resize((50, 50), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            self.tower_images[name] = photo  

            btn = tk.Button(self.tower_panel, text=f"{name} (${data['cost']})", font=("Arial", 12),
                            image=photo, compound="top", command=lambda t=data["id"]: self.select_tower(t))
            btn.pack(pady=5, fill=tk.X)

    # def select_tower(self, id):
    #     """ ✅ ฟังก์ชันเลือก Tower ที่ต้องการวาง """

    #     self.selected_tower = id
    #     self.map_loader.set_towerId(id)

    def select_tower(self, id):
        tower_data = next((data for data in self.towers.values() if data["id"] == id), None)
    
        if tower_data is not None:
            if Game.money >= tower_data["cost"]:
                self.selected_tower = id
                self.map_loader.set_towerId(id)
                Game.money -= tower_data["cost"]
                self.money_label.config(text=f"Money: ${Game.money}")
                # print(f"Tower วางสำเร็จ, เงินที่เหลือ: {Game.money}")
            # else:
                # print("เงินไม่พอสำหรับวาง Tower นี้!")


    def run_tower(self):
        dead_monsters = []
        for tower in self.map_loader.get_tower_list_on_map():
            tower_obj: Tower = tower["tower"]
            nearest_monster = tower_obj.find_target(self.monsters)
            if nearest_monster:
                new_hp  = tower_obj.shoot(nearest_monster)
                # print(f"near {new_hp}")

                # print(f"Monster at {nearest_monster.x}, {nearest_monster.y}) is dead and will be removed.")
                if new_hp <= 0:
                    dead_monsters.append(nearest_monster)  
                    
                    # ดึงค่าจากฟังก์ชัน calculate()
                    money, score = nearest_monster.calculate()
                    
                    # อัปเดตค่าเงินและคะแนนในเกม
                    Game.money += money
                    Game.score += score

        for monster in dead_monsters:
            if monster in self.monsters:
                self.monsters.remove(monster)
                self.map_loader.canvas.delete(monster.monster_obj)
                
                # อัปเดต UI ให้แสดงค่าเงินและคะแนนใหม่
                self.money_label.config(text=f"Money: ${Game.money}")
                self.score_label.config(text=f"Score {Game.score}")
                # print(f"เงินปัจจุบัน: {Game.money}, คะแนน: {Game.score}")

        self.root.after(500, self.run_tower)


    def check_alive(self):
        print(f"long long {Tower.shoot}")

    
    # def total(self):
        
    

# เริ่มเกม
Game("first_map.txt")