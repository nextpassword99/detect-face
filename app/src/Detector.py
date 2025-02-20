import face_recognition
import cv2


class Detector:
    def _videoCapture(self):
        video_capture = cv2.VideoCapture(0)
        ret, frame = video_capture.read()

        return frame
