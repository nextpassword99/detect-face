import face_recognition
import cv2


class Detector:
    def _videoCapture(self):
        video_capture = cv2.VideoCapture(0)
        ret, frame = video_capture.read()

        return frame

    def _faceLocations(self, frame):
        face_locations = face_recognition.face_locations(frame)
        return face_locations

