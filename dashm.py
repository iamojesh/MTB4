import tkinter as tk
from tkinter import font, messagebox
import time
from datetime import datetime
import subprocess
import sys

LOG_FILE = "akash_mtb_dashm.txt"

# ================= LOGGING =================
def write_log(event):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}] {event}\n")

write_log("Application Started")

# ================= FUNCTIONS =================
def button_hover(e):
    e.widget['background'] = e.widget.hover_color

def button_leave(e):
    e.widget['background'] = e.widget.original_color

def button_click(name):
    write_log(f"Button Clicked: {name}")

    if name == "START PDU CHECKS":
        write_log("Opening PDU Manual")
        root.destroy()  # ✅ CLOSE DASHM FIRST
        subprocess.Popen([sys.executable, "pdum.py"])
    else:
        messagebox.showinfo("Operation", f"{name} executed")

def exit_app():
    if messagebox.askyesno("Exit Confirmation", "Are you sure you want to exit?"):
        write_log("Application Exited")
        root.destroy()

def update_clock():
    clock_label.config(text=time.strftime("%d %B %Y | %H:%M:%S"))
    clock_label.after(1000, update_clock)

# ================= WINDOW =================
root = tk.Tk()
root.title("AKASH MTB CHECKOUT – COMMAND CENTER")
root.geometry("900x720")
root.configure(bg="#0a192f")
root.resizable(True, True)

# ================= FONTS =================
title_font = font.Font(family="Segoe UI", size=32, weight="bold")
subtitle_font = font.Font(family="Segoe UI", size=16, weight="bold")
button_font = font.Font(family="Segoe UI", size=12, weight="bold")
clock_font = font.Font(family="Consolas", size=11)

# ================= HEADER =================
tk.Label(
    root,
    text="AKASH MTB CHECKOUT",
    font=title_font,
    bg="#0a192f",
    fg="#00e5ff",
    pady=20
).pack()

tk.Label(
    root,
    text="WELCOME TO MANUAL MODE",
    font=subtitle_font,
    bg="#0a192f",
    fg="#00ff9c"
).pack(pady=(0, 25))

# ================= BUTTONS =================
button_data = [
    ("START PDU CHECKS", "#1f4068", "#4ecca3"),
    ("START SPU CHECKS", "#1b6ca8", "#00bcd4"),
    ("START SCU/ACTUATOR CHECKS", "#4b7bec", "#a5b1ff"),
    ("START CGU CHECKS", "#6d214f", "#ff6f91"),
    ("START RPF CHECKS", "#3c6382", "#60a3bc"),
    ("START PYRO CHECKS", "#b33939", "#ff5252")
]

for text, color, hover in button_data:
    frame = tk.Frame(root, bg="#0a192f")
    frame.pack(pady=10)

    btn = tk.Button(
        frame,
        text=f"{text}  >>",
        font=button_font,
        bg=color,
        fg="white",
        width=32,
        height=2,
        cursor="hand2",
        command=lambda t=text: button_click(t)
    )
    btn.original_color = color
    btn.hover_color = hover
    btn.bind("<Enter>", button_hover)
    btn.bind("<Leave>", button_leave)
    btn.pack()

# ================= STATUS BAR =================
status = tk.Frame(root, bg="#020c1b", height=40)
status.pack(side=tk.BOTTOM, fill=tk.X)

tk.Label(
    status,
    text="System Status: READY | All subsystems nominal",
    font=clock_font,
    bg="#020c1b",
    fg="#00ff9c"
).pack(side=tk.LEFT, padx=20)

clock_label = tk.Label(
    status,
    font=clock_font,
    bg="#020c1b",
    fg="#8892b0"
)
clock_label.pack(side=tk.RIGHT, padx=20)
update_clock()

root.mainloop()
