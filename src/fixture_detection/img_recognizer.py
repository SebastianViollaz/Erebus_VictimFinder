from ultralytics import YOLO
import os

class img_recognizer():

    def __init__(self) -> None:
       self.model = YOLO("src/fixture_detection/best.pt")  # pretrained YOLOv8n model

    def detect(self,frame): 
        results = self.model(frame)  # return a list of Results objects
        return self.model.names[int(results[0].boxes.cls[0])]
    