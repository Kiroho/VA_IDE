import tkinter
from tkinter import *


class HardwareWindow(Toplevel):


    def __init__(self, master):
        Toplevel.__init__(self, master)
        self.frame = Frame(self)
        self.focus_set()
        self.geometry("300x300")
        hardware_dict = {"CPU - int8": ["cpu", "int8"],
                         "CUDA - int8": ["cuda", "int8_float16"],
                         "CUDA - float16": ["cuda", "float16"],
                         "CUDA - float32": ["cuda", "float32"]}

        def on_okay():
            try:
                self.master.hardware_accelerator = hardware_dict.get(hardware_list.get(hardware_list.curselection()))
                self.master.new_hardware_selected = True
                self.master.set_hardware_accelerator()
                # print(self.master.hardware_accelerator)
            except Exception:
                self.master.new_hardware_selected = False
                print("an exception happened on hardware accelerator selection")
            finally:
                self.destroy()

        def on_cancel():
            self.destroy()

        hardware_list = Listbox(self)
        for x, y in enumerate(hardware_dict):
            print(str(y))
            hardware_list.insert(x+1, y)
        hardware_list.pack(padx=10, pady=10, fill=tkinter.BOTH, expand=True)

        button_frame = Frame(self)
        button_frame.pack(side="bottom")
        okay_btn = Button(master=button_frame, text="Okay", command=on_okay)
        cancel_btn = Button(master=button_frame, text="Cancel", command=on_cancel)
        okay_btn.pack(pady=20, padx=10, side="left")
        cancel_btn.pack(pady=20, padx=10, side="left")
        self.wm_attributes("-topmost", True)
        self.grab_set()
