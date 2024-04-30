import tkinter as tk

class ContinuousMovementApp:
    def __init__(self, master, canvas_width=800, canvas_height=600):
        self.master = master
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height

        self.canvas = tk.Canvas(master, width=self.canvas_width, height=self.canvas_height, bg="brown")
        self.canvas.pack()

        self.x = self.canvas_width // 2
        self.y = self.canvas_height // 2
        self.square_size = 50
        self.border_thickness = 2

        self.dx = 0
        self.dy = 0
        self.key_down = False

        self.draw_square()

        master.bind('<KeyPress>', self.key_press)
        master.bind('<KeyRelease>', self.key_release)

        self.start_movement()

    def draw_square(self):
        self.canvas.delete("square")
        x0 = self.x - self.square_size // 2
        y0 = self.y - self.square_size // 2
        x1 = self.x + self.square_size // 2
        y1 = self.y + self.square_size // 2
        self.canvas.create_rectangle(x0, y0, x1, y1, fill="red", tag="square")

    def move_square(self):
        new_x = self.x + self.dx
        new_y = self.y + self.dy

        if (new_x - self.square_size // 2 >= self.border_thickness and new_x + self.square_size // 2 <= self.canvas_width - self.border_thickness and
                new_y - self.square_size // 2 >= self.border_thickness and new_y + self.square_size // 2 <= self.canvas_height - self.border_thickness):
            self.x = new_x
            self.y = new_y

        self.draw_square()

    def start_movement(self):
        if not self.key_down:
            self.key_down = True
            self.move_square()
            self.master.after(20, self.continuous_movement)  # Decreased delay time for faster movement

    def stop_movement(self):
        self.key_down = False

    def continuous_movement(self):
        if self.key_down:
            self.move_square()
            self.master.after(20, self.continuous_movement)  # Decreased delay time for faster movement

    def key_press(self, event):
        if event.keysym == 'Up':
            self.dy = -10
        elif event.keysym == 'Down':
            self.dy = 10
        elif event.keysym == 'Left':
            self.dx = -10
        elif event.keysym == 'Right':
            self.dx = 10
        self.start_movement()

    def key_release(self, event):
        if event.keysym in ['Up', 'Down']:
            self.dy = 0
        elif event.keysym in ['Left', 'Right']:
            self.dx = 0
        if self.dx == 0 and self.dy == 0:
            self.stop_movement()

def main():
    root = tk.Tk()
    app = ContinuousMovementApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
