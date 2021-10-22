from tkinter import *
import tkinter.colorchooser
from PIL import Image
from PIL import ImageColor
import numpy as np
from datetime import datetime

class PixelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pixel Art")

        cell_length = 25
        self.grid_width = 20
        self.grid_height = 10
        
        self.color_chooser = tkinter.colorchooser.Chooser(self.root)
        self.chosen_color = None
        self.is_drawing_mode = True

        self.drawing_grid = Canvas(self.root)
        self.drawing_grid.grid(column=0, row=0, sticky=(N,E,S,W))

        self.cells = []
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                cell = Frame(self.drawing_grid, width=cell_length, height=cell_length, bg="#ffffff", highlightbackground="black", highlightcolor = "black", highlightthickness=1)
                cell.bind("<Button-1>", self.tap_cell)
                cell.grid(row = y, column = x)
                self.cells.append(cell)

        control_frame = Frame(self.root, height = cell_length)
        control_frame.grid(column=0, row = 1, sticky=(N,E,S,W))

        new_button = Button(control_frame, text="New", command=self.press_new_button)
        new_button.grid(column = 0, row = 0, columnspan=2, sticky=(N,E,S,W), padx=5, pady=5)

        save_button = Button(control_frame, text="Save", command=self.press_save_button)
        save_button.grid(column = 2, row = 0, columnspan=2, sticky=(N,E,S,W), padx=5, pady=5)

        self.pencil_image = PhotoImage(file="pencil.png").subsample(4,6)
        self.pencil_button = Button(control_frame, image=self.pencil_image, text="Paint", command=self.press_pencil_button)
        self.pencil_button.grid(column = 8, row = 0, columnspan=2, sticky=(N,E,S,W), padx=5, pady=5)

        self.erase_image = PhotoImage(file="eraser.png").subsample(4,6)
        self.erase_button = Button(control_frame, image=self.erase_image, text="Erase", command=self.press_erase_button)
        self.erase_button.grid(column = 10, row = 0, columnspan=2, sticky=(N,E,S,W), padx=5, pady=5)

        self.selected_color_box = Frame(control_frame, borderwidth=2, relief="raised", bg="white")
        self.selected_color_box.grid(column=15, row=0, sticky=(N, E, S, W), padx=5, pady=5)

        pick_colour_button = Button(control_frame, text="Pick color", command=self.press_pick_color_button)
        pick_colour_button.grid(column = 17, row = 0, columnspan=3, sticky=(N,E,S,W), padx=5, pady=5)
    
        cols, rows = control_frame.grid_size()
        for col in range(cols):
            control_frame.columnconfigure(col, minsize=cell_length)
        control_frame.rowconfigure(0, minsize=cell_length)

    
    def tap_cell(self, event):
        print("Cell tapped")
        if self.is_drawing_mode and self.chosen_color != None:
            event.widget.configure(bg = self.chosen_color)
        elif not self.is_drawing_mode:
            event.widget.configure(bg = "White")
    
    def press_new_button(self):
        print("New button pressed")
        for i in range(len(self.cells)):
            self.cells[i].configure(bg = "white")
        self.chosen_color = None
        self.is_drawing_mode = True
        self.selected_color_box.configure(bg = "white")

    def press_save_button(self):
        print("Save button pressed")
        colors_array = np.array(list(map(lambda s: ImageColor.getcolor(s["bg"], "RGB"), self.cells)))
        
        colors_matrix = np.zeros([self.grid_height, self.grid_width, 4], dtype=np.uint8)
        
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                index = x*self.grid_height + y
                colors_matrix[y, x] = [colors_array[index][0], colors_array[index][1], colors_array[index][2], 255]

        img = Image.fromarray(colors_matrix)
        image_name = datetime.now().strftime("%d-%m-%Y-%H-%M-%S") + ".png"
        img.save(image_name)

    
    def press_pencil_button(self):
        print("Paint button pressed")
        self.is_drawing_mode = True
 
    def press_erase_button(self):
        print("Erase button pressed")
        self.is_drawing_mode = False
    
    def press_pick_color_button(self):
        print("Pick color button pressed")
        color_info = self.color_chooser.show()
        chosen = color_info[1]
        if chosen != None:
            self.chosen_color = chosen
            self.selected_color_box.configure(bg = self.chosen_color)
        print(self.chosen_color, " picked")
    


root = Tk()
PixelApp(root)
root.mainloop()