# import tkinter as tk
# from PIL import Image, ImageTk

# class MapLoader:
#     def __init__(self, root, txt_path="first_map.txt", block_size=20, row_length=30):
#         self.root = root
#         self.txt_path = txt_path
#         self.block_size = block_size
#         self.row_length = row_length
#         self.grid = []
#         self.path_list = []
#         self.tower_lit = 0  # ✅ เก็บ ID ของ Tower ที่เลือก
#         self.towers = []  # ✅ เก็บออบเจ็กต์ของ Tower ที่สร้าง

#         self.load_map()
#         self.load_images()

#         self.canvas = tk.Canvas(self.root, width=self.row_length * self.block_size, height=len(self.grid) * self.block_size)
#         self.canvas.pack()

#         self.draw_map()
#         self.canvas.bind("<Button-1>", self.on_click)

#     def load_map(self):
#         with open(self.txt_path, "r") as file: 
#             data = list(map(int, file.read().split()))  
#             self.grid = [data[i:i + self.row_length] for i in range(0, len(data), self.row_length)]
#         self.path_list = self.find_path_order()

#     def find_path_order(self):
#         # ค้นหาจุดเริ่มต้นของเส้นทาง (ค่าที่เป็น 1)
#         start = next(((x, y) for y, row in enumerate(self.grid) for x, block in enumerate(row) if block == 1), None)

#         if not start : return []

#         path_order = []
#         queue = [start]
#         visited = set(queue)

#         while queue:
#             x, y = queue.pop(0)
#             path_order.append((x, y))

#             directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

#             for dx, dy in directions:
#                 nx, ny = x + dx, y + dy

#                 if (0 <= nx < len(self.grid[0]) and 0 <= ny < len(self.grid) and 
#                     self.grid[ny][nx] == 1 and (nx, ny) not in visited):
                    
#                     queue.append((nx, ny))
#                     visited.add((nx, ny))

#         return path_order
    
#     def load_images(self):
#         self.textures = {
#             0: Image.open("./mapImage/NormalBlock.png").resize((self.block_size, self.block_size)),
#             1: Image.open("./mapImage/PathBlock.png").resize((self.block_size, self.block_size)),
#             2: Image.open("./mapImage/WaterBlock.png").resize((self.block_size, self.block_size)),
#             10: Image.open("./towerImage/1.png").resize((self.block_size, self.block_size)),
#             20: Image.open("./towerImage/2.png").resize((self.block_size, self.block_size)),
#             30: Image.open("./towerImage/3.png").resize((self.block_size, self.block_size)),
#         }

#     def draw_map(self):
#         self.image_refs = []
#         self.canvas.delete("all")  # ✅ ล้าง Canvas ก่อนวาดใหม่
#         for y, row in enumerate(self.grid):
#             for x, block in enumerate(row):
#                 img = ImageTk.PhotoImage(self.textures.get(block, self.textures[0]))
#                 self.canvas.create_image(x * self.block_size, y * self.block_size, image=img, anchor=tk.NW)
#                 self.image_refs.append(img)  # ✅ ป้องกันรูปหาย

#     def set_towerId(self, tower_id):
#         """ ✅ อัปเดต ID ของ Tower ที่เลือก """
#         self.tower_lit = tower_id
#         print(f"Selected Tower ID: {self.tower_lit}")

#     def on_click(self, event):
#         """ ✅ เมื่อคลิก ให้เปลี่ยน `self.grid` และวาง Tower ลงบน Canvas """
#         x = event.x // self.block_size
#         y = event.y // self.block_size

#         # ✅ ตรวจสอบว่ามีการเลือก Tower แล้วหรือไม่
#         if self.tower_lit == 0:
#             print("Please select a Tower first!")
#             return

#         # ✅ ตรวจสอบว่าไม่สามารถวาง Tower บนทางเดินหรือพื้นน้ำได้
#         if self.grid[y][x] in [1, 2]:
#             print("Cannot place tower on path or water!")
#             return

#         # ✅ ตรวจสอบว่าตำแหน่งนี้มี Tower อยู่แล้วหรือไม่
#         if self.grid[y][x] in [10, 20, 30]:
#             print("Tower already placed here!")
#             return

#         # ✅ วาง Tower และอัปเดตแผนที่
#         self.grid[y][x] = self.tower_lit
#         print(f"Placed Tower {self.tower_lit} at ({x}, {y})")
        
#         # ✅ วาดรูป Tower ทันทีโดยไม่ต้อง redraw ทั้งหมด
#         img = ImageTk.PhotoImage(self.textures[self.tower_lit])
#         self.towers.append(img)  # ป้องกันรูปหาย
#         self.canvas.create_image(x * self.block_size, y * self.block_size, image=img, anchor=tk.NW)

# class Game:
#     def __init__(self, txt_path="first_map.txt"):
#         self.root = tk.Tk()
#         self.root.title("Tower Defense Game")

#         self.root.geometry("800x600")

#         self.main_frame = tk.Frame(self.root)
#         self.main_frame.pack(fill=tk.BOTH, expand=True)

#         self.map_frame = tk.Frame(self.main_frame, width=600)
#         self.map_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

#         self.map_loader = MapLoader(self.map_frame, txt_path)
#         self.map_loader.canvas.pack(fill=tk.BOTH, expand=True) 

#         self.create_tower_panel()

#         self.root.mainloop()

#     def create_tower_panel(self):
#         self.tower_panel = tk.Frame(self.main_frame, bg='gray', width=200, height=600)
#         self.tower_panel.pack(side=tk.RIGHT, fill=tk.Y, expand=False)

#         tk.Label(self.tower_panel, text="Select Tower:", font=("Arial", 14), bg='gray', fg='white').pack(pady=10)

#         self.tower_images = {}

#         towers = {
#             "Tower1": {"cost": 100, "image": "./towerImage/1.png", "id": 10},
#             "Tower2": {"cost": 200, "image": "./towerImage/2.png", "id": 20},
#             "Tower3": {"cost": 300, "image": "./towerImage/3.png", "id": 30},
#         }

#         for name, data in towers.items():
#             image = Image.open(data["image"]).resize((50, 50), Image.Resampling.LANCZOS)
#             photo = ImageTk.PhotoImage(image)
#             self.tower_images[name] = photo  

#             btn = tk.Button(self.tower_panel, text=f"{name} (${data['cost']})", font=("Arial", 12),
#                             image=photo, compound="top", command=lambda t=data["id"]: self.select_tower(t))
#             btn.pack(pady=5, fill=tk.X)

#     def select_tower(self, id):
#         """ ✅ เลือก Tower และอัปเดตใน MapLoader """
#         self.selected_tower = id
#         self.map_loader.set_towerId(id)

# # เริ่มเกม
# Game("first_map.txt")


class Tower:
    def __init__(self, dmg):
        self.dmg = dmg


class Tower1(Tower):
    def __init__(self):
        super().__init__(dmg=10)


class Tower2(Tower):
    def __init__(self):
        super().__init__(dmg=20)


tower_list = [
    Tower1(),
    Tower2(),
    Tower2(),
    Tower1(),
    Tower2(),
]

for t in tower_list:
    print(t.dng)
