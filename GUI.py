import os
import signal
import threading
import time
import tkinter
from tkinter import *
import tkinter.messagebox
from tkinter.filedialog import asksaveasfilename, askopenfilename
import subprocess

from Hardware_Accelerator import HardwareWindow
from Microphone_Selection import MicrophoneWindow
from Voice_Assistant import VoiceAssistant
import pyaudio
import Categorize as c
from tklinenums import TkLineNumbers


class MainGUI(tkinter.Tk):
    def process_va_data(self, data):
        print(data)
        c.classify_text(self, self.editor, data)

    #info pop ups
    def create_micro_on_info(self, text="", color="light green"):
        img = PhotoImage()
        self.micro = Label(master=self.editor, text=text, image=img, compound=LEFT,
                           font=('', int(self.info_text_size / 3)),
                           bg=color, width=self.editor.winfo_width(), height=int(self.info_height / 3))
        self.micro.place(relx=0, y=int(self.editor.winfo_height() - ((self.info_height + 3) / 3)))

    def stop_micro_on_info(self):
        self.after(0, self.micro.destroy)

    def create_recording_info(self, text="", color="light green"):
        img = PhotoImage()
        self.recording = Label(master=self.editor, text=text, image=img, compound=CENTER,
                               font=('', self.info_text_size), bg=color,
                               width=self.winfo_width(), height=self.info_height)
        self.recording.place(relx=.5, y=int(self.editor.winfo_height() - self.info_height + 3), anchor=CENTER)

    def stop_recording_info(self):
        self.after(0, self.recording.destroy)

    def create_processing_info(self, text="", color="yellow"):
        img = PhotoImage()
        self.processing = Label(master=self.editor, text=text, image=img, compound=CENTER,
                                font=('', self.info_text_size), bg=color,
                                width=self.winfo_width(), height=self.info_height)
        self.processing.place(relx=.5, y=int(self.editor.winfo_height() - self.info_height + 3), anchor=CENTER)

    def stop_processing_info(self):
        self.after(0, self.processing.destroy)

    def create_error_info(self, text="", color="red", timer=3000):
        img = PhotoImage()
        self.error = Label(master=self.editor, text=text, image=img, compound=CENTER, font=('', self.info_text_size),
                           bg=color, width=self.winfo_width(), height=self.info_height)
        self.error.place(relx=.5, y=int(self.editor.winfo_height() - self.info_height + 3), anchor=CENTER)
        self.after(timer, self.error.destroy)

    def set_hardware_accelerator(self):
        if self.new_hardware_selected:
            self.new_hardware_selected = False
        self.va.stop()
        self.va.tts_device = self.hardware_accelerator[0]
        self.va.tts_compute_type = self.hardware_accelerator[1]
        self.va.model = None
        print("Voice Assistant is now OFF")
        self.stop_micro_on_info()
        self.va.stop()
        self.va_on = False



    def __init__(self):
        tkinter.Tk.__init__(self)
        self.info_text_size = 12
        self.info_height = 14
        self.error = Label()
        self.recording = Label()
        self.processing = Label()
        self.micro = Label()
        self.file_path = ""
        self.process = None
        self.py_audio = None
        self.microphone_data = ""
        self.connected_devices = {}
        self.hardware_accelerator = ["cuda", "float32"]
        self.new_hardware_selected = False
        self.va_on = False
        self.va = None

        def voice_assistant():
            if not self.va:
                self.va = VoiceAssistant(owner=self,
                                         tts_device=self.hardware_accelerator[0],
                                         tts_compute_type=self.hardware_accelerator[1])
            if not self.va_on:
                print("Voice Assistant is now ON")
                self.create_micro_on_info()
                index = 0
                if self.microphone_data and self.connected_devices:
                    index = self.connected_devices[self.microphone_data]
                    print(f'choosen index = {index}')
                t = threading.Thread(target=self.va.start, args=(index,))
                t.daemon = True
                t.start()
            else:
                print("Voice Assistant is now OFF")
                self.stop_micro_on_info()
                self.va.stop()
            self.va_on = not self.va_on

        def select_hardware_accelerator():
            HardwareWindow(self)


        def select_microphone():
            check_devices()
            MicrophoneWindow(self)

        def check_devices():
            self.connected_devices = {}
            if self.py_audio is None:
                self.py_audio = pyaudio.PyAudio()
            else:
                self.py_audio.terminate()
                self.py_audio = pyaudio.PyAudio()
            device_count = self.py_audio.get_device_count()
            for i in range(device_count):
                # Get the device info
                device_info = self.py_audio.get_device_info_by_index(i)
                # Check if this device is a microphone (an input device)
                if device_info.get('maxInputChannels') > 0:
                    print(f"Microphone: {device_info.get('name')} , Device Index: {device_info.get('index')}")
                    self.connected_devices[device_info.get('name')] = device_info.get('index')
            # print("\n\n\n")
            # print(self.connected_devices)

        def set_file_path(path):
            self.file_path = path

        def new_file():
            set_file_path("")
            self.editor.delete("1.0", END)
            console.delete("1.0", END)

        def open_file():
            path = askopenfilename(filetypes=[('Python Files', '*.py')])
            if path.endswith('py'):
                with (open(path, 'r') as file):
                    code = file.read()
                    self.editor.delete("1.0", END)
                    self.editor.insert("1.0", code)
                    console.delete("1.0", END)
                    set_file_path(path)
            else:
                print("Fehlermeldung: Es handelt sich nicht um eine Python Datei.")

        def save_as():
            path = asksaveasfilename(filetypes=[('Python Files', '*.py')])
            if not path.endswith('py'):
                path += '.py'
            if not path == '':
                with open(path, 'w') as file:
                    code = self.editor.get("1.0", END)
                    file.write(code)
                    set_file_path(path)

        def save():
            if self.file_path == "":
                path = asksaveasfilename(filetypes=[('Python Files', '*.py')])
                if not path.endswith('py') and not path == '':
                    path += '.py'
            else:
                path = self.file_path
            if not path == '':
                with open(path, 'w') as file:
                    code = self.editor.get("1.0", END)
                    file.write(code)
                    set_file_path(path)

        def read_output():
            while self.process.poll() is None:
                for out in self.process.stdout:
                    if out:
                        console.insert(END, out.decode().strip() + "\n")
                        console.see(END)
                        print(out)
                for err in self.process.stderr:
                    if err:
                        console.insert(END, err.decode().strip() + "\n", 'error')
                        console.see(END)
                        print(err)

        def run():
            t = threading.Thread(target=run_code)
            t.daemon = True
            t.start()

        def run_code():
            save()
            # command = f'python{file_path}'
            self.process = subprocess.Popen(self.file_path, bufsize=0, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE, shell=True)
            # output, error = self.process.communicate()
            # console.insert(END, output.decode('utf-8'))
            # console.insert(END, error.decode('utf-8'))
            # print(output)
            # print(error)
            # print(self.file_path)
            o = threading.Thread(target=read_output)
            o.daemon = True
            o.start()

        def stop():
            console.insert(END, "ToDo: Implement Stop\n")
            subprocess.Popen("taskkill /F /T /PID %i" % self.process.pid, shell=True)
            print("__________________________________________")

        menu_bar = Menu(self)
        file_bar = Menu(menu_bar, tearoff=0)
        file_bar.add_command(label="New", command=new_file)
        file_bar.add_command(label="Open", command=open_file)
        file_bar.add_command(label="Save", command=save)
        file_bar.add_command(label="Save As", command=save_as)
        file_bar.add_command(label="Exit", command=exit)
        menu_bar.add_cascade(label="File", menu=file_bar)

        option_bar = Menu(menu_bar, tearoff=0)
        option_bar.add_command(label="Microphone", command=select_microphone)
        option_bar.add_command(label="Hardware Acceleration", command=select_hardware_accelerator)
        menu_bar.add_cascade(label="Options", menu=option_bar)

        menu_bar.add_command(label="Run", command=run)
        menu_bar.add_command(label="Stop", command=stop)
        menu_bar.add_command(label="Voice", command=voice_assistant)

        self.config(menu=menu_bar)

        self.editor_frame = Frame()
        self.editor_frame.pack(side="top", fill="both", expand=True)

        self.editor_scrollbar = Scrollbar(orient="horizontal")
        self.editor = Text(master=self.editor_frame, wrap=NONE, xscrollcommand=self.editor_scrollbar.set)
        self.editor.pack(side="right", fill="both", expand=True)
        for i in range(24):
            self.editor.insert("end", f"\n")

        linenums = TkLineNumbers(master=self.editor_frame, textwidget=self.editor, justify="center", colors=("#2197db", "#ffffff"), bd=0)
        linenums.pack(fill="y", side="left")
        self.editor.bind("<<Modified>>", lambda event: self.after_idle(linenums.redraw), add=True)

        self.editor_scrollbar.pack(side="bottom", fill='x', expand=False)
        self.editor_scrollbar.config(command=self.editor.xview)

        console_input = Entry(background="#fefefe")
        console_input.pack(fill='x', expand=False)

        console = Text(height=7, background="#fafafa")
        console.pack(fill='x', expand=False)
        console.tag_config('error', foreground="red")

        def info_boxes_resize(event):
            print("resize")
            if self.error.winfo_exists():
                print("error resize")
                self.error.place(relwidth=1.0, relx=.5, y=int(self.editor.winfo_height() - self.info_height + 3),
                                 anchor=CENTER)
            if self.micro.winfo_exists():
                print("micro resize")
                self.micro.place(relwidth=1.0, relx=0, y=int(self.editor.winfo_height() - ((self.info_height + 3) / 3)))
            if self.recording.winfo_exists():
                print("recording resize")
                self.recording.place(relwidth=1.0, relx=.5, y=int(self.editor.winfo_height() - self.info_height + 3),
                                     anchor=CENTER)
            if self.processing.winfo_exists():
                print("processing resize")
                self.processing.place(relwidth=1.0, relx=.5, y=int(self.editor.winfo_height() - self.info_height + 3),
                                      anchor=CENTER)

        self.editor.bind("<Configure>", info_boxes_resize)

        def editor_input_send(event=None):
            content = console_input.get()
            # console.insert(END, content)
            if self.process:
                o = threading.Thread(target=input_def(content))
                o.daemon = True
                o.start()
            console_input.delete(0, END)

        console_input.bind('<Return>', editor_input_send)

        def input_def(content):
            try:
                self.process.stdin.write(bytes(content + '\n', 'utf-8'))
                self.process.stdin.flush()
                console.insert(END, content + "\n")
            except OSError:
                pass


def main():
    MainGUI().mainloop()


if __name__ == '__main__':
    main()
