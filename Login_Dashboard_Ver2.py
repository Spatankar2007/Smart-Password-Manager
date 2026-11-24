import tkinter as tk
from tkinter import messagebox
import menu_integrationVer2

#                    COLOR THEME
BG_COLOR = "#8EB4E5"
SIDEBAR_COLOR = "#1E5CB9"
CARD_COLOR = "#FFFFFF"
ACCENT_COLOR = "#000612"
TEXT_COLOR = "#1E293B"
SECONDARY_TEXT = "#5C7291"
SUCCESS_COLOR = "#099B3E"
DANGER_COLOR = "#DC1818"
BUTTON_HOVER = "#1145D5"

#                    MAIN WINDOW
root = tk.Tk()

root.title("Smart Password Manager")

# Large window
root.geometry("1200x700")

# Minimum size
root.minsize(1000, 600)

# Background
root.configure(bg=BG_COLOR)

#                    WINDOW CENTERING

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

#                    BUTTON FUNCTIONS

def add_password():

    add_window = tk.Toplevel(root)
    add_window.title("Add Password")
    add_window.geometry("500x450")
    add_window.configure(bg=BG_COLOR)

    tk.Label(
        add_window,
        text="Add New Password",
        font=("Arial", 22, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(pady=20)

    tk.Label(
        add_window,
        text="Account Name",
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack()

    account_entry = tk.Entry(
        add_window,
        width=40
    )
    account_entry.pack(pady=5)

    tk.Label(
        add_window,
        text="Username / Email",
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(pady=(10, 0))

    username_entry = tk.Entry(
        add_window,
        width=40
    )
    username_entry.pack(pady=5)

    tk.Label(
        add_window,
        text="Password",
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(pady=(10, 0))

    password_entry = tk.Entry(
        add_window,
        width=40,
        show="*"
    )
    password_entry.pack(pady=5)

    def save_new_password():

        account = account_entry.get()
        username = username_entry.get()
        password = password_entry.get()

        success, result = menu_integrationVer2.save_password(
            account,
            username,
            password
        )

        if success:
            messagebox.showinfo(
                "Success",
                "Password saved successfully!"
            )
            add_window.destroy()

        else:
            messagebox.showerror(
                "Error",
                result
            )

    tk.Button(
        add_window,
        text="Save Password",
        command=save_new_password,
        width=20
    ).pack(pady=25)


def retrieve_password():

    vault_window = tk.Toplevel(root)
    vault_window.title("Password Vault")
    vault_window.geometry("600x500")
    vault_window.configure(bg=BG_COLOR)

    tk.Label(
        vault_window,
        text="Password Vault",
        font=("Arial", 22, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(pady=20)

    accounts = menu_integrationVer2.get_accounts()

    if not accounts:
        tk.Label(
            vault_window,
            text="No passwords saved yet.",
            font=("Arial", 13),
            bg=BG_COLOR,
            fg=TEXT_COLOR
        ).pack(pady=30)

        return

    tk.Label(
        vault_window,
        text="Select an account:",
        font=("Arial", 12),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(pady=10)

    account_var = tk.StringVar()
    account_var.set(accounts[0])

    account_menu = tk.OptionMenu(
        vault_window,
        account_var,
        *accounts
    )

    account_menu.config(
        width=30
    )

    account_menu.pack(pady=10)

    details_label = tk.Label(
        vault_window,
        text="",
        font=("Arial", 12),
        bg=BG_COLOR,
        fg=TEXT_COLOR,
        justify="left"
    )

    details_label.pack(pady=20)

    def view_password():

        account = account_var.get()

        success, result = menu_integrationVer2.get_password(
            account
        )

        if success:

            details_label.config(
                text=(
                    f"Account: {result['account']}\n\n"
                    f"Username: {result['username']}\n\n"
                    f"Password: {result['password']}"
                )
            )

        else:

            messagebox.showerror(
                "Error",
                result
            )

    tk.Button(
        vault_window,
        text="View Password",
        command=view_password,
        width=20
    ).pack(pady=15)


def generate_password():

    generator_window = tk.Toplevel(root)
    generator_window.title("Password Generator")
    generator_window.geometry("550x500")
    generator_window.configure(bg=BG_COLOR)

    tk.Label(
        generator_window,
        text="Password Generator",
        font=("Arial", 22, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(pady=20)

    tk.Label(
        generator_window,
        text="Password Length",
        font=("Arial", 12),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(pady=(10, 5))

    length_entry = tk.Entry(
        generator_window,
        width=15
    )
    length_entry.insert(0, "16")
    length_entry.pack()

    password_label = tk.Label(
        generator_window,
        text="",
        font=("Arial", 12),
        bg=BG_COLOR,
        fg=TEXT_COLOR,
        wraplength=450
    )
    password_label.pack(pady=25)

    strength_label = tk.Label(
        generator_window,
        text="",
        font=("Arial", 12),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    )
    strength_label.pack(pady=5)

    def create_password():

        try:
            length = int(length_entry.get())

            if length < 4:
                messagebox.showwarning(
                    "Invalid Length",
                    "Password length must be at least 4."
                )
                return

        except ValueError:
            messagebox.showwarning(
                "Invalid Length",
                "Please enter a valid number."
            )
            return

        password = menu_integrationVer2.generate_password(
            length
        )

        if password is None:
            messagebox.showerror(
                "Error",
                "Unable to generate password."
            )
            return

        password_label.config(
            text=f"Generated Password:\n{password}"
        )

        score = menu_integrationVer2.check_strength(
            password
        )

        strength_label.config(
            text=f"Strength Score: {score}/100"
        )

    tk.Button(
        generator_window,
        text="Generate Password",
        command=create_password,
        width=22
    ).pack(pady=15)


def check_strength():

    strength_window = tk.Toplevel(root)
    strength_window.title("Password Strength Analyzer")
    strength_window.geometry("550x450")
    strength_window.configure(bg=BG_COLOR)

    tk.Label(
        strength_window,
        text="Password Strength Analyzer",
        font=("Arial", 22, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(pady=25)

    tk.Label(
        strength_window,
        text="Enter a password to check:",
        font=("Arial", 12),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(pady=10)

    password_entry = tk.Entry(
        strength_window,
        width=40,
        show="*"
    )
    password_entry.pack(pady=5)

    result_label = tk.Label(
        strength_window,
        text="",
        font=("Arial", 14, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    )
    result_label.pack(pady=25)

    def analyze_password():

        password = password_entry.get()

        if not password:
            messagebox.showwarning(
                "Missing Password",
                "Please enter a password."
            )
            return

        score = menu_integrationVer2.check_strength(
            password
        )

        if score >= 80:
            level = "VERY STRONG"
        elif score >= 60:
            level = "STRONG"
        elif score >= 40:
            level = "MODERATE"
        else:
            level = "WEAK"

        result_label.config(
            text=f"Score: {score}/100\n\nStrength: {level}"
        )

    tk.Button(
        strength_window,
        text="Analyze Password",
        command=analyze_password,
        width=22
    ).pack(pady=10)


def activity_log():

    log_window = tk.Toplevel(root)
    log_window.title("Activity Log")
    log_window.geometry("700x500")
    log_window.configure(bg=BG_COLOR)

    tk.Label(
        log_window,
        text="Activity Log",
        font=("Arial", 22, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(pady=20)

    log_frame = tk.Frame(
        log_window,
        bg=BG_COLOR
    )
    log_frame.pack(
        fill="both",
        expand=True,
        padx=25,
        pady=10
    )

    scrollbar = tk.Scrollbar(log_frame)
    scrollbar.pack(
        side="right",
        fill="y"
    )

    log_text = tk.Text(
        log_frame,
        width=70,
        height=20,
        font=("Consolas", 11),
        yscrollcommand=scrollbar.set
    )

    log_text.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.config(
        command=log_text.yview
    )

    logs = menu_integrationVer2.get_activity_log()

    if logs:

        for log in logs:
            log_text.insert(
                tk.END,
                log
            )

    else:

        log_text.insert(
            tk.END,
            "No activity recorded yet."
        )

    log_text.config(
        state="disabled"
    )
#                    UPDATE PASSWORD

def update_password():

    update_window = tk.Toplevel(root)
    update_window.title("Update Password")
    update_window.geometry("600x500")
    update_window.configure(bg=BG_COLOR)

    tk.Label(
        update_window,
        text="Update Password",
        font=("Arial", 22, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(pady=25)

    accounts = menu_integrationVer2.get_accounts()

    if not accounts:

        tk.Label(
            update_window,
            text="No saved accounts found.",
            font=("Arial", 13),
            bg=BG_COLOR,
            fg=TEXT_COLOR
        ).pack(pady=30)

        return

    tk.Label(
        update_window,
        text="Select Account",
        font=("Arial", 12),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(pady=10)

    account_var = tk.StringVar()
    account_var.set(accounts[0])

    account_menu = tk.OptionMenu(
        update_window,
        account_var,
        *accounts
    )

    account_menu.config(
        width=30
    )

    account_menu.pack(pady=10)

    tk.Label(
        update_window,
        text="Enter New Password",
        font=("Arial", 12),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(pady=(20, 5))

    password_entry = tk.Entry(
        update_window,
        width=35,
        show="*"
    )

    password_entry.pack(pady=5)

    result_label = tk.Label(
        update_window,
        text="",
        font=("Arial", 12),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    )

    result_label.pack(pady=20)

    def update_now():

        account = account_var.get()
        new_password = password_entry.get()

        if not new_password:

            messagebox.showwarning(
                "Missing Password",
                "Please enter a new password."
            )

            return

        success, result = menu_integrationVer2.update_saved_password(
            account,
            new_password
        )

        if success:

            result_label.config(
                text=(
                    f"Password updated successfully!\n"
                    f"Strength Score: {result}/100"
                )
            )

            messagebox.showinfo(
                "Success",
                "Password updated successfully!"
            )

            password_entry.delete(
                0,
                tk.END
            )

        else:

            messagebox.showerror(
                "Error",
                result
            )

    tk.Button(
        update_window,
        text="Update Password",
        command=update_now,
        width=22
    ).pack(pady=15)

#                 SEARCH PASSWORDS

def search_passwords():

    search_window = tk.Toplevel(root)
    search_window.title("Search Passwords")
    search_window.geometry("650x500")
    search_window.configure(bg=BG_COLOR)

    tk.Label(
        search_window,
        text="Search Passwords",
        font=("Arial", 22, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(pady=25)

    tk.Label(
        search_window,
        text="Search by account or username/email",
        font=("Arial", 12),
        bg=BG_COLOR,
        fg=SECONDARY_TEXT
    ).pack(pady=5)

    search_entry = tk.Entry(
        search_window,
        width=40,
        font=("Arial", 12)
    )
    search_entry.pack(pady=10)

    result_list = tk.Listbox(
        search_window,
        width=55,
        height=12,
        font=("Arial", 11)
    )
    result_list.pack(pady=15)

    def perform_search():
    
        search_text = search_entry.get().strip()

        result_list.insert(tk.END, "SEARCH BUTTON CLICKED")

        result_list.delete(0, tk.END)


        if not search_text:
            result_list.insert(
            tk.END,
            "Please enter a username or account name."
             )
            return

        try:

            success, result = menu_integrationVer2.search_saved_passwords(
            search_text
        )

            if not success:
                result_list.insert(
                tk.END,
                result
                )
                return

            for item in result:
                result_list.insert(
                tk.END,
                f"{item['account']}  |  {item['username']}"
                )

        except Exception as e:

            result_list.insert(
            tk.END,
            f"Search error: {e}"
           )

    tk.Button(
        search_window,
        text="Search",
        command=perform_search,
        width=22
).pack(pady=10)
#                    DELETE PASSWORD

def delete_password():

    delete_window = tk.Toplevel(root)
    delete_window.title("Delete Password")
    delete_window.geometry("600x400")
    delete_window.configure(bg=BG_COLOR)

    tk.Label(
        delete_window,
        text="Delete Password",
        font=("Arial", 22, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(pady=25)

    accounts = menu_integrationVer2.get_accounts()

    if not accounts:

        tk.Label(
            delete_window,
            text="No saved accounts found.",
            font=("Arial", 13),
            bg=BG_COLOR,
            fg=TEXT_COLOR
        ).pack(pady=30)

        return

    tk.Label(
        delete_window,
        text="Select Account",
        font=("Arial", 12),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(pady=10)

    account_var = tk.StringVar()
    account_var.set(accounts[0])

    account_menu = tk.OptionMenu(
        delete_window,
        account_var,
        *accounts
    )

    account_menu.config(
        width=30
    )

    account_menu.pack(pady=15)

    def delete_now():

        account = account_var.get()

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete '{account}'?"
        )

        if not confirm:
            return

        success, result = menu_integrationVer2.delete_saved_password(
            account
        )

        if success:

            messagebox.showinfo(
                "Success",
                "Password deleted successfully!"
            )

            delete_window.destroy()

        else:

            messagebox.showerror(
                "Error",
                result
            )

    tk.Button(
        delete_window,
        text="Delete Password",
        command=delete_now,
        width=22
    ).pack(pady=25)
def logout():

    result = messagebox.askyesno(
        "Logout",
        "Are you sure you want to logout?"
    )

    if result:
        root.destroy()

#                    HOVER EFFECT
def on_enter(event):

    event.widget.configure(
        bg=BUTTON_HOVER
    )


def on_leave(event):

    event.widget.configure(
        bg=SIDEBAR_COLOR
    )
#                    HEADER
header = tk.Frame(
    root,
    bg=BG_COLOR,
    height=80
)
header.pack(
    side="top",
    fill="x"
)
header.pack_propagate(False)


# Logo / Title
title_frame = tk.Frame(
    header,
    bg=BG_COLOR
)

title_frame.pack(
    side="left",
    padx=30
)
title = tk.Label(
    title_frame,
    text="🔐  SMART PASSWORD MANAGER",
    font=("Segoe UI", 22, "bold"),
    bg=BG_COLOR,
    fg=TEXT_COLOR
)
title.pack(
    anchor="w"
)

subtitle = tk.Label(
    title_frame,
    text="Secure • Encrypted • Simple",
    font=("Segoe UI", 10),
    bg=BG_COLOR,
    fg=SECONDARY_TEXT
)
subtitle.pack(
    anchor="w"
)

# Security indicator
security_frame = tk.Frame(
    header,
    bg=BG_COLOR
)
security_frame.pack(
    side="right",
    padx=30
)
security_dot = tk.Label(
    security_frame,
    text="●",
    font=("Segoe UI", 16),
    bg=BG_COLOR,
    fg=SUCCESS_COLOR
)
security_dot.pack(
    side="left",
    padx=5
)
security_text = tk.Label(
    security_frame,
    text="SYSTEM SECURE",
    font=("Segoe UI", 11, "bold"),
    bg=BG_COLOR,
    fg=SUCCESS_COLOR
)
security_text.pack(
    side="left"
)
#                    SIDEBAR
sidebar = tk.Frame(
    root,
    bg=SIDEBAR_COLOR,
    width=250
)

sidebar.pack(
    side="left",
    fill="y"
)

sidebar.pack_propagate(False)
# Sidebar heading
menu_title = tk.Label(
    sidebar,
    text="MAIN MENU",
    font=("Segoe UI", 10, "bold"),
    bg=SIDEBAR_COLOR,
    fg=SECONDARY_TEXT
)

menu_title.pack(
    anchor="w",
    padx=25,
    pady=(30, 15)
)

#                    SIDEBAR BUTTON
def create_sidebar_button(
    text,
    command
):

    button = tk.Button(
        sidebar,
        text=text,
        font=("Segoe UI", 12, "bold"),
        bg=SIDEBAR_COLOR,
        fg=TEXT_COLOR,
        activebackground=BUTTON_HOVER,
        activeforeground="white",
        bd=0,
        relief="flat",
        anchor="w",
        padx=25,
        cursor="hand2",
        command=command
    )

    button.pack(
        fill="x",
        ipady=12
    )

    button.bind(
        "<Enter>",
        on_enter
    )

    button.bind(
        "<Leave>",
        on_leave
    )

    return button


create_sidebar_button(
    "🏠   Dashboard",
    lambda: None
)

create_sidebar_button(
    "🔑   Add Password",
    add_password
)

create_sidebar_button(
    "🔍   Password Vault",
    retrieve_password
)

create_sidebar_button(
    "⚙   Password Generator",
    generate_password
)

create_sidebar_button(
    "📊   Strength Analyzer",
    check_strength
)

create_sidebar_button(
    "📝   Activity Log",
    activity_log
)
create_sidebar_button(
    "🔄   Update Password",
    update_password
)
create_sidebar_button(
    "🗑️   Delete Password",
    delete_password
)
create_sidebar_button(
    "🔎   Search Passwords",
    search_passwords
)
# Logout button at bottom
logout_button = tk.Button(
    sidebar,
    text="🚪   Logout",
    font=("Segoe UI", 12, "bold"),
    bg=SIDEBAR_COLOR,
    fg=DANGER_COLOR,
    activebackground=DANGER_COLOR,
    activeforeground="white",
    bd=0,
    relief="flat",
    anchor="w",
    padx=25,
    cursor="hand2",
    command=logout
)

logout_button.pack(
    side="bottom",
    fill="x",
    ipady=12,
    pady=20
)
#                    MAIN CONTENT
content = tk.Frame(
    root,
    bg=BG_COLOR
)

content.pack(
    side="right",
    fill="both",
    expand=True
)

#                    WELCOME SECTION
welcome = tk.Frame(
    content,
    bg=BG_COLOR
)

welcome.pack(
    fill="x",
    padx=40,
    pady=(35, 20)
)

welcome_title = tk.Label(
    welcome,
    text="Welcome back! 👋",
    font=("Segoe UI", 26, "bold"),
    bg=BG_COLOR,
    fg=TEXT_COLOR
)

welcome_title.pack(
    anchor="w"
)

welcome_text = tk.Label(
    welcome,
    text=(
        "Manage your passwords securely from one place."
    ),
    font=("Segoe UI", 12),
    bg=BG_COLOR,
    fg=SECONDARY_TEXT
)

welcome_text.pack(
    anchor="w",
    pady=(5, 0)
)
#                    QUICK ACTIONS
section_title = tk.Label(
    content,
    text="Quick Actions",
    font=("Segoe UI", 15, "bold"),
    bg=BG_COLOR,
    fg=TEXT_COLOR
)

section_title.pack(
    anchor="w",
    padx=40,
    pady=(5, 15)
)


cards_frame = tk.Frame(
    content,
    bg=BG_COLOR
)

cards_frame.pack(
    fill="x",
    padx=40
)

#                    CARD CREATION
def create_card(
    parent,
    icon,
    title_text,
    description,
    command
):

    card = tk.Frame(
        parent,
        bg=CARD_COLOR,
        width=190,
        height=150,
        cursor="hand2"
    )

    card.pack(
        side="left",
        fill="both",
        expand=True,
        padx=8
    )

    card.pack_propagate(False)

    icon_label = tk.Label(
        card,
        text=icon,
        font=("Segoe UI Emoji", 28),
        bg=CARD_COLOR,
        fg=ACCENT_COLOR
    )

    icon_label.pack(
        pady=(18, 5)
    )

    title_label = tk.Label(
        card,
        text=title_text,
        font=("Segoe UI", 12, "bold"),
        bg=CARD_COLOR,
        fg=TEXT_COLOR
    )

    title_label.pack()

    description_label = tk.Label(
        card,
        text=description,
        font=("Segoe UI", 9),
        bg=CARD_COLOR,
        fg=SECONDARY_TEXT
    )

    description_label.pack(
        pady=5
    )

    # Make entire card clickable
    for widget in (
        card,
        icon_label,
        title_label,
        description_label
    ):

        widget.bind(
            "<Button-1>",
            lambda event: command()
        )

    return card


create_card(
    cards_frame,
    "🔑",
    "Add Password",
    "Save a new password",
    add_password
)

create_card(
    cards_frame,
    "🔐",
    "Password Vault",
    "View saved accounts",
    retrieve_password
)

create_card(
    cards_frame,
    "⚙",
    "Generate",
    "Create secure passwords",
    generate_password
)

create_card(
    cards_frame,
    "🛡",
    "Strength",
    "Analyze password security",
    check_strength
)

#                    SECURITY INFORMATION
info_title = tk.Label(
    content,
    text="Security Information",
    font=("Segoe UI", 15, "bold"),
    bg=BG_COLOR,
    fg=TEXT_COLOR
)

info_title.pack(
    anchor="w",
    padx=40,
    pady=(40, 15)
)


info_frame = tk.Frame(
    content,
    bg=CARD_COLOR
)

info_frame.pack(
    fill="x",
    padx=40
)

# Encryption information
encryption = tk.Label(
    info_frame,
    text="🔒  Encryption\nFernet Symmetric Encryption",
    font=("Segoe UI", 11, "bold"),
    bg=CARD_COLOR,
    fg=TEXT_COLOR,
    justify="left"
)

encryption.pack(
    side="left",
    expand=True,
    fill="x",
    padx=20,
    pady=20
)

# Storage information
storage = tk.Label(
    info_frame,
    text="💾  Storage\nEncrypted JSON Database",
    font=("Segoe UI", 11, "bold"),
    bg=CARD_COLOR,
    fg=TEXT_COLOR,
    justify="left"
)

storage.pack(
    side="left",
    expand=True,
    fill="x",
    padx=20,
    pady=20
)
# Password generator information
generator_info = tk.Label(
    info_frame,
    text="🛡  Generator\nCryptographically Secure",
    font=("Segoe UI", 11, "bold"),
    bg=CARD_COLOR,
    fg=TEXT_COLOR,
    justify="left"
)

generator_info.pack(
    side="left",
    expand=True,
    fill="x",
    padx=20,
    pady=20
)
#                    FOOTER
footer = tk.Label(
    content,
    text="Smart Password Manager  •  Secure your digital life",
    font=("Segoe UI", 9),
    bg=BG_COLOR,
    fg=SECONDARY_TEXT
)

footer.pack(
    side="bottom",
    pady=15
)

#                    START APPLICATION

root.mainloop()
