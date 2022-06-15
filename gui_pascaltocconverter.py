import tkinter as tk
from tkinter import messagebox
from pascaltocconverter import *

window = tk.Tk()
window.title("Pascal to C converter")

with open('test5.txt', 'r') as file:
    text = file.read()


def helloCallBack():
    data = inputTK.get(1.0, tk.END)
    outputTK.delete(1.0, tk.END)
    outputTK.insert(1.0, init(data))


greeting = tk.Label(text="Pascal to C converter")
greeting.pack()

btnTK = tk.Button(text="convert", command=helloCallBack)
btnTK.pack()

inputTK = tk.Text(master=window, width=40, height=30, fg="white", bg="black", insertbackground="white")
inputTK.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

inputTK.insert(1.0, text)

outputTK = tk.Text(master=window, width=40, bg="yellow")
outputTK.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

window.mainloop()
