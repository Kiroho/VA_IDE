from tkinter import *
import subprocess

main_window = Tk()
main_window.title("Placeholder")


def run():
    # command = f'python{file}'
    # process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    code = editor.get("1.0", END)
    exec(code)


menu_bar = Menu(main_window)

file_bar = Menu(menu_bar, tearoff=0)
file_bar.add_command(label="New")
file_bar.add_command(label="Save")
file_bar.add_command(label="Save As")
file_bar.add_command(label="Load")
menu_bar.add_cascade(label="File", menu=file_bar)

option_bar = Menu(menu_bar, tearoff=0)
option_bar.add_command(label="Microphone")
option_bar.add_command(label="Hardware Acceleration")
menu_bar.add_cascade(label="Options", menu=option_bar)

menu_bar.add_command(label="Run", command=run)

main_window.config(menu=menu_bar)

editor = Text()
editor.pack()

main_window.mainloop()
