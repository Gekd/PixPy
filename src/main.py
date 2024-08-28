import os
import tkinter as tk
from tkinter import ttk


def read_file(file_name, saved_design):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    folder = "data"

    if saved_design:
        file_path = os.path.join(current_dir, folder, "saved_designs",file_name)
    else:
        file_path = os.path.join(current_dir, folder, "years",file_name)

    with open(file_path, "r", encoding="utf-8") as file:
        file_lines = [line.rstrip() for line in file]

    return [line.split(", ") for line in file_lines]


class Application(tk.Frame):
    def __init__(self, parent, rows=7, columns=53):
        super().__init__(parent)

        self.url = "2024.txt"
        self.has_saved_design = False
        self.rows = rows
        self.columns = columns
        self.selected_color = "#0e4429"
        self.is_drawing = False
        self.drawing_grid = []
        self.button_width = 10

        self.create_widgets()

    def create_widgets(self):
        label = ttk.Label(self, text="Draw page")
        label.grid(row=0, column=3, padx=10, pady=10)

        self.canvas = tk.Canvas(self, width=self.columns * 10, height=self.rows * 10)
        self.canvas.grid(row=1, column=0, columnspan=self.columns, padx=10, pady=10)
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)

        self.file_chooser_widgets = []
        self.start_new_design_widgets = []

        self.show_file_chooser()

    def show_file_chooser(self):
        load_new_button = ttk.Button(
            self, text="Start new design", command=lambda: self.open_design_page(False), width=self.button_width + 10
        )
        load_new_button.grid(row=2, column=2, padx=10, pady=10)
        self.file_chooser_widgets.append(load_new_button)

        load_saved_button = ttk.Button(
            self, text="Load saved design", command=lambda: self.open_design_page(True), width=self.button_width + 10
        )
        load_saved_button.grid(row=2, column=4, padx=10, pady=10)
        self.file_chooser_widgets.append(load_saved_button)

    def hide_file_chooser(self):
        for widget in self.file_chooser_widgets:
            widget.grid_forget()

    def open_design_page(self, has_saved_design):
        self.has_saved_design = has_saved_design
        self.hide_file_chooser()
        self.data = read_file(self.url, self.has_saved_design)
        self.create_drawing_view()

    def create_drawing_view(self):
        self.create_grid()

        color_buttons = {
            "1": "#0e4429",
            "5": "#006d32",
            "10": "#26a641",
            "15": "#39d353",
        }

        for i, (text, color) in enumerate(color_buttons.items(), start=1):
            button = ttk.Button(
                self, text=text, command=lambda c=color: self.select_color(c), width=self.button_width
            )
            button.grid(row=2, column=i, padx=10, pady=10)
            self.start_new_design_widgets.append(button)

        clear_button = ttk.Button(self, text="Clear all", command=self.clear_grid, width=self.button_width)
        clear_button.grid(row=2, column=5, padx=10, pady=10)
        self.start_new_design_widgets.append(clear_button)

        save_button = ttk.Button(self, text="Save design", command=self.save_design, width=self.button_width)
        save_button.grid(row=3, column=3, padx=10, pady=10)
        self.start_new_design_widgets.append(save_button)

    def create_grid(self):
        for row_idx, row in enumerate(self.data):
            row_labels = []
            for col_idx, value in enumerate(row):
                x1, y1 = col_idx * 10, row_idx * 10
                x2, y2 = x1 + 10, y1 + 10
                color = self.get_color(value)
                if color:
                    label = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
                else:
                    label = None
                row_labels.append(label)
            self.drawing_grid.append(row_labels)

    def get_color(self, value):
        color_mapping = {
            "0": "white",
            "1": "#0e4429",
            "5": "#006d32",
            "10": "#26a641",
            "15": "#39d353",
        }
        return color_mapping.get(value)

    def select_color(self, color):
        self.selected_color = color

    def start_drawing(self, event):
        self.is_drawing = True
        self.color_label(event.x, event.y)

    def draw(self, event):
        if self.is_drawing:
            self.color_label(event.x, event.y)

    def stop_drawing(self):
        self.is_drawing = False

    def color_label(self, x, y):
        col, row = x // 10, y // 10
        if 0 <= row < self.rows and 0 <= col < self.columns:
            label = self.drawing_grid[row][col]
            if label:
                self.canvas.itemconfig(label, fill=self.selected_color)

    def clear_grid(self):
        for row in self.drawing_grid:
            for label in row:
                if label:
                    self.canvas.itemconfig(label, fill="white")

    def save_design(self):
        data_to_save = self.convert_grid_to_text(self.drawing_grid)
        self.save_to_file(self.url, data_to_save)

    def convert_grid_to_text(self, grid):
        result = []
        
        for row in grid:
            row_data = []
            
            for label in row:
                if label is not None:
                    color = self.canvas.itemcget(label, 'fill')
                    value = self.get_value_from_color(color)
                else:
                    value = "X"
                
                row_data.append(value)
            
            result.append(', '.join(row_data))
        
        return result


    def get_value_from_color(self, color):
        color_mapping = {
            "white": "0",
            "#0e4429": "1",
            "#006d32": "5",
            "#26a641": "10",
            "#39d353": "15",
        }
        return color_mapping.get(color, "X")

    def save_to_file(self, file_name, data):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        folder = os.path.join(current_dir, "data/saved_designs")

        os.makedirs(folder, exist_ok=True)

        file_path = os.path.join(folder, file_name)

        with open(file_path, "w", encoding="utf-8") as file:
            for line in data:
                file.write(f"{line}\n")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Drawing Application")
    ui_page = Application(root)
    ui_page.pack(fill="both", expand=True)
    root.mainloop()