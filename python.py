import tkinter as tk
import time

class ContinuousMovementApp:
    def __init__(self, master, canvas_width=800, canvas_height=600):
        self.master = master
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height

        self.canvas = tk.Canvas(master, width=self.canvas_width, height=self.canvas_height, bg="brown")
        self.canvas.pack()

        self.x = self.canvas_width // 10 + 50  # Start from bottom left corner + 50px to the right
        self.y = self.canvas_height - 35  # Start from bottom + 10px up
        self.square_size = 50
        self.border_thickness = 2
        self.gravity = 1
        self.jump_speed = -15  # Decreased jump speed
        self.water_height = self.canvas_height - 10  # Height of the water surface
        self.water_width = 75  # Width of the water area

        self.dx = 0
        self.dy = 0
        self.key_down = False
        self.jump_cooldown = 0
        self.jump_cooldown_duration = 0.5  # 0.5 seconds cooldown

        # Position of the brown box
        self.brown_box_x = self.canvas_width - 100  # Adjusted position
        self.brown_box_y = self.canvas_height - 100  # Adjusted position
        self.brown_box_size = 150  # Increased size

        self.draw_floor()
        self.draw_water()
        self.draw_square()
        self.draw_brown_box()  # Draw the brown box

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

    def draw_water(self):
        self.canvas.create_rectangle(self.canvas_width / 2 - self.water_width / 2, self.water_height,
                                     self.canvas_width / 2 + self.water_width / 2, self.canvas_height,
                                     fill="blue", outline="blue")

    def draw_floor(self):
        self.canvas.create_rectangle(0, self.water_height, self.canvas_width, self.canvas_height,
                                     fill="green", outline="green")

    def draw_brown_box(self):
        self.canvas.create_rectangle(self.brown_box_x, self.brown_box_y,
                                     self.brown_box_x + self.brown_box_size, self.brown_box_y + self.brown_box_size,
                                     fill="#D2B48C", outline="", width=0)  # No outline

    def move_square(self):
        new_x = self.x + self.dx
        new_y = self.y + self.dy

        # Movement boundaries
        if new_x - self.square_size // 2 < self.border_thickness:
            new_x = self.square_size // 2
        elif new_x + self.square_size // 2 > self.brown_box_x - self.border_thickness:
            new_x = self.brown_box_x - self.square_size // 2 - self.border_thickness

        if new_y + self.square_size // 2 > self.canvas_height - self.border_thickness:
            new_y = self.canvas_height - self.square_size // 2 - self.border_thickness
            self.dy = 0
        elif new_y - self.square_size // 2 < self.border_thickness:
            new_y = self.square_size // 2 + self.border_thickness

        # Collision with brown box
        if (new_x - self.square_size // 2 < self.brown_box_x + self.brown_box_size and
                new_x + self.square_size // 2 > self.brown_box_x and
                new_y + self.square_size // 2 > self.brown_box_y and
                new_y - self.square_size // 2 < self.brown_box_y + self.brown_box_size):
            # Check if on top of the brown box
            if self.y + self.square_size // 2 <= self.brown_box_y:
                new_y = self.brown_box_y - self.square_size // 2
            else:
                # Move with the brown box
                dx_box = self.brown_box_x - (self.brown_box_x - self.dx)
                new_x += dx_box

        # Apply gravity if not on any surface
        if new_y + self.square_size // 2 < self.canvas_height - self.border_thickness:
            self.dy += self.gravity

        self.x = new_x
        self.y = new_y

        self.draw_square()

    def jump(self):
        if self.jump_cooldown <= 0:
            self.jump_cooldown = self.jump_cooldown_duration
            self.dy += self.jump_speed

    def start_movement(self):
        if not self.key_down:
            self.key_down = True
            self.move_square()
            self.check_collision()
            self.master.after(20, self.continuous_movement)

    def continuous_movement(self):
        if self.key_down:
            self.move_square()
            self.check_collision()
            if self.jump_cooldown > 0:
                self.jump_cooldown -= 0.02  # Decrease cooldown timer
            self.master.after(20, self.continuous_movement)

    def check_collision(self):
        if (self.x - self.square_size / 2 < self.canvas_width / 2 + self.water_width / 2 and
                self.x + self.square_size / 2 > self.canvas_width / 2 - self.water_width / 2 and
                self.y + self.square_size / 2 > self.water_height):
            self.restart()

    def restart(self):
        self.x = self.canvas_width // 10
        self.y = self.canvas_height - 25
        self.dy = 0
        self.draw_square()
        self.start_movement()

    def key_press(self, event):
        if event.keysym == 'Left':
            self.dx = -10
        elif event.keysym == 'Right':
            self.dx = 10
        elif event.keysym == 'Up':
            self.jump()
        self.start_movement()

    def key_release(self, event):
        if event.keysym in ['Left', 'Right']:
            self.dx = 0
        self.start_movement()

def main():
    root = tk.Tk()
    app = ContinuousMovementApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
