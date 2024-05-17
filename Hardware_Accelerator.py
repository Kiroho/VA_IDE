import tkinter
from tkinter import *


class MicrophoneWindow(Toplevel):
    def __init__(self, master):
        Toplevel.__init__(self, master)
        self.frame = Frame(self)
        self.focus_set()
        self.geometry("300x300")

        def on_okay():
            self.master.microphone_data = device_list.get(ANCHOR)
            print(device_list.get(ANCHOR))
            print(self.master.connected_devices[device_list.get(ANCHOR)])
            self.destroy()

        def on_cancel():
            self.destroy()

        device_list = Listbox(self)
        for x, y in enumerate(self.master.connected_devices):
            device_list.insert(x + 1, y)
        device_list.pack(padx=10, pady=10, fill=tkinter.BOTH, expand=True)

        okay_btn = Button(self, text="Okay", command=on_okay)
        cancel_btn = Button(self, text="Cancel", command=on_cancel)
        okay_btn.pack(pady=1)
        cancel_btn.pack(pady=1)
        self.wm_attributes("-topmost", True)
        self.grab_set()
