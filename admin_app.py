import tkinter as tk

class ChatApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Admin Board")

        # Main frame for layout
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Chat display frame
        self.chat_display_frame = tk.Frame(self.main_frame, bg='white', width=400)
        self.chat_display_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Chat display area
        self.chat_display = tk.Text(self.chat_display_frame)
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        self.chat_display.config(state=tk.DISABLED)

        # Chat input frame
        self.chat_input_frame = tk.Frame(self.chat_display_frame)
        self.chat_input_frame.pack(side=tk.LEFT, fill=tk.X)

        # Chat input field
        self.chat_entry = tk.Entry(self.chat_display_frame)
        self.chat_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Send button
        self.send_button = tk.Button(self.chat_display_frame, text="Send", command=self.send_message, width=10, background="#3B67B1", borderwidth=0, fg='white')
        self.send_button.pack(side=tk.RIGHT)

        # Logs frame
        self.logs_frame = tk.Frame(self.main_frame, width=150, bg='#222')
        self.logs_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Logs display area
        self.logs_display = tk.Text(self.logs_frame, bg='#222', fg='white')
        self.logs_display.pack(fill=tk.BOTH, expand=True)
        self.logs_display.config(state=tk.DISABLED)

        # User menu frame
        self.user_menu_frame = tk.Frame(self.main_frame, width=100, bg='lightgrey')
        self.user_menu_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Active users listbox in user menu
        self.active_users_label = tk.Label(self.user_menu_frame, text="Active Users", bg='lightgrey', pady=10)
        self.active_users_label.pack()
        self.active_users_listbox = tk.Listbox(self.user_menu_frame, selectmode=tk.SINGLE)
        self.active_users_listbox.pack(fill=tk.BOTH, expand=True)
        self.populate_active_users()  # Function to populate active users

        # Kick button
        self.kick_button = tk.Button(self.user_menu_frame, text="Kick", command=self.kick_user, width=18, bg='#900', fg='white')
        self.kick_button.pack()

    def populate_active_users(self):
        # Dummy method to populate active users listbox
        active_users = ["User1", "User2", "User3"]  # Replace with actual active users
        for user in active_users:
            self.active_users_listbox.insert(tk.END, user)

    def send_message(self):
        message = self.chat_entry.get()
        if message:
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.insert(tk.END, f"You: {message}\n")
            self.chat_display.config(state=tk.DISABLED)
            self.chat_entry.delete(0, tk.END)

    def kick_user(self):
        selected_user_index = self.active_users_listbox.curselection()
        if selected_user_index:
            selected_user = self.active_users_listbox.get(selected_user_index)
            # Add your logic to kick the selected user
            self.logs_display.config(state=tk.NORMAL)
            self.logs_display.insert(tk.END, f"{selected_user} has been kicked.\n")
            self.logs_display.config(state=tk.DISABLED)


if __name__ == "__main__":
    app = ChatApp()
    app.mainloop()
