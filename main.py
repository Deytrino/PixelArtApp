from tkinter import *
import tkinter.colorchooser
from PIL import ImageGrab
from datetime import datetime

class PixelApp:
	def __init__(self, root):
		self.root = root
		self.root.title("Pixel Art")

		cell_length = 25
		grid_width = 20
		grid_height = 10
		
		self.color_chooser = tkinter.colorchooser.Chooser(self.root)
		self.chosen_color = None
		self.is_pen_selected = False
		self.is_eraser_selected = False

		self.drawing_grid = Canvas(self.root)
		self.drawing_grid.grid(column=0, row=0, sticky=(N,E,S,W))

		self.cells = []
		for x in range(grid_width):
			for y in range(grid_height):
				cell = Frame(self.drawing_grid, width=cell_length, height=cell_length, bg="white", highlightbackground="black", highlightcolor = "black", highlightthickness=1)
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
		pencil_button = Button(control_frame, image=self.pencil_image, text="Paint", command=self.press_pencil_button)
		pencil_button.grid(column = 8, row = 0, columnspan=2, sticky=(N,E,S,W), padx=5, pady=5)

		self.erase_image = PhotoImage(file="eraser.png").subsample(4,6)
		erase_button = Button(control_frame, image=self.erase_image, text="Erase", command=self.press_erase_button)
		erase_button.grid(column = 10, row = 0, columnspan=2, sticky=(N,E,S,W), padx=5, pady=5)

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
		widget = event.widget
		index = self.cells.index(widget)
		selected_cell = self.cells[index]
		if self.is_pen_selected and self.chosen_color != None:
			selected_cell.configure(bg = self.chosen_color)
		elif self.is_eraser_selected:
			selected_cell.configure(bg = "White")
    
	def press_new_button(self):
		print("New button pressed")
		for i in range(len(self.cells)):
			self.cells[i].configure(bg = "white")
		self.chosen_color = None
		self.is_pen_selected = False
		self.is_eraser_selected = False
		self.selected_color_box.configure(bg = "white")

	def press_save_button(self):
		print("Save button pressed")
		x = self.root.winfo_rootx() + self.drawing_grid.winfo_x()
		y = self.root.winfo_rooty() + self.drawing_grid.winfo_y() + 35

		width = x + 500
		height = y + 250

		image_name = datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".png"
		ImageGrab.grab(bbox=(x, y, width, height)).save(image_name)

    
	def press_pencil_button(self):
		print("Paint button pressed")
		self.is_pen_selected = True
		self.is_eraser_selected = False
 
	def press_erase_button(self):
		print("Erase button pressed")
		self.is_pen_selected = False
		self.is_eraser_selected = True
    
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