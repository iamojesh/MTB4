import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import os
import subprocess

# ================= WINDOW =================
root = tk.Tk()
root.title("AKASH MTB CHECKOUT")
root.geometry("1000x600")
root.resizable(False, False)

# ================= THEME =================
theme = {
    "left_bg": "#a8c5b8",
    "right_bg": "#fafafa",
    "card_bg": "#ffffff",
    "fg": "#2c3e50",
    "fg_light": "#7f8c8d",
    "label_text": "#4a5568",
    "entry_bg": "#ffffff",
    "entry_border": "#d0d0d0",
    "entry_focus": "#2a4bd7",
    "button_bg": "#2a4bd7",
    "button_hover": "#1e3ba8",
    "button_fg": "#ffffff",
    "accent": "#2a4bd7"
}

# ================= FUNCTIONS =================
def on_entry_focus_in(event, entry):
    if entry == username_entry:
        username_border.configure(bg=theme["entry_focus"])
    else:
        password_border.configure(bg=theme["entry_focus"])

def on_entry_focus_out(event, entry):
    if entry == username_entry:
        username_border.configure(bg=theme["entry_border"])
    else:
        password_border.configure(bg=theme["entry_border"])

def on_button_enter(event):
    login_btn.configure(bg=theme["button_hover"])

def on_button_leave(event):
    login_btn.configure(bg=theme["button_bg"])

def toggle_password():
    if password_entry.cget("show") == "":
        password_entry.config(show="*")
        show_btn.config(text="Show")
    else:
        password_entry.config(show="")
        show_btn.config(text="Hide")

def write_log(status, username, user_type):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("login_logs.txt", "a") as f:
        f.write(f"{timestamp} | {status:<7} | Type: {user_type:<8} | Username: {username}\n")

def check_operator_credentials(username, password):
    """Check if credentials exist in operators.txt"""
    try:
        if os.path.exists("operators.txt"):
            with open("operators.txt", "r") as file:
                for line in file:
                    line = line.strip()
                    if line and "," in line:
                        u, p = line.split(",", 1)
                        if username == u.strip() and password == p.strip():
                            return True
    except Exception as e:
        messagebox.showerror("Error", f"Error reading operators file: {str(e)}")
    return False

def check_manual_credentials(username, password):
    """Check if credentials exist in manual_users.txt"""
    try:
        if os.path.exists("manual_users.txt"):
            with open("manual_users.txt", "r") as file:
                for line in file:
                    line = line.strip()
                    if line and "," in line:
                        u, p = line.split(",", 1)
                        if username == u.strip() and password == p.strip():
                            return True
    except Exception as e:
        messagebox.showerror("Error", f"Error reading manual users file: {str(e)}")
    return False

def validate_login():
    username = username_entry.get().strip()
    password = password_entry.get().strip()

    if not username or not password:
        messagebox.showwarning("Required", "Please enter both username and password")
        return

    # Check operator credentials first
    if check_operator_credentials(username, password):
        write_log("SUCCESS", username, "OPERATOR")
        messagebox.showinfo("Success", f"Welcome, Operator {username}!")
        root.destroy()
        subprocess.Popen(["python", "dasho.py"])
        return

    # Check manual user credentials
    if check_manual_credentials(username, password):
        write_log("SUCCESS", username, "MANUAL")
        messagebox.showinfo("Success", f"Welcome, Manual User {username}!")
        root.destroy()
        subprocess.Popen(["python", "dashm.py"])
        return

    # If credentials not found in either file
    write_log("FAILED", username, "UNKNOWN")
    messagebox.showerror("Failed", "Invalid username or password")

def on_enter_key(event):
    validate_login()

# ================= MAIN CONTAINER =================
container = tk.Frame(root, bg="#ffffff")
container.pack(fill="both", expand=True)

# ================= LEFT PANEL =================
left_panel = tk.Frame(container, bg=theme["left_bg"], width=450)
left_panel.pack(side="left", fill="both", expand=False)
left_panel.pack_propagate(False)

left_content = tk.Frame(left_panel, bg=theme["left_bg"])
left_content.place(relx=0.5, rely=0.5, anchor="center")

# DRDO Logo (adjust path if needed)
try:
    drdo_logo = tk.PhotoImage(file=r"C:\Users\mojes\Downloads\drdo_converted.png")
    drdo_logo = drdo_logo.subsample(2, 2)
    logo_label = tk.Label(left_content, image=drdo_logo, bg=theme["left_bg"])
    logo_label.pack(pady=(0, 30))
    root.drdo_logo = drdo_logo
except:
    deco_frame = tk.Frame(left_content, bg="#ffffff", width=200, height=200)
    deco_frame.pack(pady=(0, 30))
    deco_frame.pack_propagate(False)
    tk.Label(deco_frame, text="AKASH MTB CHECKOUT", font=("Segoe UI", 36, "bold"),
             bg="#ffffff", fg=theme["accent"]).place(relx=0.5, rely=0.5, anchor="center")

tk.Label(left_content, text="Secure Access Portal",
         font=("Segoe UI", 18, "bold"), bg=theme["left_bg"], fg="#ffffff").pack(pady=(0, 15))

tk.Label(left_content, text="Defence Research and Development Organisation\nAuthentication System",
         font=("Segoe UI", 11), bg=theme["left_bg"], fg="#ffffff", justify="center").pack()

dots_frame = tk.Frame(left_content, bg=theme["left_bg"])
dots_frame.pack(pady=(40, 0))
for i in range(4):
    color = "#ffffff" if i == 0 else "#b8d4c4"
    tk.Label(dots_frame, text="●", font=("Arial", 8), bg=theme["left_bg"], fg=color).pack(side="left", padx=3)

# ================= RIGHT PANEL (Login Form) =================
right_panel = tk.Frame(container, bg=theme["right_bg"])
right_panel.pack(side="right", fill="both", expand=True)

form_container = tk.Frame(right_panel, bg=theme["right_bg"])
form_container.place(relx=0.5, rely=0.5, anchor="center", width=380)

tk.Label(form_container, text="AKASH MTB CHECKOUT", font=("Brush Script MT", 23),
         bg=theme["right_bg"], fg=theme["fg"]).pack(pady=(0, 40))

tk.Label(form_container, text="WELCOME",
         font=("Segoe UI", 14), bg=theme["right_bg"], fg=theme["fg"]).pack(pady=(0, 40))

# Username
tk.Label(form_container, text="Username ", font=("Segoe UI", 10, "bold"),
         bg=theme["right_bg"], fg=theme["entry_focus"]).pack(anchor="w", pady=(0, 8))

username_border = tk.Frame(form_container, bg=theme["entry_border"], height=45)
username_border.pack(fill="x", pady=(0, 20))
username_border.pack_propagate(False)

username_inner = tk.Frame(username_border, bg=theme["entry_bg"])
username_inner.pack(fill="both", expand=True, padx=2, pady=2)

username_entry = tk.Entry(username_inner, font=("Segoe UI", 11),
                          bg=theme["entry_bg"], fg=theme["fg"], relief="flat", bd=0)
username_entry.pack(fill="both", expand=True, padx=15, pady=10)
username_entry.bind("<FocusIn>", lambda e: on_entry_focus_in(e, username_entry))
username_entry.bind("<FocusOut>", lambda e: on_entry_focus_out(e, username_entry))
username_entry.bind("<Return>", on_enter_key)

# Password
tk.Label(form_container, text="Password", font=("Segoe UI", 10, "bold"),
         bg=theme["right_bg"], fg=theme["entry_focus"]).pack(anchor="w", pady=(0, 8))

password_border = tk.Frame(form_container, bg=theme["entry_border"], height=45)
password_border.pack(fill="x", pady=(0, 10))
password_border.pack_propagate(False)

password_inner = tk.Frame(password_border, bg=theme["entry_bg"])
password_inner.pack(fill="both", expand=True, padx=2, pady=2)

password_container = tk.Frame(password_inner, bg=theme["entry_bg"])
password_container.pack(fill="both", expand=True, padx=15, pady=10)

password_entry = tk.Entry(password_container, font=("Segoe UI", 11), show="*",
                          bg=theme["entry_bg"], fg=theme["fg"], relief="flat", bd=0)
password_entry.pack(side="left", fill="both", expand=True)
password_entry.bind("<FocusIn>", lambda e: on_entry_focus_in(e, password_entry))
password_entry.bind("<FocusOut>", lambda e: on_entry_focus_out(e, password_entry))
password_entry.bind("<Return>", on_enter_key)

show_btn = tk.Button(password_container, text="Show", font=("Segoe UI", 9, "bold"),
                     command=toggle_password, relief="flat", bd=0, cursor="hand2",
                     bg=theme["entry_bg"], fg=theme["entry_focus"],
                     activebackground=theme["entry_bg"], activeforeground=theme["button_hover"])
show_btn.pack(side="right", padx=10)

# Login Button
login_btn = tk.Button(form_container, text="LOG IN", font=("Segoe UI", 11, "bold"),
                      bg=theme["button_bg"], fg=theme["button_fg"],
                      relief="flat", cursor="hand2", command=validate_login)
login_btn.pack(fill="x", ipady=12, pady=(20, 20))
login_btn.bind("<Enter>", on_button_enter)
login_btn.bind("<Leave>", on_button_leave)

# Footer (simplified)
tk.Label(form_container, text="New to DRDO Portal? Contact Administrator",
         font=("Segoe UI", 9), bg=theme["right_bg"], fg=theme["fg_light"]).pack()

username_entry.focus()

root.mainloop()
