import os
import tkinter as tk
from tkinter import ttk

def list_maker(labels):
    result_list = []
    for row in labels:
        inner_list = []
        for label in row:
            color_name = label.palette().window().color().name()
            if color_name == "#0e4429":
                inner_list.append("1")
            elif color_name == "#006d32":
                inner_list.append("5")
            elif color_name == "#26a641":
                inner_list.append("10")
            elif color_name == "#39d353":
                inner_list.append("15")
        result_list.append(inner_list)
    return result_list


def read_file(file_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "data", file_name)

    with open(file_path, "r", encoding="utf-8") as file:
        file_lines = [line.rstrip() for line in file]

    return_data = []  
    
    for line in file_lines:
        splitted_line = line.split(", ")
        return_data.append(splitted_line)

    return return_data

class UiPage(tk.Frame): 
    def __init__(self, parent, controller, page, rows=7, columns=53):
        tk.Frame.__init__(self, parent)
        
        label = ttk.Label(self, text="Draw page")
        label.grid(row=0, column=4, padx=10, pady=10)

        self.rows = rows
        self.columns = columns
        self.selected_color = "#0e4429"
        self.is_drawing = False

        # Use grid for the canvas
        self.canvas = tk.Canvas(self, width=columns * 10, height=rows * 10)
        self.canvas.grid(row=1, column=0, columnspan=columns, padx=10, pady=10)

        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)

        self.data = read_file("2024.txt")
        self.drawing_grid = []  
        self.create_grid()


        color_button_1 = ttk.Button(self, text="1", command=lambda: self.select_color("#0e4429"))
        color_button_1.grid(row=2, column=1, padx=10, pady=10)

        color_button_5 = ttk.Button(self, text="5", command=lambda: self.select_color("#006d32"))
        color_button_5.grid(row=2, column=2, padx=10, pady=10)

        color_button_10 = ttk.Button(self, text="10", command=lambda: self.select_color("#26a641"))
        color_button_10.grid(row=2, column=3, padx=10, pady=10)

        color_button_15 = ttk.Button(self, text="15", command=lambda: self.select_color("#39d353"))
        color_button_15.grid(row=2, column=4, padx=10, pady=10)

        clear_button = ttk.Button(self, text="Clear all", command= self.clear_grid())
        clear_button.grid(row=2, column=5, padx=10, pady=10)

        button2 = ttk.Button(self, text="Startpage", command=lambda: controller.show_frame(page))
        button2.grid(row=3, column=1, padx=10, pady=10)
    
    def create_grid(self):
        for row_idx, row in enumerate(self.data):
            row_labels = []
            for col_idx, col in enumerate(row):
                if col == 'X':
                    x1 = col_idx * 10
                    y1 = row_idx * 10
                    x2 = x1 + 10
                    y2 = y1 + 10

                    label = self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")
                    row_labels.append(label)
                else:
                    row_labels.append(None)
            self.drawing_grid.append(row_labels)

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
        col = x // 10
        row = y // 10
        if 0 <= row < self.rows and 0 <= col < self.columns:
            label = self.drawing_grid[row][col]
            if label is not None:
                self.canvas.itemconfig(label, fill=self.selected_color)

    def clear_grid(self):
        for row in self.drawing_grid:
            for label in row:
                if label is not None:
                    self.canvas.itemconfig(label, fill="white")