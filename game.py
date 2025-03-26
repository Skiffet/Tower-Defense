import tkinter as tk
import random
from maploader import MapLoader
from tower import Tower1, Tower
from PIL import Image, ImageTk
from monster import Monster1, Monster2, Monster3, Monster
import time
import csv
import os

class Game:
    # money = 100
    # score = 0
    def __init__(self, root, txt_path="first_map.txt"):
        self.start_time = time.time()
        self.total_monster_killed = 0
        self.total_tower_placed = 0
        self.total_damege = 0

        self.money = 100
        self.score = 0
        self.root = root
        # self.root.title("Tower Defense Game")

        # self.root.geometry("800x600")

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.map_frame = tk.Frame(self.main_frame, width=600)
        self.map_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.map_loader = MapLoader(self.map_frame, txt_path, game=self)
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
        self.root.after(7000, lambda: self.spawn_monster(Monster1))
        self.root.after(7000, lambda: self.spawn_monster(Monster2))

        # ตั้งเวลาให้ Monster1, Monster2 เกิดหลัง 10 วิ
        self.root.after(10000, lambda: self.spawn_monster(Monster1))
        self.root.after(10000, lambda: self.spawn_monster(Monster2))

        print("เริ่มตั้งค่าให้เกิดการสุ่มมอนสเตอร์หลังจาก 15 วิ")
        self.root.after(5000, self.random_spawn)

    def random_spawn(self):
        """ สุ่มเกิดมอนสเตอร์ และจำนวนเพิ่มขึ้น 2 เท่าทุก 5 วินาที """

        if self.spawn_multiplier == 0:
            self.spawn_multiplier = 1
        else:
            self.spawn_multiplier *= 2
        self.spawn_multiplier = 1
        count = int(self.spawn_multiplier) 
        monster_types = [Monster1, Monster2, Monster3] 

        for _ in range(count):
            random_monster = random.choice(monster_types)
            self.spawn_monster(random_monster)
        self.root.after(7000, self.random_spawn)


    def create_tower_panel(self):

        # self.money = 1000
        self.money_label = tk.Label(self.main_frame, text=f"Money: ${self.money}", font=("Arial", 14))
        self.score_label = tk.Label(self.main_frame,text=f"Score: {self.score}", font=("Arial", 14))
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

    def select_tower(self, id):
        tower_data = next((data for data in self.towers.values() if data["id"] == id), None)
        if tower_data is not None:
            if self.money >= tower_data["cost"]:
                self.total_tower_placed += 1
                self.selected_tower = id
                self.map_loader.set_towerId(id)
                self.money_label.config(text=f"Money: ${self.money}")


    def run_tower(self):
        dead_monsters = []
        for tower in self.map_loader.get_tower_list_on_map():
            tower_obj: Tower = tower["tower"]
            nearest_monster = tower_obj.find_target(self.monsters)
            if nearest_monster:
                new_hp  = tower_obj.shoot(nearest_monster)
                if new_hp <= 0:
                    
                    self.total_monster_killed += 1
                    self.total_damege += tower_obj.get_damage()

                    dead_monsters.append(nearest_monster)
                    money, score = nearest_monster.calculate()
                    self.money += money
                    self.score += score

        for monster in dead_monsters:
            if monster in self.monsters:
                self.monsters.remove(monster)
                self.map_loader.canvas.delete(monster.monster_obj)
                self.money_label.config(text=f"Money: ${self.money}")
                self.score_label.config(text=f"Score: {self.score}")
        
            # เช็คว่า Monster ถึงจุดสุดท้ายหรือยัง
        for monster in self.monsters:
            if monster.current_step >= len(monster.path_list) - 1:
                self.game_over()
                return

        self.root.after(500, self.run_tower)


    def check_alive(self):
        print(f"long long {Tower.shoot}")

    
     
    def game_over(self):
        play_time = time.time() - self.start_time
        minutes = int(play_time // 60)
        seconds = int(play_time % 60)

        self.history()

        msg = f"You Lost!\nScore: {self.score}\nTime: {minutes}m {seconds}s"

        import tkinter.messagebox as msgbox
        msgbox.showinfo("Game Over กากมาก", msg)

        # ปิดเกม (หรือจะให้ restart ก็ได้)
        self.root.destroy()

    
    def history(self):
        play_time = time.time() - self.start_time
        # minutes = int(play_time // 60)
        seconds = int(play_time % 60)
        print("History")
        print(f"Total Monster Killed: {self.total_monster_killed}")
        print(f"Total Tower Placed: {self.total_tower_placed}")
        print(f"Total Damage: {self.total_damege}")
        print(f"Total Score: {self.score}")
        print(f"Total Time: {seconds}")


        file_empty = not os.path.exists("history.csv") or os.stat("history.csv").st_size == 0
        with open("history.csv", mode="a", newline='') as file:
            writer = csv.writer(file)
            if file_empty:
                writer.writerow(["Time", "Monsters Killed", "Towers Placed", "Damage", "Score"])  # ✅ เขียน header ถ้าว่าง
            writer.writerow([
                seconds,
                self.total_monster_killed,
                self.total_tower_placed,
                self.total_damege,
                self.score
            ]) 

