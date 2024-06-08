import tkinter
from tkinter import *


class VAConfigWindow(Toplevel):

    def __init__(self, master):
        Toplevel.__init__(self, master)
        self.frame = Frame(self)
        self.focus_set()
        self.geometry("300x300")

        def on_okay():
            sliders = {"start": start_volume.get(), "stop": stop_volume.get(), "timer": timeout_timer.get()}
            print(sliders.get("start"))
            print(sliders.get("stop"))
            print(sliders.get("timer"))
            self.master.sliders = sliders
            self.destroy()

        def on_cancel():
            self.destroy()

        volume_start_frame = Frame(self)
        volume_start_frame.pack(side="top")
        start_volume = Scale(master=volume_start_frame, from_=500, to=2500, resolution=50.0, length=150,
                             orient=HORIZONTAL)
        start_volume.set(self.master.sliders.get("start"))
        start_volume.pack(side="right", padx=10)
        volume_start_label = Label(master=volume_start_frame, text="Activation Volume: ")
        volume_start_label.pack(side="right")

        volume_stop_frame = Frame(self)
        volume_stop_frame.pack(side="top")
        stop_volume = Scale(master=volume_stop_frame, from_=0, to=2000,
                            resolution=50.0, length=150, orient=HORIZONTAL)
        stop_volume.set(self.master.sliders.get("stop"))
        stop_volume.pack(side="right", padx=10)
        volume_stop_label = Label(master=volume_stop_frame,
                                  text="Deactivation Volume: ")
        volume_stop_label.pack(side="right")

        timeout_frame = Frame(self)
        timeout_frame.pack(side="top")
        timeout_timer = Scale(master=timeout_frame, from_=0.5, to=5, resolution=0.5, length=150, orient=HORIZONTAL)
        timeout_timer.set(self.master.sliders.get("timer"))
        timeout_timer.pack(side="right", padx=10)
        timeout_label = Label(master=timeout_frame, text="Deactivation Timer: ")
        timeout_label.pack(side="right")

        button_frame = Frame(self)
        button_frame.pack(side="bottom")
        okay_btn = Button(master=button_frame, text="Okay", command=on_okay)
        cancel_btn = Button(master=button_frame, text="Cancel", command=on_cancel)
        okay_btn.pack(pady=20, padx=10, side="left")
        cancel_btn.pack(pady=20, padx=10, side="left")
        self.wm_attributes("-topmost", True)
        self.grab_set()
