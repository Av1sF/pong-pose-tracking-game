from multiprocessing import Process, Queue, Lock
import random

def makenumber(queue, lock):
    #make 2 random numbers // add to queue
    while True:
        with lock:
            num1 = random.randint(1,10)
            num2 = random.randint(10,20)
            print(f"{num1} {num2}")
            queue.put([num1, num2])




def timesnum(queue, lock):
    #take 2 random number from queue and print them // read from queue
    while True:
        with lock:
            if not queue.empty():
                lst = queue.get()
                # print(f"fi {lst[0]} nief {lst[1]}")


if __name__ == "__main__":
    lock = Lock()
    q = Queue()
    p1 = Process(target=makenumber, args=(q,lock))
    p2 = Process(target=timesnum, args=(q,lock))

    p1.start()
    p2.start()

    p1.join()
    p2.join()
