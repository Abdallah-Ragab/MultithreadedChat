import tkinter as tk
import logging


def on_message_received(message):
    app.append_message(f"{message.source}: {message.content}")


class LogsWidgetHandler(logging.Handler):
    def __init__(self, logs_display):
        super().__init__()
        self.logs_display = logs_display

    def emit(self, record):
        log_message = self.format(record)
        self.logs_display.config(state=tk.NORMAL)
        self.logs_display.insert(tk.END, f"{log_message}\n")
        self.logs_display.config(state=tk.DISABLED)
        self.logs_display.see(tk.END)


class ChatApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hiet Chat Application - Admin panel")
        self.geometry("1400x600")

        # Main frame for layout
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Chat display frame
        self.chat_display_frame = tk.Frame(self.main_frame, bg="white", width=400)
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
        self.chat_entry.bind("<Return>", lambda event: self.send_message())

        # Send button
        self.send_button = tk.Button(
            self.chat_display_frame,
            text="Send",
            command=self.send_message,
            width=10,
            background="#3B67B1",
            borderwidth=0,
            fg="white",
        )
        self.send_button.pack(side=tk.RIGHT)

        # Logs frame
        self.logs_frame = tk.Frame(self.main_frame, width=150, bg="#222")
        self.logs_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Logs display area
        self.logs_display = tk.Text(self.logs_frame, bg="#222", fg="white")
        self.logs_display.pack(fill=tk.BOTH, expand=True)
        self.logs_display.config(state=tk.DISABLED)

        # User menu frame
        self.user_menu_frame = tk.Frame(self.main_frame, width=100, bg="lightgrey")
        self.user_menu_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Active users listbox in user menu
        self.active_users_label = tk.Label(
            self.user_menu_frame, text="Active Users", bg="lightgrey", pady=10
        )
        self.active_users_label.pack()
        self.active_users_listbox = tk.Listbox(
            self.user_menu_frame, selectmode=tk.SINGLE
        )
        self.active_users_listbox.pack(fill=tk.BOTH, expand=True)

        # Kick button
        self.kick_button = tk.Button(
            self.user_menu_frame,
            text="Kick",
            command=self.kick_user,
            width=18,
            bg="#900",
            fg="white",
        )
        self.kick_button.pack()

        admin_app_log_handler = LogsWidgetHandler(self.logs_display)

        from server import Server

        self.server = Server(
            onmessage=on_message_received,
            onclientadd=self.on_client_change,
            onclientremove=self.on_client_change,
            onclientchange=self.on_client_change,
            log_handler=admin_app_log_handler,
        )
        self.server.start()

        self.populate_active_users()  # Function to populate active users

    def append_message(self, message):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"{message}\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

    def populate_active_users(self):
        self.active_users_listbox.delete(0, tk.END)
        active_users = self.server.clients.values()
        for user in active_users:
            self.active_users_listbox.insert(tk.END, f"{user.username}[{user.id}]")

    def on_client_change(self, client):
        self.populate_active_users()

    def send_message(self):
        message = self.chat_entry.get().strip()
        if message:
            self.chat_entry.delete(0, tk.END)
            self.server.send(message)

    def kick_user(self):
        selected_user_index = self.active_users_listbox.curselection()
        if selected_user_index:
            selected_user_identifier = self.active_users_listbox.get(
                selected_user_index
            )
            selected_user_id = selected_user_identifier.split("[")[1].split("]")[0]
            self.server.kick(selected_user_id)

    def exit(self):
        if hasattr(self, "server"):
            self.server.shutdown()
        self.destroy()
        exit(0)


if __name__ == "__main__":
    app = ChatApp()
    app.protocol("WM_DELETE_WINDOW", app.exit)
    app.mainloop()
