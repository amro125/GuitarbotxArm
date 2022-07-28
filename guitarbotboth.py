import os
import sys
import time
import numpy as np
from GuitarBotUDP import GuitarBotUDP
from queue import Queue
from threading import Thread


def third_poly(q_i, q_f, time):
    traj_t = np.arange(0,time,0.005)
    dq_i = 0
    dq_f = 0
    a0 = q_i
    a1 = dq_i
    a2 = 3*(q_f-q_i)/(time**2)
    a3 = 2*(q_i-q_f)/(time**3)
    traj_pos = a0 + a1 * traj_t + a2 * traj_t ** 2 + a3 * traj_t ** 3
    return traj_pos


def fifth_poly(q_i, q_f, time):
# np.linspace
# time/0.005
    traj_t = np.arange(0,time,0.005)
    dq_i = 0
    dq_f = 0
    ddq_i = 0
    ddq_f = 0
    a0 = q_i
    a1 = dq_i
    a2 = 0.5*ddq_i
    a3 = 1/(2*time**3)*(20*(q_f-q_i)-(8*dq_f+12*dq_i)*time-(3*ddq_f-ddq_i)*time**2)
    a4 = 1/(2*time**4)*(30*(q_i-q_f)+(14*dq_f+16*dq_i)*time+(3*ddq_f-2*ddq_i)*time**2)
    a5 = 1/(2*time**5)*(12*(q_f-q_i)-(6*dq_f+6*dq_i)*time-(ddq_f-ddq_i)*time**2)
    traj_pos = a0 +a1*traj_t +a2*traj_t**2 + a3*traj_t**3 + a4*traj_t**4 + a5*traj_t**5
    return traj_pos




def setup():
    for a in arms:
        a.set_simulation_robot(on_off=False)
        a.motion_enable(enable=True)
        a.clean_warn()
        a.clean_error()
        a.set_mode(0)
        a.set_state(0)
        a.set_position(*initial_pose, wait=True)

def rightHand(qplay):
    arm1.set_mode(1)
    arm1.set_state(0)
    qplay.get()
    # time.sleep(5)
    while True:
        guitarbot_udp.send_msg_picker(ipickercommand=1, bstartpicker=1, pgain=3000, dgain=30, ipickerpos=-20, ipickervel=5, ipickeracc=100)
        fingerq.put(1)
        strumq.get()
        for i in range(len(qx)):

            #run command
            start_time = time.time()
            movepose = [qx[i],qy[i],qz[i], -90, 0, -0]
            # print(qz[i])

            arm1.set_servo_cartesian(movepose)
            tts = time.time() - start_time
            sleep = 0.005 - tts

            if tts > 0.005:
                sleep = 0
            print(tts)
            time.sleep(sleep)

        guitarbot_udp.send_msg_picker(ipickercommand=1, bstartpicker=1, pgain=3000, dgain=30, ipickerpos=10, ipickervel=5, ipickeracc=100)
        fingerq.put(1)
        strumq.get()
        for i in range(len(qx)):

            #run command
            start_time = time.time()
            movepose = [rqx[i],rqy[i],rqz[i], -90, 0, -0]
            arm1.set_servo_cartesian(movepose)
            tts = time.time() - start_time
            sleep = 0.005 - tts
            print(tts)
            if tts > 0.005:
                sleep = 0
            time.sleep(sleep)
        
        
        

initial_pose = [657.8, 274, 369.3, -90, 0, -0]
final_pose = [657.8, 274, 269.3, -90, 0, -0]


if __name__ == "__main__":
    UDP_IP = "192.168.1.50"
    UDP_PORT = 1001
    guitarbot_udp = GuitarBotUDP(UDP_IP,UDP_PORT)
    sleeptime = 4
    ROBOT = "xArms"
    PORT = 5004
    sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
    from xarm.wrapper import XArmAPI
    strumq = Queue()
    fingerq = Queue()
    global arm1
    arm1 = XArmAPI('192.168.1.215')

    arms = [arm1]
    totalArms = len(arms)

    setup()
    print("setup")
    

    timet = .15 #second

    
    qx = fifth_poly(initial_pose[0],final_pose[0],timet)
    qy = fifth_poly(initial_pose[1],final_pose[1],timet)
    qz = fifth_poly(initial_pose[2],final_pose[2],timet)

    rqx = qx[::-1] 
    rqy = qy[::-1] 
    rqz = qz[::-1] 
    xArm = Thread(target=rightHand, args=(strumq,))
    xArm.start()
    
    
    pos =int(input("pick degrees"))
    guitarbot_udp.send_msg_picker(ipickercommand=1, bstartpicker=1, pgain=3000, dgain=30, ipickerpos=pos, ipickervel=5, ipickeracc=100)


    input("start")
    
   
    
    for x in range(10):
        iplaycommand = 1
        bstartplay = [1, 1, 1, 1, 1, 1]
        ifretnumber = [3, 3, 2, 2, 1, 2]
        bdamp = [0, 0, 0, 0, 0, 0]
        bopenstr = [1, 0, 0, 0, 0, 0]
        bvibrato = [0, 0, 0, 0, 0, 0]
        bglide = [0, 0, 0, 0, 0, 0]
        tnotelen = [3500, 3500, 3500, 3500, 3500, 350]
        guitarbot_udp.send_msg_left(iplaycommand, bstartplay, ifretnumber, bdamp, bopenstr, bvibrato, bglide)
        strumq.put(1)
        fingerq.get()
        # time.sleep(0.2)
        # guitarbot_udp.send_msg_picker(ipickercommand=1, bstartpicker=1, pgain=8000, dgain=80, ipickerpos=-10, ipickervel=5, ipickeracc=100)
        # time.sleep(sleeptime)

        iplaycommand = 1
        bstartplay = [1,1,1,1,1,1]
        ifretnumber = [3, 3, 2, 2, 2, 2]
        bdamp = [0,0,0,0,0,0]
        bopenstr = [1,1,0,0,0,1]
        bvibrato = [0,0,0,0,0,0]
        bglide = [0,0,0,0,0,0]
        tnotelen = [3500, 3500, 3500, 3500, 3500, 3500]
        guitarbot_udp.send_msg_left(iplaycommand, bstartplay, ifretnumber, bdamp, bopenstr, bvibrato, bglide)
        strumq.put(1)
        fingerq.get()
        # time.sleep(0.2)
        # guitarbot_udp.send_msg_picker(ipickercommand=1, bstartpicker=1, pgain=8000, dgain=80, ipickerpos=10, ipickervel=5,
        #                             ipickeracc=100)
        # time.sleep(sleeptime)
    


    




    
