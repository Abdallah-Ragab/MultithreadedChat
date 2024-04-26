import threading
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk, scrolledtext
from client import Client


def on_message_received(message):
    app.append_message(f"{message.source}: {message.content}")

class ChatApplication:

    b_color = "#3B67B1"
    y_color = "#F8CD53"

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("HIET Chat Application")
        self.root.geometry("800x600")

        self.create_username_frame()

    def create_username_frame(self):
        self.username_frame = ttk.Frame(self.root)

        # chat icon
        self.chat_icon = tk.PhotoImage(file="icon.png")
        self.chat_icon_label = ttk.Label(self.username_frame, image=self.chat_icon)
        self.chat_icon_label.pack(pady=10)

        # welcome message
        self.title = ttk.Label(self.username_frame, text="Welcome to", font=("Helvetica", 14))
        self.title.pack(pady=10)

        # chat app name
        self.title = ttk.Label(self.username_frame, text="HIET Chat Application!", font=("Helvetica", 20, "bold"))
        self.title.pack(pady=20)

        # username label
        self.username_label = ttk.Label(self.username_frame, text="Enter your username:", font=("Helvetica", 12))
        self.username_label.pack(pady=5)

        # username entry
        self.username_entry = ttk.Entry(self.username_frame, width=30, font=("Helvetica", 12))
        self.username_entry.pack(pady=5)
        self.username_entry.bind("<Return>", lambda event: self.create_chat_frame())

        # connect button
        self.connect_button = ttk.Button(self.username_frame, text="Connect", command=self.create_chat_frame, style="C.TButton", cursor="hand2", takefocus=0, )
        ttk.Style().configure("C.TButton", padding=0, relief="flat", background=self.b_color, foreground=self.y_color)
        self.connect_button.pack(pady=5)

        self.username_frame.pack(fill=tk.BOTH, expand=True)

    def create_chat_frame(self):
        username = self.username_entry.get().strip()
        if username:
            self.username_frame.destroy()

            self.chat_frame = ttk.Frame(self.root)

            self.chat_history = scrolledtext.ScrolledText(self.chat_frame, wrap=tk.WORD)
            self.chat_history.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)

            self.input_frame = ttk.Frame(self.chat_frame)
            self.input_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)

            self.message_entry = ttk.Entry(self.input_frame)
            self.message_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
            self.message_entry.bind("<Return>", lambda event: self.send_message())

            self.send_button = ttk.Button(self.input_frame, text="Send", command=self.send_message, style="", cursor="hand2", takefocus=0,)
            ttk.Style().configure("blue.TButton", padding=0, relief="flat", background=self.b_color, foreground=self.y_color)
            self.send_button.pack(side=tk.RIGHT)

            self.chat_frame.pack(fill=tk.BOTH, expand=True)

            self.client = Client(username=username, onmessage=on_message_received)

            threading.Thread(target=self.client.connect).start()

        else:
            tk.messagebox.showerror("Error", "Nickname cannot be empty.")

    def append_message(self, message):
        self.chat_history.insert(tk.END, message + "\n")
        self.chat_history.tag_configure("blue", foreground="blue")
        self.chat_history.tag_configure("black", foreground="black")
        if message.startswith("Server:"):
            self.chat_history.tag_add("blue", "end-2l", "end-1c")
        else:
            self.chat_history.tag_add("black", "end-2l", "end-1c")
        self.chat_history.see(tk.END)

    def send_message(self):
        message = self.message_entry.get().strip()
        if message:
            self.message_entry.delete(0, tk.END)
            self.client.send(message)

    def exit(self):
        if hasattr(self, "client"):
            self.client.disconnect()

        self.root.destroy()


    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ChatApplication()
    app.root.protocol("WM_DELETE_WINDOW", app.exit)

    app.run()
