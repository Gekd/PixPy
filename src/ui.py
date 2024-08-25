import tkinter as tk

# TODO: Implement the read_file function
def read_file(file_name):
    with open(file_name, encoding='utf-8') as file:
        file_lines = [line.rstrip() for line in file]

    data = []
    for line in file_lines:
        splitted_line = line.split(", ")
        data.append(splitted_line)

    return data

# TODO: Implement the list_maker function
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
    print(result_list)
              


class ColorGridApp(tk.Tk):
    def __init__(self, rows=7, columns=53):
        super().__init__()
        
        self.title("Pixel Art Drawing Window")
        self.geometry("500x240")
        
        self.rows = rows
        self.columns = columns
        self.selected_color = "#0e4429"  # Default color
        self.is_drawing = False

        self.canvas = tk.Canvas(self, width=columns * 10, height=rows * 10)
        self.canvas.pack()

        self.create_grid()

        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)

        # Corrected button commands
        self.color_button1 = tk.Button(self, text="1", command=lambda: self.select_color("#0e4429"))
        self.color_button1.pack(side=tk.TOP)
        
        self.color_button2 = tk.Button(self, text="5", command=lambda: self.select_color("#006d32"))
        self.color_button2.pack(side=tk.TOP)

        self.color_button3 = tk.Button(self, text="10", command=lambda: self.select_color("#26a641"))
        self.color_button3.pack(side=tk.TOP)

        self.color_button4 = tk.Button(self, text="15", command=lambda: self.select_color("#39d353"))
        self.color_button4.pack(side=tk.TOP)

        # Button to clear the grid
        self.clear_button = tk.Button(self, text="Clear All", command=self.clear_grid)
        self.clear_button.pack(side=tk.TOP)

    def create_grid(self):
        self.labels = []
        for row in range(self.rows):
            row_labels = []
            for col in range(self.columns):
                x1 = col * 10
                y1 = row * 10
                x2 = x1 + 10
                y2 = y1 + 10
                label = self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")
                row_labels.append(label)
            self.labels.append(row_labels)

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
            label = self.labels[row][col]
            self.canvas.itemconfig(label, fill=self.selected_color)

    def clear_grid(self):
        for row in self.labels:
            for label in row:
                self.canvas.itemconfig(label, fill="white")

if __name__ == "__main__":
    app = ColorGridApp()
    app.mainloop()


