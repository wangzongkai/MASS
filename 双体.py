import tkinter as tk
from tkinter import ttk
import math
import numpy as np

running = False  # 运行状态标志


def shuangti(u0, course0, r0, f1, f2, dt):
    M = 500  # 质量
    L = 2  # 船体长度
    du = (f1 + f2) / (2 * M)
    dr = (f1 - f2) / (M * L)
    r = r0 + dr * dt
    course = course0 + r * dt + 0.5 * dr * dt ** 2  # 角度更新
    u = u0 + dt * du
    return u, course, r


def get_xy(x, y, f1, f2, u0, course0, r0, dt):
    u0, course0, r0 = shuangti(u0, course0, r0, f1, f2, dt)
    x = x + u0 * np.sin(course0) * dt
    y = y + u0 * np.cos(course0) * dt
    return x, y, u0, course0, r0


class Ship:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.angle = 0

        # 创建双体船的两个细长椭圆和连接线
        self.body1 = canvas.create_oval(x - 10, y - 3, x + 10, y + 3, fill="blue")
        self.body2 = canvas.create_oval(x +30, y - 3, x + 50, y +3, fill="blue")
        self.link = canvas.create_line(x + 10, y, x + 30, y, fill="black", width=2)

    def update(self, x, y, angle):
        self.x = 400 + x * 10
        self.y = 300 - y * 10
        self.angle = angle

        # 更新椭圆和连接线
        self.canvas.coords(self.body1, self.x - 10, self.y - 3, self.x + 10, self.y + 3)
        self.canvas.coords(self.body2, self.x + 30, self.y - 3, self.x + 50, self.y + 3)
        self.canvas.coords(self.link, self.x + 10, self.y, self.x + 30, self.y)


def update_ship():
    global running, x, y, u0, course0, r0, f1, f2, dt
    if running:
        x, y, u0, course0, r0 = get_xy(x, y, f1, f2, u0, course0, r0, dt)
        ship.update(x, y, math.degrees(course0))
        root.after(int(dt * 1000), update_ship)


def toggle_simulation():
    global running
    running = not running
    if running:
        update_ship()


def update_parameters():
    global x, y, u0, course0, r0, f1, f2, dt
    try:
        f1 = float(f1_entry.get())
        f2 = float(f2_entry.get())
        u0 = float(u0_entry.get())
        course0 = float(course0_entry.get())
        r0 = float(r0_entry.get())
        dt = float(dt_entry.get())
        x, y = 0, 0
    except ValueError:
        pass


root = tk.Tk()
root.title("船舶运动仿真")
canvas = tk.Canvas(root, width=800, height=600, bg="white")
canvas.pack()

# x, y, u0, course0, r0 = 0, 0, 0, 0, 0
# f1, f2 = 22, 22
# dt = 0.05

ship = Ship(canvas, 400, 300)
control_frame = ttk.LabelFrame(root, text="控制面板", padding=10)
control_frame.pack(side=tk.RIGHT, fill=tk.Y)

ttk.Label(control_frame, text="f1 (N):").grid(row=0, column=0, sticky=tk.W)
f1_entry = ttk.Entry(control_frame)
f1_entry.grid(row=0, column=1)
f1_entry.insert(0, "22")

ttk.Label(control_frame, text="f2 (N):").grid(row=1, column=0, sticky=tk.W)
f2_entry = ttk.Entry(control_frame)
f2_entry.grid(row=1, column=1)
f2_entry.insert(0, "22")

ttk.Label(control_frame, text="u0 (m/s):").grid(row=2, column=0, sticky=tk.W)
u0_entry = ttk.Entry(control_frame)
u0_entry.grid(row=2, column=1)
u0_entry.insert(0, "0")

ttk.Label(control_frame, text="course0 (rad):").grid(row=3, column=0, sticky=tk.W)
course0_entry = ttk.Entry(control_frame)
course0_entry.grid(row=3, column=1)
course0_entry.insert(0, "0")

ttk.Label(control_frame, text="r0 (rad/s):").grid(row=4, column=0, sticky=tk.W)
r0_entry = ttk.Entry(control_frame)
r0_entry.grid(row=4, column=1)
r0_entry.insert(0, "0")

ttk.Label(control_frame, text="dt (s):").grid(row=5, column=0, sticky=tk.W)
dt_entry = ttk.Entry(control_frame)
dt_entry.grid(row=5, column=1)
dt_entry.insert(0, "0.05")

update_button = ttk.Button(control_frame, text="更新参数", command=update_parameters)
update_button.grid(row=6, column=0, columnspan=2)

start_button = ttk.Button(control_frame, text="启动/暂停", command=toggle_simulation)
start_button.grid(row=7, column=0, columnspan=2)

root.mainloop()
