import tkinter as tk
from pascaltocconverter import *

window = tk.Tk()

with open('test.txt', 'r') as file:
    text = file.read()


def helloCallBack():
    # data = inputTK.get(1.0, tk.END)
    # outputTK.delete(1.0, tk.END)
    # outputTK.insert(1.0, data)
    data = inputTK.get(1.0, tk.END)
    outputTK.delete(1.0, tk.END)
    outputTK.insert(1.0, init(data))


greeting = tk.Label(text="Pascal to C converter")
greeting.pack()

btnTK = tk.Button(text="convert", command=helloCallBack)
btnTK.pack()

inputTK = tk.Text(master=window, width=30, height=20, fg="white", bg="black", insertbackground="white")
inputTK.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

inputTK.insert(1.0, text)

outputTK = tk.Text(master=window, width=30, bg="yellow")
outputTK.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

window.mainloop()
