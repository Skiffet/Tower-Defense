from PIL import Image, ImageTk
import tkinter as tk


class Monster:
    def __init__(self, canvas, path_list, image_path, speed, block_size=20, hp=0, amount=0, score = 0):
        self.canvas = canvas
        self.path_list = path_list
        self.current_step = 0
        self.block_size = block_size
        self.speed = speed
        self.hp = hp
        self.amount = amount 
        self.score = score 

        self.x, self.y = self.path_list[0] if self.path_list else (0, 0)

        self.image = Image.open(image_path).resize((self.block_size, self.block_size))
        self.image_tk = ImageTk.PhotoImage(self.image)

        # self.monster_obj = self.canvas.create_image(self.x * self.block_size, self.y * self.block_size, image=self.image_tk, anchor=tk.NW)
        self.monster_obj = self.canvas.create_image(self.x * self.block_size, self.y * self.block_size, image=self.image_tk, anchor=tk.NW)
        self.canvas.addtag_withtag('monster', self.monster_obj)


    def move(self):
        if self.hp <= 0:
            return
        
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

    def calculate(self):
        # self.amount += self.amount 
        # self.score += self.score
        return self.amount, self.score


class Monster1(Monster): 
    def __init__(self, canvas, path_list, block_size=20):
        super().__init__(canvas, path_list, "./mosterImage/Monster1.png", speed=300, block_size=block_size, hp=50, amount=100, score = 10)


class Monster2(Monster):
    def __init__(self, canvas, path_list, block_size=20):
        super().__init__(canvas, path_list, "./mosterImage/Monster2.png", speed=200, block_size=block_size, hp=150, amount = 150, score = 15)

class Monster3(Monster):
    def __init__(self, canvas, path_list,block_size=20):
        super().__init__(canvas, path_list, "./mosterImage/MonsterBig.png", speed=200, block_size=block_size, hp=300, amount = 200, score = 20)
