import tkinter as tk

root = tk.Tk()
root.title("Tower Defense - Main Menu")
root.geometry("800x600")

label = tk.Label(root, text="Hello, World!")
label.pack()

# สร้าง label1 ว่างไว้ก่อน
label1 = tk.Label(root, text="")
label1.pack()

sum = 0
click_count = 0

def on_click():
    global click_count
    click_count += 1
    
    label1.config(text=click_count)  # เปลี่ยนข้อความตรงนี้

button = tk.Button(root, text="Click me!", command=on_click)

button.pack()

root.mainloop()