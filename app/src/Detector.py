import face_recognition
import cv2

from app.src.Compare import Compare

class Detector:
    def __init__(self):
        self.compare = Compare(face_recognition)
        self.video_capture = None

    def start(self):
        self._initialize_camera()
        try:
            while True:
                frame = self._capture_frame()
                if frame is not None:
                    face_locations = self._face_locations(frame)
                    self._display_video(frame, face_locations)
                    self.compare._saveFaces(frame, face_locations)
                else:
                    print('No frame')

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        finally:
            self._release_resources()

    def _initialize_camera(self):
        self.video_capture = cv2.VideoCapture(0)
        if not self.video_capture.isOpened():
            print("Error: No se pudo abrir la cámara.")
            exit(1)

    def _capture_frame(self):
        ret, frame = self.video_capture.read()
        return frame if ret else None

    def _face_locations(self, frame):
        frame = frame[:, :, ::-1]
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return face_recognition.face_locations(frame)

    def _display_video(self, frame, face_locations):
        for top, right, bottom, left in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        cv2.imshow('Video', frame)

    def _release_resources(self):
        if self.video_capture is not None:
            self.video_capture.release()
        cv2.destroyAllWindows()

