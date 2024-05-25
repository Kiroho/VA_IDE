import threading
import traceback

from faster_whisper import WhisperModel
import pyaudio
import wave
import os
import time
import audioop
def check_volume(data):
    rms = audioop.rms(data, 2)
    return rms

class VoiceAssistant:

    def __init__(self, owner, tts_device="cuda", tts_compute_type="float32"):
        self.model = None
        self.stop_all = False
        self.owner = owner
        self.start_time = 0.0
        self.end_time = 0.0
        self.voice_time_start = 0.0
        self.voice_time_end = 0.0

        self.py_audio = pyaudio.PyAudio()
        self.input_device_index = "0"
        self.temp_audio_file_path = "temp/temp_chunk.wav"
        # self.temp_log_file_path = ""
        # self.volume_start_threshold = 1200
        # self.volume_stop_threshold = 700
        # self.recording_timeout = 0.5

        self.tts_device = tts_device
        self.tts_compute_type = tts_compute_type

    def configure_model(self):
        print("Initialize....\n")
        self.owner.create_processing_info("Initialize Voice Assistant...")
        try:
            self.model = WhisperModel("medium", device=self.tts_device, compute_type=self.tts_compute_type)
        except Exception:
            self.owner.stop_micro_on_info()
            self.stop()
            self.owner.va_on = False
            self.owner.create_error_info("Error. Hardware Accelerator is not supported by hardware", timer=3000)
            print("Initialization done!\n")
        finally:
            self.owner.stop_processing_info()
        if not self.stop_all:
            self.owner.create_error_info("Voice Assistant ready", color="light green", timer=2000)
            print("Initialization Error\n")



    def stop(self):
        self.stop_all = True

    def start(self, microphone_id):
        self.stop_all = False
        if not self.model:
            self.configure_model()
        if microphone_id:
            self.input_device_index = microphone_id
            print(self.input_device_index)
        self.py_audio = pyaudio.PyAudio()
        # for i in range(self.py_audio.get_device_count()):
        #     print(self.py_audio.get_device_info_by_index(i))
        #     print(self.py_audio.get_device_info_by_index(i)["defaultSampleRate"])
        if not self.stop_all:
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
        self.owner.create_recording_info(text="Recording...")
        while not self.stop_all:
            data = stream.read(1024)
            frames.append(data)
            if check_volume(data) < self.owner.sliders.get("stop"):
                self.voice_time_end = time.time()
                deltatime = self.voice_time_end - self.voice_time_start
                print(deltatime)
                if deltatime > self.owner.sliders.get("timer"):
                    self.start_time = time.time()
                    break
            else:
                self.voice_time_start = time.time()
        self.bitstream_to_wave(frames, self.temp_audio_file_path)
        print("recording ended")
        self.owner.stop_recording_info()

    def main(self):
        self.stop_all = False
        stream = ""
        log = ""
        try:
            stream = self.py_audio.open(format=pyaudio.paInt16, channels=1, rate=16000,
                                        input_device_index=int(self.input_device_index), input=True,
                                        frames_per_buffer=1024)
            while not self.stop_all:
                if check_volume(stream.read(1024)) > self.owner.sliders.get("start"):
                    self.recording(stream)
                    print("processing...")
                    self.owner.create_processing_info("Processing...")
                    segments, info = self.model.transcribe(self.temp_audio_file_path, beam_size=5, language="de",
                                                           condition_on_previous_text=False)
                    text = ""
                    for segment in segments:
                        text += segment.text + " "
                        # print(segment.text)
                    log += text + "\n"
                    print("processing done")
                    self.owner.stop_processing_info()

                    if self.owner:
                        self.owner.temp_whole_sentence = text
                        # print("Call owner")
                        self.owner.process_va_data(text)

                    self.end_time = time.time()
                    deltatime = self.end_time - self.start_time
                    print(f'Procession Time: {deltatime}')
                    os.remove(self.temp_audio_file_path)
        except OSError:
            self.owner.create_error_info("Error. Starting Input Device Failed. Select a valid Input Device.")
            self.owner.stop_micro_on_info()
            self.owner.stop_processing_info()
            print("Error. Starting Input Device Failed. Choose a valid microphone.\n"
                  "This error can be cause by missing permissions.\n"
                  "Check your microphone's privacy settings.")
            self.owner.va_on = False
        except Exception:
            print("Some Error during recording")
            self.owner.create_error_info("An Error occoured during recording. Stopping recording...")
            self.owner.stop_micro_on_info()
            self.owner.stop_processing_info()
            traceback.print_exc()
            self.owner.va_on = False
        finally:
            print("Stopping...")
            print("LOG: " + log)
            with open("temp/log.txt", "w") as log_file:
                log_file.write(log)
            if stream:
                stream.stop_stream()
                stream.close()

# if __name__ == '__main__':
#     print("Start")
#     start = VoiceAssistant()
#     start.start()
