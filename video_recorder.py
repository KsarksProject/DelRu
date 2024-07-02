import cv2
import numpy as np
import pyautogui
import threading

class VideoRecorder:
    def __init__(self, filename="output.avi", fps=20.0):
        self.filename = filename
        self.fps = fps
        self.screen_size = pyautogui.size()
        self.fourcc = cv2.VideoWriter_fourcc(*"MJPG")
        self.out = cv2.VideoWriter(self.filename, self.fourcc, self.fps, self.screen_size)
        self.is_recording = False

    def start(self):
        self.is_recording = True
        self.thread = threading.Thread(target=self.record)
        self.thread.start()

    def record(self):
        while self.is_recording:
            img = pyautogui.screenshot()
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.out.write(frame)

    def stop(self):
        self.is_recording = False
        self.thread.join()
        self.out.release()
