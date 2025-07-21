import customtkinter as ctk
import requests
from tkinter import messagebox

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

BASE_URL = "http://127.0.0.1:8000"

def get_token():
    try:
        with open("token.txt", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return None

class LoginScreen(ctk.CTkFrame):
    def __init__(self, master, switch_to_dashboard):
        super().__init__(master)
        self.master = master
        self.switch_to_dashboard = switch_to_dashboard

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username")
        self.username_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=10)

        login_button = ctk.CTkButton(self, text="Login", command=self.login)
        login_button.pack(pady=20)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if not username or not password:
            messagebox.showerror("Error", "Fill all fields")
            return

        response = requests.post(f"{BASE_URL}/login", data={"username": username, "password": password})
        if response.status_code == 200:
            token = response.json()["access_token"]
            with open("token.txt", "w") as file:
                file.write(token)
            self.switch_to_dashboard()
        else:
            messagebox.showerror("Login Failed", response.json().get("detail", "Unknown error"))

class Dashboard(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        ctk.CTkLabel(self, text="Dashboard", font=("Arial", 20)).pack(pady=10)

        ctk.CTkButton(self, text="Create Habit", command=self.create_habit).pack(pady=5)
        ctk.CTkButton(self, text="View Habits", command=self.view_habits).pack(pady=5)
        ctk.CTkButton(self, text="Update Habit", command=self.update_habit).pack(pady=5)
        ctk.CTkButton(self, text="Delete Habit", command=self.delete_habit).pack(pady=5)
        ctk.CTkButton(self, text="Logout", command=self.logout).pack(pady=20)

    def create_habit(self):
        token = get_token()
        if not token:
            return messagebox.showerror("Error", "Login first")

        def submit():
            data = {
                "name": name.get(),
                "description": desc.get(),
                "category": cat.get(),
                "target_per_day": int(target.get())
            }
            response = requests.post(f"{BASE_URL}/habits/", json=data, headers={"Authorization": f"Bearer {token}"})
            messagebox.showinfo("Status", response.text)
            window.destroy()

        window = ctk.CTkToplevel(self)
        name = ctk.CTkEntry(window, placeholder_text="Name")
        desc = ctk.CTkEntry(window, placeholder_text="Description")
        cat = ctk.CTkEntry(window, placeholder_text="Category")
        target = ctk.CTkEntry(window, placeholder_text="Target Per Day")
        for widget in [name, desc, cat, target]: widget.pack(pady=5)
        ctk.CTkButton(window, text="Submit", command=submit).pack(pady=10)

    def view_habits(self):
        token = get_token()
        if not token:
            return messagebox.showerror("Error", "Login first")
        response = requests.get(f"{BASE_URL}/habits/", headers={"Authorization": f"Bearer {token}"})
        window = ctk.CTkToplevel(self)
        if response.status_code == 200:
            habits = response.json()
            for habit in habits:
                ctk.CTkLabel(window, text=f"{habit['id']}: {habit['name']} - {habit['category']} ({habit['target_per_day']})").pack()
        else:
            messagebox.showerror("Error", response.text)

    def update_habit(self):
        token = get_token()
        if not token:
            return messagebox.showerror("Error", "Login first")

        def submit():
            habit_id = id_entry.get()
            data = {
                "name": name.get(),
                "description": desc.get(),
                "category": cat.get(),
                "target_per_day": int(target.get())
            }
            response = requests.put(f"{BASE_URL}/habits/{habit_id}", json=data, headers={"Authorization": f"Bearer {token}"})
            messagebox.showinfo("Status", response.text)
            window.destroy()

        window = ctk.CTkToplevel(self)
        id_entry = ctk.CTkEntry(window, placeholder_text="Habit ID")
        name = ctk.CTkEntry(window, placeholder_text="New Name")
        desc = ctk.CTkEntry(window, placeholder_text="New Description")
        cat = ctk.CTkEntry(window, placeholder_text="New Category")
        target = ctk.CTkEntry(window, placeholder_text="New Target")
        for widget in [id_entry, name, desc, cat, target]: widget.pack(pady=5)
        ctk.CTkButton(window, text="Update", command=submit).pack(pady=10)

    def delete_habit(self):
        token = get_token()
        if not token:
            return messagebox.showerror("Error", "Login first")

        def submit():
            habit_id = id_entry.get()
            response = requests.delete(f"{BASE_URL}/habits/{habit_id}", headers={"Authorization": f"Bearer {token}"})
            messagebox.showinfo("Status", response.text)
            window.destroy()

        window = ctk.CTkToplevel(self)
        id_entry = ctk.CTkEntry(window, placeholder_text="Habit ID to delete")
        id_entry.pack(pady=10)
        ctk.CTkButton(window, text="Delete", command=submit).pack(pady=10)

    def logout(self):
        with open("token.txt", "w") as file:
            file.write("")
        self.master.show_login()

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("500x500")
        self.title("Habit Tracker")
        self.login_screen = LoginScreen(self, self.show_dashboard)
        self.dashboard = Dashboard(self)
        self.show_login()

    def show_login(self):
        self.dashboard.pack_forget()
        self.login_screen.pack(fill="both", expand=True)

    def show_dashboard(self):
        self.login_screen.pack_forget()
        self.dashboard.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = App()
    app.mainloop()
