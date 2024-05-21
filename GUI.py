import os
import signal
import threading
import time
import tkinter
from tkinter import *
import tkinter.messagebox
from tkinter.filedialog import asksaveasfilename, askopenfilename
import subprocess
from Microphone_Selection import MicrophoneWindow
from Voice_Assistant import VoiceAssistant
import pyaudio
import Editor_Commands as e
from timeit import default_timer as timer


class MainGUI(tkinter.Tk):
    def process_va_data(self, data):
        print(data)

    def __init__(self):
        tkinter.Tk.__init__(self)
        self.file_path = ""
        self.process = None
        self.py_audio = None
        self.microphone_data = ""
        self.connected_devices = {}
        self.va_on_off = False
        self.va = VoiceAssistant(owner=self)

        def voice_assistant():
            if not self.va_on_off:
                print("Voice Assistant is now ON")
                index = 0
                if self.microphone_data and self.connected_devices:
                    index = self.connected_devices[self.microphone_data]
                    print(f'choosen index = {index}')
                t = threading.Thread(target=self.va.start, args=(index,))
                t.daemon = True
                t.start()
            else:
                print("Voice Assistant is now OFF")
                self.va.stop()
            self.va_on_off = not self.va_on_off

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
                    # print(f"Microphone: {device_info.get('name')} , Device Index: {device_info.get('index')}")
                    self.connected_devices[device_info.get('name')] = device_info.get('index')
            # print("\n\n\n")
            # print(self.connected_devices)

        def set_file_path(path):
            self.file_path = path

        def new_file():
            set_file_path("")
            editor.delete("1.0", END)
            console.delete("1.0", END)

        def open_file():
            path = askopenfilename(filetypes=[('Python Files', '*.py')])
            if path.endswith('py'):
                with (open(path, 'r') as file):
                    code = file.read()
                    editor.delete("1.0", END)
                    editor.insert("1.0", code)
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
                    code = editor.get("1.0", END)
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
                    code = editor.get("1.0", END)
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
            my_timer = timer()
            # e.get_cursor_position(editor)
            # get_editor_selected_text()
            # jump_to_row("1")
            # get_editor_cursor_row()
            # editor_copy("1.56", "2")
            # editor_copy()
            # editor_paste()
            # e.delete(editor)
            # e.editor_delete(editor)
            # e.get_editor_cursor_position(editor)
            # e.get_editor_selected_text(editor)
            # e.jump_to_row(editor,"3")
            # e.get_cursor_row(editor)
            # e.copy(editor, "1.56", "2")
            # e.insert_if_statement(editor)
            # e.insert_while(editor, x="a", y="3", o="<=")
            # e.insert_match(editor, "x", "y", "z", row=None, status="text")
            # e.insert_try(editor, excep="ValueError", final=True)
            # e.insert_infinite_loop(editor)
            # e.insert_print(editor, text="hallo, wie gehts?")
            # e.insert_input(editor)
            # e.insert_timer(editor)
            # e.insert_thread(editor, target="my_cool_function")

            print(f'Time: {timer() - my_timer}')

        def pop_up_info():
            img = PhotoImage()
            info = Label(self, text="INFORMATION!", image=img, compound=CENTER, font=('', 12), bg='light green',
                         width=self.winfo_width(), height=25)
            info.place(relx=.5, rely=0.7, anchor=CENTER)
            self.after(2000, info.destroy)

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
        option_bar.add_command(label="Hardware Acceleration", command=pop_up_info)
        menu_bar.add_cascade(label="Options", menu=option_bar)

        menu_bar.add_command(label="Run", command=run)
        menu_bar.add_command(label="Stop", command=stop)
        menu_bar.add_command(label="Voice", command=voice_assistant)

        self.config(menu=menu_bar)

        editor_scrollbar = Scrollbar(orient="horizontal")
        editor = Text(wrap=NONE, xscrollcommand=editor_scrollbar.set)
        editor.pack(fill=BOTH, expand=True)

        editor_scrollbar.pack(fill='x', expand=False)
        editor_scrollbar.config(command=editor.xview)

        console_input = Entry(background="#fefefe")
        console_input.pack(fill='x', expand=False)

        console = Text(height=7, background="#fafafa")
        console.pack(fill='x', expand=False)
        console.tag_config('error', foreground="red")


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
