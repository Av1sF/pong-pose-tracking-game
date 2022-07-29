from multiprocessing import Process, Queue, Lock
from MobileNet_Mediapipe_posedetector import poseMain
from pong_game import gameMain
"""
PONGTRACK 1.3 

Using multiprocessing, a queue of wrist coordinates and image side is passed between the multi-person wrist detector and the pong_game.
But there is a problem where opencv is not using the GPU for pose detection and passing the locks between two processes has caused low 
frame rates -> bad accuracy in detection -> pong game is laggy. 

"""

if __name__ == "__main__":
    lock = Lock()
    q = Queue()
    p1 = Process(target=poseMain, args=(q,lock))
    p2 = Process(target=gameMain, args=(q,lock))

    p1.start()
    p2.start()

    p1.join()
    p2.join()
