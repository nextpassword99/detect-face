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

    def _showVideo(self, frame, face_locations):
        for top, right, bottom, left in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        cv2.imshow('Video', frame)
