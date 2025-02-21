from datetime import datetime, timedelta
import face_recognition
import cv2
import numpy as np


class Detector:
    def __init__(self):
        self._initializeCamera()

        while True:
            frame = self._captureFrame()
            if frame is not None:
                face_locations = self._faceLocations(frame)
                self._displayVideo(frame, face_locations)
                self._saveFaces(frame, face_locations)
            else:
                print('No frame')

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self._releaseResources()

    def _initializeCamera(self):
        self.video_capture = cv2.VideoCapture(0)
        if not self.video_capture.isOpened():
            print("Error: No se pudo abrir la cámara.")
            exit(1)

    def _captureFrame(self):
        ret, frame = self.video_capture.read()
        if not ret:
            return None
        return frame

    def _faceLocations(self, frame):
        frame = frame[:, :, ::-1]
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return face_recognition.face_locations(frame)

    def _displayVideo(self, frame, face_locations):
        for top, right, bottom, left in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        cv2.imshow('Video', frame)

    def _releaseResources(self):
        if self.video_capture is not None:
            self.video_capture.release()
        cv2.destroyAllWindows()

