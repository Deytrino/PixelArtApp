from tkinter import *
import tkinter as tk

class PixelApp:
  def __init__(self, root):
    self.root = root
    self.root.title("Pixel Art")

root = Tk()
PixelApp(root)
root.mainloop()