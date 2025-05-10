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
        self.monster_obj = self.canvas.create_image(self.x * self.block_size, self.y * self.block_size, image=self.image_tk, anchor=tk.NW)
        self.canvas.addtag_withtag('monster', self.monster_obj)


    def move(self):
        if self.hp <= 0:
            return
        
        if self.current_step < len(self.path_list) - 1:
            target_x, target_y = self.path_list[self.current_step + 1]
            
            dx = (target_x - self.x) * self.block_size
            dy = (target_y - self.y) * self.block_size
            self.canvas.move(self.monster_obj, dx, dy)
            self.x, self.y = target_x, target_y
            self.current_step += 1
            self.canvas.after(self.speed, self.move)

    def calculate(self):
        return self.amount, self.score


class Monster1(Monster): 
    def __init__(self, canvas, path_list, block_size=20):
        super().__init__(canvas, path_list, "./mosterImage/Monster1.png", speed=300, block_size=block_size, hp=30, amount=40, score = 10)


class Monster2(Monster):
    def __init__(self, canvas, path_list, block_size=20):
        super().__init__(canvas, path_list, "./mosterImage/Monster2.png", speed=500, block_size=block_size, hp=70, amount = 40, score = 20)

class Monster3(Monster):
    def __init__(self, canvas, path_list,block_size=20):
        super().__init__(canvas, path_list, "./mosterImage/MonsterBig.png", speed=350, block_size=block_size, hp=150, amount = 100, score = 40)
