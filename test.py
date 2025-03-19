# import tkinter as tk
# import random
# from maploader import MapLoader, Monster1, Monster2, Monster3, Tower

# class Game:
#     def __init__(self, txt_path="first_map.txt"):
#         self.root = tk.Tk()
#         self.root.title("Tower Defense Game")
#         self.root.geometry("800x600")

#         self.main_frame = tk.Frame(self.root)
#         self.main_frame.pack(fill=tk.BOTH, expand=True)

#         self.map_frame = tk.Frame(self.main_frame, width=600, bg='black')  # ตั้งค่าพื้นหลังเป็นสีดำ
#         self.map_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

#         self.map_loader = MapLoader(self.map_frame, txt_path)
#         self.map_loader.canvas.pack(fill=tk.BOTH, expand=True)

#         self.create_tower_panel()

#         self.monsters = []
#         self.spawn_multiplier = 1
#         self.spawn_initial_monsters()

#         self.root.mainloop()

#     def create_tower_panel(self):
#         self.tower_panel = tk.Frame(self.main_frame, bg='gray', width=200)
#         self.tower_panel.pack(side=tk.RIGHT, fill=tk.Y, expand=False)

#     def spawn_monster_delayed(self, monster_class, delay):
#         """ สร้างมอนสเตอร์โดยมีการหน่วงเวลา """
#         self.root.after(delay, lambda: self.spawn_monster(monster_class))

#     def spawn_monster(self, monster_class):
#         """ สร้างมอนสเตอร์ 1 ตัว และให้มันเคลื่อนที่ """
#         monster = monster_class(self.map_loader.canvas, self.map_loader.path_list)
#         self.monsters.append(monster)
#         monster.move()

#     def spawn_initial_monsters(self):
#         """ เริ่มต้นเกมโดยให้ Monster1 เกิดทีละตัว พร้อม delay """
#         spawn_delay = 500
#         for i in range(4):
#             self.spawn_monster_delayed(Monster1, i * spawn_delay)

#         self.root.after(7000, lambda: self.spawn_monster(Monster1))
#         self.root.after(7000, lambda: self.spawn_monster(Monster2))
#         self.root.after(10000, lambda: self.spawn_monster(Monster1))
#         self.root.after(10000, lambda: self.spawn_monster(Monster2))

#         self.root.after(17000, self.random_spawn)

#     def random_spawn(self):
#         """ สุ่มเกิดมอนสเตอร์ และจำนวนเพิ่มขึ้น 2 เท่าทุก 5 วินาที """
#         if self.spawn_multiplier == 0:
#             self.spawn_multiplier = 1
#         else:
#             self.spawn_multiplier *= 2  # เพิ่มจำนวน *2

#         count = int(self.spawn_multiplier)
#         monster_types = [Monster1, Monster2, Monster3]

#         for _ in range(count):
#             random_monster = random.choice(monster_types)
#             self.spawn_monster(random_monster)

#         self.root.after(7000, self.random_spawn)

# # เริ่มเกม
# Game("first_map.txt")


# a = [[[3.8,4,5,6],[7,8,9,10]],[[11,12,13,14],[15,16,17,18]],[[21,22,23,24],[25,26,27,28]]]
# print(len(a))

import numpy as np
import matplotlib.pyplot as plt

# กำหนดจุดข้อมูล
points = {
    "A1": (3, 8), "A2": (9, 4), "A3": (4, 9),
    "A4": (2, 2), "A5": (10, 5), "A6": (2, 4),
    "A7": (6, 8), "A8": (4, 3), "A9": (4, 7)
}

# กำหนด centroid เริ่มต้น
centroids = {
    "C1": points["A1"],
    "C2": points["A4"],
    "C3": points["A7"],
}

# ฟังก์ชันคำนวณระยะห่าง Euclidean
def euclidean_distance(p1, p2):
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# ทำ K-Means Iteration
def k_means(points, centroids, max_iter=10):
    for i in range(max_iter):
        clusters = {c: [] for c in centroids}  # สร้างคลัสเตอร์ใหม่

        # กำหนดแต่ละจุดให้อยู่ในคลัสเตอร์ที่ใกล้ที่สุด
        for point, coords in points.items():
            distances = {c: euclidean_distance(coords, centroids[c]) for c in centroids}
            closest_centroid = min(distances, key=distances.get)
            clusters[closest_centroid].append(point)

        # คำนวณ centroid ใหม่
        new_centroids = {}
        for c, members in clusters.items():
            if members:  # หลีกเลี่ยง division by zero
                avg_x = np.mean([points[m][0] for m in members])
                avg_y = np.mean([points[m][1] for m in members])
                new_centroids[c] = (avg_x, avg_y)
            else:
                new_centroids[c] = centroids[c]

        # ถ้า centroid ไม่เปลี่ยนแปลง แสดงว่า converged แล้ว
        if new_centroids == centroids:
            return clusters, new_centroids

        centroids = new_centroids  # อัปเดต centroid
    
    return clusters, centroids

# รัน K-Means
clusters, final_centroids = k_means(points, centroids)

# กำหนดสีสำหรับแต่ละคลัสเตอร์
colors = {"C1": "blue", "C2": "green", "C3": "red"}

# สร้างกราฟแสดงการกระจายของคลัสเตอร์
plt.figure(figsize=(8, 6))

# พล็อตจุดของแต่ละคลัสเตอร์
for cluster, members in clusters.items():
    x_vals = [points[m][0] for m in members]
    y_vals = [points[m][1] for m in members]
    plt.scatter(x_vals, y_vals, color=colors[cluster], label=f"Cluster {cluster}")

# พล็อต centroid
for cluster, centroid in final_centroids.items():
    plt.scatter(centroid[0], centroid[1], color=colors[cluster], marker="X", s=200, edgecolors="black", label=f"Centroid {cluster}")

# เพิ่มรายละเอียด
plt.xlabel("X Coordinate")
plt.ylabel("Y Coordinate")
plt.title("K-Means Clustering Result")
plt.legend()
plt.grid()

# แสดงกราฟ
plt.show()