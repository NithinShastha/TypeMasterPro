import tkinter as tk
import sqlite3

class TypeMasterPro:
    def __init__(self, root):
        self.root = root
        self.root.geometry("200x300")
        self.root.title("Type Master Pro")
        self.current_screen = None 
        self.create_user_db()

        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.firstName = tk.StringVar()
        self.lastName = tk.StringVar()
        self.emailId = tk.StringVar()

        self.return_icon = tk.PhotoImage(file="back.png")
        self.return_icon = self.return_icon.subsample(x=25,y=25)

        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        # Calculate the x and y coordinates based on screen size
        self.x = self.screen_width - 25 
        self.y = self.screen_height - 25 

        # Initialize the main page
        self.main_page()


    def main_page(self):
        self.clear_widgets()
        
        self.current_screen = "main_page"
        main_page_frame = tk.Frame(self.root)
        main_page_frame.pack(expand=True, fill='both')
        # Create and configure the GUI elements for the Welcome screen
        self.welcome_label = tk.Label(main_page_frame, text="Welcome to Type Master Pro!")
        self.welcome_label.pack()
        self.login_button = tk.Button(main_page_frame, text="Log In", command=self.login_page)
        self.login_button.pack()
        self.signup_button = tk.Button(main_page_frame, text="Sign Up", command=self.registration_page)
        self.signup_button.pack()
        


    def create_user_db(self):
        with sqlite3.connect("user.db") as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    firstname TEXT NOT NULL,
                    lastname TEXT NOT NULL,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL,
                    emailID TEXT NOT NULL
                );
            ''')

    def registration_page(self):
        self.clear_widgets()
        self.current_screen = "registration_page"
        self.username.set("")  # Set the value of self.username to an empty string
        self.password.set("")  # Set the value of self.password to an empty string
        # Add "Return" button
        return_button = tk.Button(self.root, image=self.return_icon, command=self.return_to_previous_screen)
        return_button.place(x=self.x, y=self.y)
        return_button.photo = self.return_icon
        return_button.pack()
        self.registration_label = tk.Label(self.root, text="Registration")
        self.registration_label.pack()

        self.firstName_label = tk.Label(self.root, text="First Name:")
        self.firstName_label.pack()
        self.firstName_label = tk.Entry(self.root, textvariable=self.firstName)
        self.firstName_label.pack()

        self.lastName_label = tk.Label(self.root, text="Last Name:")
        self.lastName_label.pack()
        self.lastName_label = tk.Entry(self.root, textvariable=self.lastName)
        self.lastName_label.pack()

        self.emailId_label = tk.Label(self.root, text="Email ID:")
        self.emailId_label.pack()
        self.emailId_label = tk.Entry(self.root, textvariable=self.emailId)
        self.emailId_label.pack()

        self.username_label = tk.Label(self.root, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.root, textvariable=self.username)
        self.username_entry.pack()

        self.password_label = tk.Label(self.root, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.root, textvariable=self.password, show="*")
        self.password_entry.pack()

        self.register_button = tk.Button(self.root, text="Register", command=self.register_user)
        self.register_button.pack()

    def login_page(self):
        self.clear_widgets()
        self.current_screen = "login_page"
        self.username.set("")  # Set the value of self.username to an empty string
        self.password.set("")  # Set the value of self.password to an empty string

        # Add "Return" button
        return_button = tk.Button(self.root, image=self.return_icon, command=self.return_to_previous_screen)
        return_button.pack()
        self.login_label = tk.Label(self.root, text="Login")
        self.login_label.pack()

        self.username_label = tk.Label(self.root, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.root, textvariable=self.username)
        self.username_entry.pack()

        self.password_label = tk.Label(self.root, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.root, textvariable=self.password, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(self.root, text="Log In", command=self.authenticate_user)
        self.login_button.pack()

    def register_user(self):
        username = self.username.get()
        password = self.password.get()

        with sqlite3.connect("user.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()

        self.clear_widgets()
        self.login_page()

    def authenticate_user(self):
        username = self.username.get()
        password = self.password.get()

        if username == "admin" and password == "123":
            self.clear_widgets()
            self.manage_profiles()
        else:
            with sqlite3.connect("user.db") as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
                user = cursor.fetchone()
                if user is not None:
                    self.clear_widgets()
                    self.dashboard_page()
                else:
                    # Display an error message
                    self.show_toast("Wrong UserID/password, hope you have already registered")

    def show_toast(self, message):
        toast_window = tk.Toplevel()
        toast_window.geometry("400x100+400+300")  # Adjust the size and position as needed
        toast_label = tk.Label(toast_window, text=message)
        toast_label.pack()

        # After 2 seconds, close the toast window
        toast_window.after(2500, toast_window.destroy)
                

    def dashboard_page(self):
        self.current_screen = "dashboard_page"
        self.clear_widgets()
        dashboard_frame = tk.Frame(self.root)
        dashboard_frame.pack(expand=True, fill='both')
        # Add "Return" button
        return_button = tk.Button(dashboard_frame, image=self.return_icon, command=self.return_to_previous_screen)
        return_button.pack()
        self.dashboard_label = tk.Label(dashboard_frame, text="Dashboard")
        self.dashboard_label.pack()

        self.start_game_button = tk.Button(dashboard_frame, text="Start Game", command=self.start_game)
        self.start_game_button.pack()

        self.check_stats_button = tk.Button(dashboard_frame, text="Check Stats", command=self.check_stats)
        self.check_stats_button.pack()
    def manage_profiles(self):
        if self.username.get() == "admin" and self.password.get() == "123":
            # The user is the admin, so allow access to the profile management feature
            self.clear_widgets()
            self.current_screen = "manage_profiles"
            return_button = tk.Button(self.root, image=self.return_icon, command=self.return_to_previous_screen)
            return_button.pack()

            # List registered users and allow admin to delete profiles
            with sqlite3.connect("user.db") as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users")
                users = cursor.fetchall()
            
                # Display the list of users
                user_listbox = tk.Listbox(self.root)
                for user in users:
                    user_listbox.insert(tk.END, f"Username: {user[1]}, ID: {user[0]}")
                user_listbox.pack()

                # Button to delete selected user
                delete_user_button = tk.Button(self.root, text="Delete User", command=lambda: self.delete_user(user_listbox))
                delete_user_button.pack()
        else:
            self.show_toast("You don't have permission to manage profiles.")

    def delete_user(self, user_listbox):
        selected_user = user_listbox.get(user_listbox.curselection())
        user_id = int(selected_user.split(":")[-1].strip())
    
        with sqlite3.connect("user.db") as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
    
        # Refresh the user list after deletion
        self.manage_profiles()


    def start_game(self):
        # Implement the game here
        pass

    def check_stats(self):
        # Implement stat checking here
        pass

    def return_to_previous_screen(self):
        
        if self.current_screen == "login_page":
            self.main_page()
        elif self.current_screen == "registration_page":
            self.main_page()
        elif self.current_screen == "dashboard_page":
            self.main_page()
        elif self.current_screen == "manage_profiles":
            self.main_page()
        # Add more cases for other screens

    def clear_widgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
if __name__ == "__main__":
    root = tk.Tk()
    app = TypeMasterPro(root)
    root.mainloop()
