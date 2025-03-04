import tkinter as tk
from tkinter import filedialog, Menu
from PIL import Image, ImageTk
import os
import sys

class PetWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.setup_window()
        self.setup_animation("cat-vibe-disco-cat.gif")
        self.bind_events()

    def setup_window(self):
        try:
            self.overrideredirect(True)
            self.attributes('-topmost', True)
            self.configure(bg="white")
            self.resizable(False, False)  # Pencerenin yeniden boyutlandırılabilir olmasını devre dışı bırakır
        except Exception as e:
            print(f"window error: {e}")

    def setup_animation(self, gif_file):
        self.frames = []
        self.current_frame = 0
        
        gif_path = os.path.join(os.path.dirname(__file__), gif_file)
        
        try:
            if not os.path.exists(gif_path):
                raise FileNotFoundError(f"couldnt locate gif: {gif_path}")
                
            gif = Image.open(gif_path)
            while True:
                self.frames.append(gif.copy())
                gif.seek(len(self.frames))
        except EOFError:
            pass
        except Exception as e:
            print(f"gif error: {e}")
            return

        if not self.frames:
            print("gif error: frames not found")
            return

        gif_width, gif_height = self.frames[0].width, self.frames[0].height
        self.geometry(f"{gif_width}x{gif_height}+100+100")

        self.label = tk.Label(self, bg="black")
        self.label.place(x=0, y=0)
        self.animate(0)

        self.bind_events()

    def animate(self, frame_num):
        frame = self.frames[frame_num]
        self.photo = ImageTk.PhotoImage(frame)
        self.label.configure(image=self.photo)
        self.current_frame = (frame_num + 1) % len(self.frames)
        self.after(50, self.animate, self.current_frame)

    def bind_events(self):
        self.label.bind('<Button-1>', self.start_drag)
        self.label.bind('<B1-Motion>', self.on_drag)
        self.bind('<F8>', self.show_menu)

    def start_drag(self, event):
        self.x = event.x
        self.y = event.y

    def on_drag(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry(f"+{x}+{y}")

    def show_menu(self, event):
        menu = Menu(self, tearoff=0)
        menu.add_command(label="Change gif", command=self.change_gif)
        menu.add_command(label="Template 1", command=lambda: self.setup_animation("cat-vibe-disco-cat.gif"))
        menu.add_command(label="Template 2", command=lambda: self.setup_animation("sansss.gif"))
        menu.add_command(label="Exit", command=self.quit)
        menu.add_command(label="sup qhere32", command=lambda: None)
        menu.post(event.x_root, event.y_root)

    def change_gif(self):
        file_path = filedialog.askopenfilename(filetypes=[("GIF files", "*.gif")])
        if file_path:
            self.setup_animation(file_path)

if __name__ == "__main__":
    app = PetWindow()
    app.mainloop()