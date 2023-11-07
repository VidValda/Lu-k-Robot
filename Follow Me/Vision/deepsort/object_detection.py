# import darknet functions to perform object detections
from darknet.darknet import *

import cv2
class HumanDetector:

    def __init__(self):
        # load in our YOLOv4 architecture network
        network, class_names, class_colors = load_network("darknet/cfg/custom-yolov4-tiny-detector.cfg", "darknet/data/obj.data", "darknet/backup/custom_best.weights")
        #network, class_names, class_colors = load_network("darknet/cfg/custom-yolov4-tiny-detector.cfg", "darknet/data/obj.data", "darknet/backup/firstversion.weights")
        width = network_width(network)
        height = network_height(network)
        self.network = network
        self.class_names = class_names
        self.class_colors = class_colors
        self.width = width
        self.height = height
        self.detections = None
        self.width_ratio = None
        self.height_ratio = None


    # darknet helper function to run detection on image
    def detect(self,img):
        darknet_image = make_image(self.width, self.height, 3)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_resized = cv2.resize(img_rgb, (self.width, self.height),
                                    interpolation=cv2.INTER_LINEAR)

        # get image ratios to convert bounding boxes to proper size
        img_height, img_width, _ = img.shape
        width_ratio = img_width/self.width
        height_ratio = img_height/self.height

        # run model on darknet style image to get detections
        copy_image_from_bytes(darknet_image, img_resized.tobytes())
        detections = detect_image(self.network, self.class_names, darknet_image)
        free_image(darknet_image)
        self.detections = detections
        self.width_ratio = width_ratio
        self.height_ratio = height_ratio
        return detections, width_ratio, height_ratio
    
    def draw(self,img):
        image_copy = np.copy(img)
        # loop through detections and draw them on transparent overlay image
        for label, confidence, bbox in self.detections:
            left, top, right, bottom = bbox2points(bbox)
            left, top, right, bottom = int(left * self.width_ratio), int(top * self.height_ratio), int(right * self.width_ratio), int(bottom * self.height_ratio)
            image_copy = cv2.rectangle(image_copy, (left, top), (right, bottom), self.class_colors[label], 2)
            image_copy = cv2.putText(image_copy, "{} [{:.2f}]".format(label, float(confidence)),
                                (left, top - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                self.class_colors[label], 2)
        return image_copy