import cv2 as cv
import numpy as np

# Пороговые значения (уверенность в объекте)
Conf_threshold = 0.4
NMS_threshold = 0.4
 
# Цвет для рамки в формате BGR
COLOR = (0, 0, 255)
 
# Все классы из файла
class_names = []
with open('yolo_classes.txt', 'r') as fl:
    class_names = [cname.strip() for cname in fl.readlines()]
 
# Чтение весов и конфигурации нейронной сети yolov4-tiny
net = cv.dnn.readNet('yolov4-tiny.weights', 'yolov4-tiny.cfg')
 
# Использование CUDA бэкендов
net.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA_FP16)
 
# Определенеи модели
model = cv.dnn_DetectionModel(net)
model.setInputParams(size=(416, 416), scale=1/255, swapRB=True)

def get_car_list(frame: np.ndarray) -> list[tuple]:
    out_car_list = []

    # detect & add to list
    classes, scores, boxes = model.detect(frame, Conf_threshold, NMS_threshold)
    for (classid, score, box) in zip(classes, scores, boxes):
        if class_names[classid] == "dont_show": continue
        name = class_names[classid]

        out_car_list.append((name, boxes))

    return out_car_list

if __name__ == "__main__":
    FILE_NAME = "example.jpeg"
    # обычное чтение изображения
    # frame = cv.imread("example.jpeg")
    
    # Чтение при помощи класса VideoCapture
    cap = cv.VideoCapture(FILE_NAME)
    ret, frame = cap.read()
    
    # Детектирование, выделение в рамку всех объектов
    classes, scores, boxes = model.detect(frame, Conf_threshold, NMS_threshold)
    for (classid, score, box) in zip(classes, scores, boxes):
        if class_names[classid] == "dont_show": continue
        label = f"{class_names[classid]}"
    
        cv.rectangle(frame, box, COLOR, 2)
        cv.putText(frame, label, (box[0], box[1]-10), cv.FONT_HERSHEY_COMPLEX, 0.3, COLOR, 1)
    
    cv.imshow('frame', frame)
    cv.waitKey(0)