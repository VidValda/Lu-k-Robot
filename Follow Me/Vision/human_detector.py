# import darknet functions to perform object detections
from darknet.darknet import *

import cv2

# load in our YOLOv4 architecture network
network, class_names, class_colors = load_network("darknet/cfg/custom-yolov4-tiny-detector.cfg", "darknet/data/obj.data", "darknet/backup/custom_best.weights")
#network, class_names, class_colors = load_network("darknet/cfg/custom-yolov4-tiny-detector.cfg", "darknet/data/obj.data", "darknet/backup/firstversion.weights")
width = network_width(network)
height = network_height(network)

# darknet helper function to run detection on image
def darknet_helper(img, width, height):
  darknet_image = make_image(width, height, 3)
  img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
  img_resized = cv2.resize(img_rgb, (width, height),
                              interpolation=cv2.INTER_LINEAR)

  # get image ratios to convert bounding boxes to proper size
  img_height, img_width, _ = img.shape
  width_ratio = img_width/width
  height_ratio = img_height/height

  # run model on darknet style image to get detections
  copy_image_from_bytes(darknet_image, img_resized.tobytes())
  detections = detect_image(network, class_names, darknet_image)
  free_image(darknet_image)
  return detections, width_ratio, height_ratio


 
capture = cv2.VideoCapture(0)
 
while (capture.isOpened()):
    ret, frame = capture.read()

    # create transparent overlay for bounding box

    bbox_array = np.zeros([480,640,4], dtype=np.uint8)

    # call our darknet helper on video frame
    detections, width_ratio, height_ratio = darknet_helper(frame, width, height)

    # loop through detections and draw them on transparent overlay image
    for label, confidence, bbox in detections:
      left, top, right, bottom = bbox2points(bbox)
      left, top, right, bottom = int(left * width_ratio), int(top * height_ratio), int(right * width_ratio), int(bottom * height_ratio)
      frame = cv2.rectangle(frame, (left, top), (right, bottom), class_colors[label], 2)
      frame = cv2.putText(frame, "{} [{:.2f}]".format(label, float(confidence)),
                        (left, top - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        class_colors[label], 2)
    
    
    cv2.imshow('webCam',frame)
    if (cv2.waitKey(1) == ord('s')):
        break
 
capture.release()
cv2.destroyAllWindows()