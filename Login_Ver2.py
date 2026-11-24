import tkinter as tk
from tkinter import messagebox
import os
import hashlib
import subprocess
import sys
#                    COLOR THEME
BG_COLOR = "#097BB0"
CARD_COLOR = "#4C86E3"
ACCENT_COLOR = "#59A4C5"
TEXT_COLOR = "#01080E"
SECONDARY_TEXT = "#05244F"
SUCCESS_COLOR = "#0C7834"
DANGER_COLOR = "#EF3939"
BUTTON_HOVER = "#7FC9EB"
MASTER_FILE = "master.hash"

MASTER_FILE = "master.hash"

def hash_master_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def setup_master_password(password):
    with open(MASTER_FILE, "w") as file:
        file.write(hash_master_password(password))


def verify_master_password(password):
    if not os.path.exists(MASTER_FILE):
        return False

    with open(MASTER_FILE, "r") as file:
        stored_hash = file.read().strip()

    return hash_master_password(password) == stored_hash


#                    LOGIN FUNCTION
def login():
    username = entry_user.get().strip()
    password = entry_pass.get()

    if not password:
        messagebox.showwarning(
            "Missing Password",
            "Please enter your master password."
        )
        return

    if not os.path.exists(MASTER_FILE):
        setup_master_password(password)

        messagebox.showinfo(
            "Master Password Created",
            "Your master password has been created successfully!"
        )

        open_dashboard()
        return

    if verify_master_password(password):
        messagebox.showinfo(
            "Login Successful",
            "Welcome to Smart Password Manager!"
        )

        open_dashboard()
    else:
        messagebox.showerror(
            "Login Failed",
            "Incorrect master password."
        )



def open_dashboard():

    dashboard_path = os.path.join(
        os.path.dirname(__file__),
        "Login_Dashboard_Ver2.py"
    )

    subprocess.Popen(
        [sys.executable, dashboard_path]
    )

    root.destroy()

#                    SHOW / HIDE PASSWORD

def toggle_password():

    if entry_pass.cget("show") == "*":

        entry_pass.config(show="")

        show_button.config(
            text="Hide"
        )

    else:

        entry_pass.config(show="*")

        show_button.config(
            text="Show"
        )

#                    CLEAR LOGIN
def clear_fields():

    entry_user.delete(
        0,
        tk.END
    )

    entry_pass.delete(
        0,
        tk.END
    )

    entry_user.focus()

#                    MAIN WINDOW
root = tk.Tk()

root.title(
    "Smart Password Manager - Login"
)

root.geometry(
    "1100x700"
)

root.minsize(
    900,
    600
)

root.configure(
    bg=BG_COLOR
)

#                    CENTER WINDOW
def center_window():

    root.update_idletasks()

    width = root.winfo_width()
    height = root.winfo_height()

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    root.geometry(
        f"{width}x{height}+{x}+{y}"
    )


center_window()

#                    MAIN CONTAINER
main_frame = tk.Frame(
    root,
    bg=BG_COLOR
)

main_frame.pack(
    fill="both",
    expand=True
)

#                    LEFT INFORMATION PANEL
left_panel = tk.Frame(
    main_frame,
    bg=BG_COLOR,
    width=550
)

left_panel.pack(
    side="left",
    fill="both",
    expand=True
)

left_panel.pack_propagate(False)
# Security icon
security_icon = tk.Label(
    left_panel,
    text="🔐",
    font=("Segoe UI Emoji", 70),
    bg=BG_COLOR,
    fg=ACCENT_COLOR
)

security_icon.pack(
    pady=(100, 20)
)


# Main title
title = tk.Label(
    left_panel,
    text="SMART\nPASSWORD MANAGER",
    font=("Segoe UI", 30, "bold"),
    bg=BG_COLOR,
    fg=TEXT_COLOR,
    justify="center"
)

title.pack()

# Subtitle
subtitle = tk.Label(
    left_panel,
    text="Your secure digital password vault",
    font=("Segoe UI", 14),
    bg=BG_COLOR,
    fg=SECONDARY_TEXT
)

subtitle.pack(
    pady=15
)

# Security description
description = tk.Label(
    left_panel,
    text=(
        "Protect your passwords with secure encryption\n"
        "and manage your digital credentials in one place."
    ),
    font=("Segoe UI", 11),
    bg=BG_COLOR,
    fg=SECONDARY_TEXT,
    justify="center"
)

description.pack(
    pady=10
)


# Security features
features = tk.Frame(
    left_panel,
    bg=BG_COLOR
)

features.pack(
    pady=25
)


feature1 = tk.Label(
    features,
    text="🔒  Encrypted Storage",
    font=("Segoe UI", 11, "bold"),
    bg=BG_COLOR,
    fg=TEXT_COLOR
)

feature1.pack(
    pady=5
)


feature2 = tk.Label(
    features,
    text="🛡  Secure Password Generation",
    font=("Segoe UI", 11, "bold"),
    bg=BG_COLOR,
    fg=TEXT_COLOR
)

feature2.pack(
    pady=5
)


feature3 = tk.Label(
    features,
    text="📊  Password Strength Analysis",
    font=("Segoe UI", 11, "bold"),
    bg=BG_COLOR,
    fg=TEXT_COLOR
)

feature3.pack(
    pady=5
)
#                    RIGHT LOGIN PANEL

right_panel = tk.Frame(
    main_frame,
    bg=CARD_COLOR,
    width=500
)

right_panel.pack(
    side="right",
    fill="both",
    expand=True,
    padx=60,
    pady=60
)

right_panel.pack_propagate(False)


# Login title
login_title = tk.Label(
    right_panel,
    text="Welcome Back",
    font=("Segoe UI", 26, "bold"),
    bg=CARD_COLOR,
    fg=TEXT_COLOR
)

login_title.pack(
    pady=(70, 5)
)


login_subtitle = tk.Label(
    right_panel,
    text="Sign in to access your password vault",
    font=("Segoe UI", 10),
    bg=CARD_COLOR,
    fg=SECONDARY_TEXT
)

login_subtitle.pack(
    pady=(0, 35)
)
#                    USERNAME
user_label = tk.Label(
    right_panel,
    text="Username",
    font=("Segoe UI", 11, "bold"),
    bg=CARD_COLOR,
    fg=TEXT_COLOR
)

user_label.pack(
    anchor="w",
    padx=60
)

entry_user = tk.Entry(
    right_panel,
    font=("Segoe UI", 13),
    bg="#334155",
    fg=TEXT_COLOR,
    insertbackground=TEXT_COLOR,
    relief="flat",
    bd=0
)

entry_user.pack(
    fill="x",
    padx=60,
    ipady=12,
    pady=(8, 20)
)

#                    PASSWORD
pass_label = tk.Label(
    right_panel,
    text="Password",
    font=("Segoe UI", 11, "bold"),
    bg=CARD_COLOR,
    fg=TEXT_COLOR
)

pass_label.pack(
    anchor="w",
    padx=60
)


# Password container
password_frame = tk.Frame(
    right_panel,
    bg="#334155"
)

password_frame.pack(
    fill="x",
    padx=60,
    pady=(8, 30)
)


entry_pass = tk.Entry(
    password_frame,
    font=("Segoe UI", 13),
    bg="#334155",
    fg=TEXT_COLOR,
    insertbackground=TEXT_COLOR,
    show="*",
    relief="flat",
    bd=0
)

entry_pass.pack(
    side="left",
    fill="x",
    expand=True,
    ipady=12,
    padx=(10, 0)
)


show_button = tk.Button(
    password_frame,
    text="Show",
    font=("Segoe UI", 9, "bold"),
    bg="#334155",
    fg=ACCENT_COLOR,
    activebackground="#334155",
    activeforeground=ACCENT_COLOR,
    relief="flat",
    bd=0,
    cursor="hand2",
    command=toggle_password
)

show_button.pack(
    side="right",
    padx=10
)

#                    LOGIN BUTTON
login_button = tk.Button(
    right_panel,
    text="LOGIN",
    font=("Segoe UI", 12, "bold"),
    bg=ACCENT_COLOR,
    fg="#0F172A",
    activebackground=BUTTON_HOVER,
    activeforeground="white",
    relief="flat",
    bd=0,
    cursor="hand2",
    command=login
)

login_button.pack(
    fill="x",
    padx=60,
    ipady=13
)

#                    CLEAR BUTTON


clear_button = tk.Button(
    right_panel,
    text="Clear",
    font=("Segoe UI", 10),
    bg=CARD_COLOR,
    fg=SECONDARY_TEXT,
    activebackground=CARD_COLOR,
    activeforeground=TEXT_COLOR,
    relief="flat",
    bd=0,
    cursor="hand2",
    command=clear_fields
)

clear_button.pack(
    pady=12
)

#                    SECURITY STATUS
security_status = tk.Label(
    right_panel,
    text="●  Secure Login System",
    font=("Segoe UI", 10, "bold"),
    bg=CARD_COLOR,
    fg=SUCCESS_COLOR
)

security_status.pack(
    pady=(25, 5)
)


security_info = tk.Label(
    right_panel,
    text="Your credentials are protected.",
    font=("Segoe UI", 9),
    bg=CARD_COLOR,
    fg=SECONDARY_TEXT
)

security_info.pack()

#                    ENTER KEY LOGIN

root.bind(
    "<Return>",
    lambda event: login()
)


# Automatically place cursor in username field
entry_user.focus()

#                    START APPLICATION
root.mainloop()

