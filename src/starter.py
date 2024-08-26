import tkinter as tk
from tkinter import ttk

class StartPage(tk.Frame):
    def __init__(self, parent, controller, page): 
        super().__init__(parent)
        
        label = ttk.Label(self, text="Startpage")
        label.grid(row=0, column=4, padx=10, pady=10) 
    
        button2 = ttk.Button(self, text="UI",
                             command=lambda: controller.show_frame(page))
        button2.grid(row=2, column=1, padx=10, pady=10)
