import threading

from faster_whisper import WhisperModel
import pyaudio
import wave
import os
import keyboard
import time
import audioop


def check_volume(data):
    rms = audioop.rms(data, 2)
    return rms


class VoiceAssistant:

    def __init__(self, owner):
        self.stop_all = False
        self.owner = owner
        self.start_time = 0.0
        self.end_time = 0.0
        self.voice_time_start = 0.0
        self.voice_time_end = 0.0

        self.py_audio = pyaudio.PyAudio()
        self.input_device_index = "0"
        self.temp_audio_file_path = "temp/temp_chunk.wav"
        self.temp_log_file_path = ""
        self.volume_start_threshold = 1000
        self.volume_stop_threshold = 500
        self.recording_timeout = 2

        self.tts_device = "cuda"
        self.tts_compute_type = "float32"
        print("Model stuff....\n")
        # Comment out for testing
        # self.model = WhisperModel("medium", device=self.tts_device, compute_type=self.tts_compute_type)
        print("Model stuff done!\n")

    def stop(self):
        self.stop_all = True
        # self.py_audio.terminate()

    def start(self, microphone_id):
        self.stop_all = False
        if microphone_id:
            self.input_device_index = microphone_id
            print(self.input_device_index)
        self.py_audio = pyaudio.PyAudio()
        for i in range(self.py_audio.get_device_count()):
            print(self.py_audio.get_device_info_by_index(i))
            print(self.py_audio.get_device_info_by_index(i)["defaultSampleRate"])
        self.main()

    def bitstream_to_wave(self, frames, path):
        wf = wave.open(path, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(self.py_audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(16000)
        wf.writeframes(b''.join(frames))
        wf.close()

    def recording(self, stream):
        frames = []
        self.voice_time_start = time.time()
        print("recording:...\n")
        while not self.stop_all:
            data = stream.read(1024)
            frames.append(data)
            if check_volume(data) < self.volume_stop_threshold:
                self.voice_time_end = time.time()
                deltatime = self.voice_time_end - self.voice_time_start
                if deltatime > self.recording_timeout:
                    self.start_time = time.time()
                    break
        print("recording ended")
        self.bitstream_to_wave(frames, self.temp_audio_file_path)

    def main(self):
        self.stop_all = False
        stream = ""
        log = ""
        try:
            stream = self.py_audio.open(format=pyaudio.paInt16, channels=1, rate=16000,
                                        input_device_index=int(self.input_device_index), input=True,
                                        frames_per_buffer=1024)
            while not self.stop_all:
                if check_volume(stream.read(1024)) > 1000:
                    self.recording(stream)
                    print("processing...")
                    segments, info = self.model.transcribe(self.temp_audio_file_path, beam_size=5, language="de",
                                                           condition_on_previous_text=False)
                    text = ""
                    for segment in segments:
                        text += segment.text + " "
                        # print(segment.text)
                    log += text
                    print("processing done")

                    if self.owner:
                        print("Call owner")
                        self.owner.process_va_data(text)

                    self.end_time = time.time()
                    deltatime = self.end_time - self.start_time
                    print("Procession Time: ")
                    print(deltatime)
                    os.remove(self.temp_audio_file_path)
        except OSError:
            # Zu einer Pop Up Message machen
            print("Error. Starting Input Device Failed. Choose a valid microphone.\n"
                  "This error can be cause by missing permissions.\n"
                  "Check your microphone's privacy settings.")
            self.owner.va_on_off = False
        except Exception:
            with open("temp/log.txt", "w") as log_file:
                log_file.write(log)
            self.owner.va_on_off = False
        finally:
            print("Stopping...")
            print("LOG: " + log)
            if stream:
                stream.stop_stream()
                stream.close()

# if __name__ == '__main__':
#     print("Start")
#     start = VoiceAssistant()
#     start.start()
