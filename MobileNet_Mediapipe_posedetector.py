import cv2
import numpy as np
import mediapipe as mp
import time


"""
Python Ver. 3.9

Combines the use of MobileNet SDD object detection and MediaPipe pose estimation for
limited multi-person tracking. Has the purpose of 1 person detection each on the left and right side
of the camera and outputs the x,y coordinates of right wrist. (with inheritance) 

[all of these could be adjusted]
Max no. of people detected: 2

Max no. of people detected on the left: 1 
Max no. of people detected on the right: 1 

if x,y coordinates of left wrist are not available it returns None

To do list:
    
    - make a variable that measures the half way point of the camera and variables for maxLPeople and such 
    for easier modification in the future. 

    - install opencv gpu ver. 


"""

class posedetector():
    #detects position of right wrist with MediaPipe pose estimator
    def __init__(self, mode=False, complexity=1, smoothLm=True, segmentation=False,
                 smoothSegmentation=True, detectionCon=0.5, trackCon=0.5):

        self.mode = mode
        self.complexity = complexity
        self.smoothLm = smoothLm
        self.segmentation = segmentation
        self.smoothSegmentation = smoothSegmentation
        self.detectionCon = detectionCon
        self.trackCon = trackCon


        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.complexity, self.smoothLm, self.segmentation,
                            self.smoothSegmentation, self.detectionCon, self.trackCon)

    def findpose(self, img):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)

        if self.results.pose_landmarks:
            self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
        return img

    def findposition(self, img):
        # wristPosition = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                # // lm 16 = right wrist
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)

                if id == 16:
                    cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)
                    # print(f"{id},\n  x:{cx} \n y:{cy}")
                    return cx, cy




class personsegmentation(posedetector):
    def __init__(self, thres=0.5, nms_threshold=0.2):
        super().__init__() # inherit all methods and properities

        self.thres = thres
        self.nms_threshold = nms_threshold
        self.classNames = []
        self.configPath = "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
        self.weightsPath = "frozen_inference_graph.pb"
        self.classFile = 'coco.names'

        with open(self.classFile, "rt") as f:
            self.classNames = f.read().rstrip("\n").split("\n")

        self.net = cv2.dnn_DetectionModel(self.weightsPath, self.configPath)
        self.net.setInputSize(320, 320)
        self.net.setInputScale(1.0 / 127.5)
        self.net.setInputMean((127.5, 127.5, 127.5))
        self.net.setInputSwapRB(True)


    def findperson(self, img, width, height, persondetected=0, leftpersondetected=0,
                   rightpersondetected=0):
        classIds, confs, bbox = self.net.detect(img, confThreshold=self.thres)
        bbox = list(bbox)
        confs = list(np.array(confs).reshape(1, -1)[0])
        confs = list(map(float, confs))

        indices = cv2.dnn.NMSBoxes(bbox, confs, self.thres, self.nms_threshold)

        wristCoords = 0

        side = 0

        for i in indices:
            i = str(i)
            i = int(i[0])
            box = bbox[i]

            if self.classNames[classIds[i] - 1] == "person" and persondetected < 2:

                persondetected += 1
                x, y, w, h = box[0], box[1], box[2], box[3]


                if x + (w / 2) < width and leftpersondetected < 1:
                    # left side (takes middle of box x value to determine which side it is on)
                    leftpersondetected += 1
                    cv2.rectangle(img, (x, y), (x + w, h + y), color=(0, 255, 0), thickness=2)
                    cv2.putText(img,
                                f"{self.classNames[classIds[i] - 1].upper()} on the left {str(round(confs[0] * 100, 2))}%",
                                (box[0] + 10, box[1] + 30),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                    leftcroppedimg = img[y:y + h, x:x + w]
                    # display bbox + pose detection

                    leftcroppedimg, wristCoords = personsegmentation.leftboundingBox(self, leftcroppedimg)
                    # print(wristCoords)

                    side = 'L'
                    # cv2.imshow("left person", leftcroppedimg)

                elif x + (w / 2) > width and rightpersondetected < 1:  # right side
                    rightpersondetected += 1
                    cv2.rectangle(img, (x, y), (x + w, h + y), color=(0, 255, 0), thickness=2)
                    cv2.putText(img,
                                f"{self.classNames[classIds[i] - 1].upper()} on the right {str(round(confs[0] * 100, 2))}%",
                                (box[0] + 10, box[1] + 30),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                    rightcroppedimg = img[y:y + h, x:x + w]
                    rightcroppedimg, wristCoords = personsegmentation.leftboundingBox(self, rightcroppedimg)
                    side = 'R'
                    # cv2.imshow("right person", rightcroppedimg)


        return img, wristCoords, side

    # use mediapipe for individual pose detector

    def leftboundingBox(self, Lcroppedimg):
        Lcroppedimg = personsegmentation.findpose(self, Lcroppedimg)  # draws pose detection
        # coords is a tuple here
        coords = personsegmentation.findposition(self, Lcroppedimg) \
                     if type(personsegmentation.findposition(self, Lcroppedimg)) is not None else None
        # ternary operator prevents, cannot unpack non-iterable nonetype object error
        # and instead assigns None as coordinates
        print(coords)

        return Lcroppedimg, coords

    def rightboundingBox(self, Rcroppedimg):
        Rcroppedimg = personsegmentation.findpose(self, Rcroppedimg)
        coords = personsegmentation.findposition(self, Rcroppedimg) \
                     if type(personsegmentation.findposition(self, Rcroppedimg)) is not None else None
        return Rcroppedimg, coords


def poseMain(q, lock):
    cap = cv2.VideoCapture(0)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    cap.set(3, 1280)
    cap.set(4, 720)
    cap.set(10, 150)
    detector = personsegmentation()
    pTime = 0

    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        img, wristCoords, side = detector.findperson(img, width, height)
        print(side)
        if wristCoords != None:
            with lock:
                q.put([wristCoords, side])

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 0), 3)


        cv2.imshow("Output", img)
        k = cv2.waitKey(33)
        if k == 27:  # Esc key to stop
            break

# if __name__ == "__main__":
#     poseMain()