import tkinter as tk

window = tk.Tk()


def helloCallBack():
    data = inputTK.get(1.0, tk.END)
    outputTK.delete(1.0, tk.END)
    outputTK.insert(1.0, data)


greeting = tk.Label(text="Pascal to C converter")
greeting.pack()

btnTK = tk.Button(text="convert", command=helloCallBack)
btnTK.pack()

inputTK = tk.Text(master=window, width=30, height=20, fg="white", bg="black")
inputTK.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

outputTK = tk.Text(master=window, width=30, bg="yellow")
outputTK.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)


window.mainloop()
