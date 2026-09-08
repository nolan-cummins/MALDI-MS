from PySide6.QtCore import QThread, Signal, Slot, QMutex, QMutexLocker
from time import sleep
import os
import numpy as np
import cv2

class processVideo(QThread):
    display_out = Signal(tuple)
    frame_out = Signal(object)
    
    def __init__(self):
        super().__init__()

        self.cap = None
        self.fps = 1
        self.running = True
        self.pause = False
        self.display_fps = 30
        self.name = ''
        self.file = ''
        self.init_mutex = QMutex()
        self.pause_mutex = QMutex()
            
    @Slot(str)
    def loadVideo(self, file):
        try:
            with QMutexLocker(self.init_mutex):
                self.cap = cv2.VideoCapture(file)
                self.fps = self.cap.get(cv2.CAP_PROP_FPS)
                self.name = os.path.basename(file)
                self.file = file
            print(f"Loading video: {self.name}")
        except Exception as e:
            print(f"Error loading video {self.name}: {e}")

    @Slot()
    def clearVideo(self):
        with QMutexLocker(self.init_mutex):
            self.cap = None

    def capExists(self):
        with QMutexLocker(self.init_mutex):
            return self.cap is not None
    
    def videoState(self, paused):
        with QMutexLocker(self.pause_mutex):
            self.pause = paused
    
    @Slot()
    def restartVideo(self):
        with QMutexLocker(self.init_mutex):
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    
    def run(self):
        tick_freq = cv2.getTickFrequency()
        fps_tick = 0
        last_tick = 0
        while self.running:
            with QMutexLocker(self.pause_mutex):
                paused = self.pause

            if paused:
                sleep(0.1)
                continue

            if self.cap is not None:
                with QMutexLocker(self.init_mutex):
                    cap = self.cap
                    display_time = 1/self.display_fps
                    frame_time = 1/self.fps
                    fps = 0
                try:
                    start_tick = cv2.getTickCount()
                    ret, frame = cap.read()
                    if not ret:
                        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    if fps_tick == 0:
                        fps_tick = cv2.getTickCount()
                    if last_tick == 0:
                        last_tick = cv2.getTickCount()

                    if frame is not None:
                        try:
                            ms = int(cap.get(cv2.CAP_PROP_POS_MSEC))
                            current_tick = cv2.getTickCount()
                            if (current_tick - fps_tick) / tick_freq >= display_time:
                                fps_tick = current_tick
                                if current_tick - last_tick > 0:
                                    fps = tick_freq / (current_tick - last_tick)
                                self.display_out.emit((frame, fps, ms/1000.0, False))
                        except Exception as e:
                            print(f'Error emitting display frame: {e}')
                        self.frame_out.emit(frame)

                    last_tick = cv2.getTickCount()
                        
                    process_time = (cv2.getTickCount() - start_tick) / tick_freq
                    sleep_time = max(frame_time - process_time, 0)
                    sleep(sleep_time)
                except Exception as e:
                    print(e)
        if self.cap is not None:
            self.cap.release()

    @Slot()
    def stop(self):
        self.running = False
        self.quit()
        self.wait()