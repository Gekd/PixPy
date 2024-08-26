import tkinter as tk
import sv_ttk

from ui import UiPage
from starter import StartPage

class Application(tk.Tk):
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs)
        
        container = tk.Frame(self) 
        container.pack(side="top", fill="both", expand=True) 

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        sv_ttk.set_theme("dark")
        self.title("PixPy")


        self.frames = {} 

        for Page in (StartPage, UiPage):
            if Page == StartPage:
                frame = Page(container, self, UiPage)
            else:
                frame = Page(container, self,StartPage)
            self.frames[Page] = frame  
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


if __name__ == "__main__":
    app = Application()
    app.mainloop()
