# Pong Pose Tracking Game

###### Play pong with another friend with pose detection!
###### Warning: bad coding conventions, I wrote this in HS 

It works by...

  • Using [Opencv-python](https://github.com/opencv/opencv-python) to capture frames from a webcam and as a framework
  to run [MobileNet SSD object detection](https://docs.openvino.ai/latest/omz_models_model_mobilenet_ssd.html).
  
  • Modifying the object detection outputs and limiting it to only return bounding boxes of two people per frame, it also returns
  whether the person is detected on the left or right side of the image. 
  
  • Once the two bounding boxes are cropped, each image is entered into [MediaPipe's Holistic](https://google.github.io/mediapipe/solutions/holistic)
  neural network to detect the position of the player's left wrist. Effectively allowing multi-persons pose detection.
  
  • The values of the coordinates of the player's left wrist and which side of the image the person was standing in is then entered into a global queue
  and with multiprocessing, the pong game framework uses the change between an old coordinate and a new coordinate to decide how much the paddle should 
  be moved in the game. 
  
## Try it out from source

Install the following python packages:
  - [MediaPipe](https://pypi.org/project/mediapipe/)
  - [opencv](https://pypi.org/project/opencv-python/)
  - [NumPy](https://pypi.org/project/numpy/)
  
Clone the repo...
```
 $ git clone https://github.com/Av1sF/pong-pose-tracking-game
```

Open the cloned repo in an IDE! 
