# from tawer_defense import MapLoader
import tkinter as tk
import random
import math
# from maploader import MapLoader
class Tower:
    def __init__(self, radius, x, y, canvas, damage, speed):
        self.canvas = canvas
        self.x = x
        self.y = y 
        self.radius = radius
        self.damage = damage
        self.speed = speed


    def find_target(self, enemies):
        for enemy in enemies:
            enemy_distance = self.distance_to(enemy)
            if enemy_distance  <= self.radius:
                self.target = enemy
                return enemy
    
    def distance_to(self, enemy):
        return math.sqrt((self.x - enemy.x * 20) ** 2 + (self.y - enemy.y * 20) ** 2)

    
    def traking_bullet(self):
        self.length = (
            (self.x - (self.target.x)) ** 2 + (self.y - (self.target.y)) ** 2
            
        ) ** 0.5
        if self.length <= 0:
            return
        self.x += self.speed * ((self.target.x) - self.x) / self.length
        self.y += self.speed * ((self.target.y) - self.y) / self.length
    
    def shoot(self, monster):
        print("Shoot Monster", monster)
        print("before", monster.hp)
        monster.hp -= self.damage
        print("after", monster.hp)
        return monster.hp



class Tower1(Tower):
    def __init__(self, x, y, canvas):
        super().__init__(radius=30, x=x, y=y, canvas=canvas, damage=50, speed=15)

class Tower2(Tower):
    def __init__(self, x, y, canvas):
        super().__init__(radius=60, x=x, y=y, canvas=canvas, damage=30,  speed=15)

    
class Tower3(Tower):
    def __init__(self, x, y, canvas):
        super().__init__(radius=100, x=x, y=y, canvas=canvas, damage=150, speed=7)
