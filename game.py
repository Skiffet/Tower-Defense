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
    def __init__(self, root, txt_path="first_map.txt"):
        self.start_time = time.time()
        self.total_monster_killed = 0
        self.total_tower_1_placed = 0
        self.total_tower_2_placed = 0
        self.total_tower_3_placed = 0
        self.total_damege = 0

        self.money = 100
        self.score = 0
        self.root = root
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
        self.root.after(delay, lambda: self.spawn_monster(monster_class))

    def spawn_monster(self, monster_class): 
        monster = monster_class(self.map_loader.canvas, self.map_loader.path_list)
        self.monsters.append(monster)
        monster.move()

    def spawn_initial_monsters(self):
        spawn_delay = 500 
        for i in range(2): 
            self.spawn_monster_delayed(Monster1, i * spawn_delay)
        self.root.after(7000, lambda: self.spawn_monster(Monster1))
        self.root.after(7000, lambda: self.spawn_monster(Monster2))
        self.root.after(10000, lambda: self.spawn_monster(Monster1))
        self.root.after(10000, lambda: self.spawn_monster(Monster2))
        self.root.after(15000, self.random_spawn)


    def random_spawn(self):
        if not hasattr(self, 'wave'):
            self.wave = 1
        else:
            self.wave += 1

        print(f"Wave {self.wave} เริ่มแล้ว!")

        count = random.randint(2 + self.wave, 4 + self.wave * 2)
        monster_types = [Monster1, Monster2, Monster3]
        if self.wave < 3:
            weights = [0.6, 0.4, 0.0]
        elif self.wave < 6:
            weights = [0.4, 0.4, 0.2]
        else:
            weights = [0.2, 0.3, 0.5]

        for _ in range(count):
            monster_class = random.choices(monster_types, weights)[0]
            if hasattr(monster_class, 'speed'):
                monster_class.speed += self.wave * 0.1
            self.spawn_monster(monster_class)

        min_delay = max(2000, 8000 - self.wave * 500)
        max_delay = max(4000, 12000 - self.wave * 500)
        next_delay = random.randint(min_delay, max_delay)
        self.root.after(next_delay, self.random_spawn)

        if self.wave >= 20:
            print("WIN")
            self.game_over(win=True)
            return

        if hasattr(self, 'base_hp') and self.base_hp <= 0:
            print("Game Over! ฐานถูกทำลาย")
            self.game_over(win=False)
            return

    def game_over(self, win=False):
        if win:
            print("WIN")
        else:
            print("LOSS")
        self.root.quit()


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

    def select_tower(self, tower_id):
        tower_data = next((data for data in self.towers.values() if data["id"] == tower_id), None)
        if tower_data and self.money >= tower_data["cost"]:
            self.selected_tower = tower_id
            self.map_loader.set_towerId(tower_id)
            self.money_label.config(text=f"Money: ${self.money}")

            tower_type_map = {
                10: 'total_tower_1_placed',
                20: 'total_tower_2_placed',
                30: 'total_tower_3_placed'
            }

            attr_name = tower_type_map.get(tower_id)
            if attr_name:
                setattr(self, attr_name, getattr(self, attr_name) + 1)

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
        
            
        for monster in self.monsters:
            if monster.current_step >= len(monster.path_list) - 1:
                self.game_over()
                return

        self.root.after(500, self.run_tower)


    # def check_alive(self):
    #     print(f"long long {Tower.shoot}")

    
    def game_over(self):
        play_time = time.time() - self.start_time
        minutes = int(play_time // 60)
        seconds = int(play_time % 60)

        self.history()

        msg = f"You Lost!\nScore: {self.score}\nTime: {minutes}m {seconds}s"

        import tkinter.messagebox as msgbox
        msgbox.showinfo("Game Over", msg)

        self.root.destroy()

    
    def history(self):
        play_time = time.time() - self.start_time
        # minutes = int(play_time // 60)
        seconds = int(play_time % 60)
        print("History")
        print(f"Total Monster Killed: {self.total_monster_killed}")
        print(f"Total Damage: {self.total_damege}")
        print(f"Total Score: {self.score}")
        print(f"Total Time: {seconds}")
        print(f"Tower1 Placed: {self.total_tower_1_placed}")
        print(f"Tower2 Placed: {self.total_tower_2_placed}")
        print(f"Tower3 Placed: {self.total_tower_3_placed}")


        file_empty = not os.path.exists("history.csv") or os.stat("history.csv").st_size == 0
        with open("history.csv", mode="a", newline='') as file:
            writer = csv.writer(file)
            if file_empty:
                writer.writerow(["Time", "Monsters Killed", "Damage", "Score", "Tower1", "Tower2", "Tower3"])
            writer.writerow([
                seconds,
                self.total_monster_killed,
                self.total_damege,
                self.score,
                self.total_tower_1_placed,
                self.total_tower_2_placed,
                self.total_tower_3_placed
            ]) 

