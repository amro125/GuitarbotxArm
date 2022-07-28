import socket
import time



class GuitarBotUDP:

    def __init__(self,UDP_IP, UDP_PORT):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_ip = UDP_IP
        self.udp_port = UDP_PORT
        self.router_left = bytes('/lguitar', 'utf8')
        self.router_picker = bytes('/rguitar', 'utf8')

    def send_msg_left(self, iplaycommand, bstartplay, ifretnumber, bdamp, bopenstr, bvibrato, bglide, tnotelen):
        stringCount = 6
        bstartplay_int = 0
        bdamp_int = 0
        bopenstr_int = 0
        bvibrato_int = 0
        bglide_int = 0
        ifretnumber_byte = [b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00']
        tnotelen_byte = [b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00']
        for i in range(stringCount):
            bstartplay_int = bstartplay_int * 2 + bstartplay[i]
            bdamp_int = bdamp_int * 2 + bdamp[i]
            bopenstr_int = bopenstr_int * 2 + bopenstr[i]
            bvibrato_int = bvibrato_int * 2 + bvibrato[i]
            bglide_int = bglide_int * 2 + bglide[i]
            ifretnumber_byte[i] = ifretnumber[i].to_bytes(1, 'little')
            tnotelen_byte[i] = tnotelen[i].to_bytes(2, 'little')
        print(ifretnumber)
        router = self.router_left
        iplaycommand = iplaycommand.to_bytes(1, 'little')
        bstartplay = bstartplay_int.to_bytes(1, 'little')
        bdamp = bdamp_int.to_bytes(1, 'little')
        bopenstr = bopenstr_int.to_bytes(1, 'little')
        bvibrato = bvibrato_int.to_bytes(1, 'little')
        bglide = bglide_int.to_bytes(1, 'little')

        ifretnumber_merge = ifretnumber_byte[0]
        tnotelen_merge = tnotelen_byte[0]

        for i in range(stringCount - 1):
            ifretnumber_merge += ifretnumber_byte[i + 1]
            tnotelen_merge += tnotelen_byte[i + 1]

        message = router
        message += iplaycommand
        message += bstartplay
        message += ifretnumber_merge
        message += bdamp
        message += bopenstr
        message += bvibrato
        message += bglide
        message += tnotelen_merge
        message += b'\x00'
        self.sock.sendto(message, (self.udp_ip, self.udp_port))
        return 0

    def send_msg_picker(self, ipickercommand, bstartpicker, pgain,dgain,ipickerpos,ipickervel,ipickeracc):
        router = self.router_picker
        ipickercommand_byte = ipickercommand.to_bytes(1, 'little')
        bstartpicker_byte = bstartpicker.to_bytes(1, 'little')
        pgain_byte = pgain.to_bytes(2, 'little')
        dgain_byte = dgain.to_bytes(1, 'little')
        ipickerpos_byte = ipickerpos.to_bytes(1, 'little', signed=True)
        ipickervel_byte = ipickervel.to_bytes(1, 'little')
        ipickeracc_byte = ipickeracc.to_bytes(2, 'little')

        message = router
        message += ipickercommand_byte
        message += bstartpicker_byte
        message += pgain_byte
        message += dgain_byte
        message += ipickerpos_byte
        message += ipickervel_byte
        message += ipickeracc_byte
        self.sock.sendto(message, (self.udp_ip, self.udp_port))
        return 0

def main():
    UDP_IP = "169.254.60.100"
    UDP_PORT = 1001
    guitarbot_udp = GuitarBotUDP(UDP_IP,UDP_PORT)
    sleeptime = 4

    #time.sleep(5)
    # iplaycommand = 2
    # bstartplay = [0, 0, 0, 1, 0, 0]
    # ifretnumber = [4, 4, 4, 2, 3, 4]
    # bdamp = [1, 0, 0, 0, 0, 0]
    # bopenstr = [0, 0, 0, 0, 0, 0]
    # bvibrato = [0, 0, 0, 0, 0, 0]
    # bglide = [0, 0, 0, 0, 0, 0]
    # tnotelen = [50, 50, 50, 50, 50, 50]
    #
    # lguitar.send_msg(iplaycommand, bstartplay, ifretnumber, bdamp, bopenstr, bvibrato, bglide, tnotelen)
    # bstartplay = [0, 0, 1, 0, 0, 0]
    # ifretnumber = [4, 4, 3, 2, 4, 4]
    # tnotelen = [100, 100, 100, 100, 100, 100]
    # time.sleep(0.25)
    # lguitar.send_msg(iplaycommand, bstartplay, ifretnumber, bdamp, bopenstr, bvibrato, bglide, tnotelen)
    # bstartplay = [0, 0, 1, 0, 0, 0]
    # ifretnumber = [4, 4, 2, 2, 4, 4]
    # tnotelen = [100, 100, 100, 100, 100, 100]
    # time.sleep(0.25)
    # lguitar.send_msg(iplaycommand, bstartplay, ifretnumber, bdamp, bopenstr, bvibrato, bglide, tnotelen)
    # bstartplay = [1, 0, 0, 0, 0, 0]
    # ifretnumber = [5, 4, 3, 2, 4, 4]
    # tnotelen = [300, 300, 300, 300, 300, 300]
    # time.sleep(0.5)
    # lguitar.send_msg(iplaycommand, bstartplay, ifretnumber, bdamp, bopenstr, bvibrato, bglide, tnotelen)
    # bstartplay = [1, 0, 0, 0, 0, 0]
    # ifretnumber = [5, 3, 3, 2, 4, 4]
    # tnotelen = [300, 300, 300, 300, 300, 300]
    # time.sleep(0.5)
    # lguitar.send_msg(iplaycommand, bstartplay, ifretnumber, bdamp, bopenstr, bvibrato, bglide, tnotelen)
    # bstartplay = [0, 1, 0, 0, 0, 0]
    # ifretnumber = [5, 3, 3, 2, 4, 4]
    # tnotelen = [100, 100, 100, 100, 100, 100]
    # time.sleep(0.25)
    # lguitar.send_msg(iplaycommand, bstartplay, ifretnumber, bdamp, bopenstr, bvibrato, bglide, tnotelen)
    # lguitar.send_msg(iplaycommand, bstartplay, ifretnumber, bdamp, bopenstr, bvibrato, bglide, tnotelen)
    # bstartplay = [1, 0, 0, 0, 0, 0]
    # ifretnumber = [5, 3, 3, 2, 4, 4]
    # tnotelen = [300, 300, 300, 300, 300, 300]
    # time.sleep(0.5)
    # lguitar.send_msg(iplaycommand, bstartplay, ifretnumber, bdamp, bopenstr, bvibrato, bglide, tnotelen)
    # bstartplay = [1, 0, 0, 0, 0, 0]
    # ifretnumber = [5, 3, 3, 2, 4, 4]
    # tnotelen = [300, 300, 300, 300, 300, 300]
    # time.sleep(0.5)
    # lguitar.send_msg(iplaycommand, bstartplay, ifretnumber, bdamp, bopenstr, bvibrato, bglide, tnotelen)
    # bstartplay = [0, 0, 1, 0, 0, 0]
    # ifretnumber = [4, 4, 2, 2, 4, 4]
    # tnotelen = [100, 100, 100, 100, 100, 100]
    # time.sleep(0.25)
    # lguitar.send_msg(iplaycommand, bstartplay, ifretnumber, bdamp, bopenstr, bvibrato, bglide, tnotelen)
    # bstartplay = [0, 0, 1, 0, 0, 0]
    # ifretnumber = [4, 4, 2, 2, 4, 4]
    # tnotelen = [100, 100, 100, 100, 100, 100]
    # time.sleep(0.25)
    # lguitar.send_msg(iplaycommand, bstartplay, ifretnumber, bdamp, bopenstr, bvibrato, bglide, tnotelen)
    # bstartplay = [0, 0, 1, 0, 0, 0]
    # ifretnumber = [4, 4, 2, 2, 4, 4]
    # tnotelen = [100, 100, 100, 100, 100, 100]
    # time.sleep(0.25)
    # lguitar.send_msg(iplaycommand, bstartplay, ifretnumber, bdamp, bopenstr, bvibrato, bglide, tnotelen)
    # bstartplay = [0, 0, 1, 0, 0, 0]
    # ifretnumber = [4, 4, 2, 2, 4, 4]
    # tnotelen = [100, 100, 100, 100, 100, 100]
    # time.sleep(0.25)
    # lguitar.send_msg(iplaycommand, bstartplay, ifretnumber, bdamp, bopenstr, bvibrato, bglide, tnotelen)

    iplaycommand = 1
    bstartplay = [1, 1, 1, 1, 1, 1]
    ifretnumber = [3, 3, 2, 2, 1, 2]
    bdamp = [0, 0, 0, 0, 0, 0]
    bopenstr = [1, 0, 0, 0, 0, 0]
    bvibrato = [0, 0, 0, 0, 0, 0]
    bglide = [0, 0, 0, 0, 0, 0]
    tnotelen = [3500, 3500, 3500, 3500, 3500, 350]
    guitarbot_udp.send_msg_left(iplaycommand, bstartplay, ifretnumber, bdamp, bopenstr, bvibrato, bglide, tnotelen)
    time.sleep(0.2)
    guitarbot_udp.send_msg_picker(ipickercommand=1, bstartpicker=1, pgain=8000, dgain=80, ipickerpos=-10, ipickervel=5, ipickeracc=100)
    time.sleep(sleeptime)

    iplaycommand = 1
    bstartplay = [1,1,1,1,1,1]
    ifretnumber = [3, 3, 2, 2, 2, 2]
    bdamp = [0,0,0,0,0,0]
    bopenstr = [1,1,0,0,0,1]
    bvibrato = [0,0,0,0,0,0]
    bglide = [0,0,0,0,0,0]
    tnotelen = [3500, 3500, 3500, 3500, 3500, 3500]
    guitarbot_udp.send_msg_left(iplaycommand, bstartplay, ifretnumber, bdamp, bopenstr, bvibrato, bglide, tnotelen)
    time.sleep(0.2)
    guitarbot_udp.send_msg_picker(ipickercommand=1, bstartpicker=1, pgain=8000, dgain=80, ipickerpos=10, ipickervel=5,
                                  ipickeracc=100)
    time.sleep(sleeptime)

    iplaycommand = 1
    bstartplay = [1,1,1,1,1,1]
    ifretnumber = [1, 3, 3, 2, 1, 1]
    bdamp = [0,0,0,0,0,0]
    bopenstr = [0,0,0,0,0,0]
    bvibrato = [0,0,0,0,0,0]
    bglide = [0,0,0,0,0,0]
    tnotelen = [3500, 3500, 3500, 3500, 3500, 3500]
    guitarbot_udp.send_msg_left(iplaycommand, bstartplay, ifretnumber, bdamp, bopenstr, bvibrato, bglide, tnotelen)
    time.sleep(0.2)
    guitarbot_udp.send_msg_picker(ipickercommand=1, bstartpicker=1, pgain=8000, dgain=80, ipickerpos=-10, ipickervel=5,
                                  ipickeracc=100)
    time.sleep(sleeptime)
    iplaycommand = 1
    bstartplay = [1,1,1,1,1,1]
    ifretnumber = [3, 2, 3, 2, 1, 3]
    bdamp = [0,0,0,0,0,0]
    bopenstr = [0,0,1,1,1,0]
    bvibrato = [0,0,0,0,0,0]
    bglide = [0,0,0,0,0,0]
    tnotelen = [3500, 3500, 3500, 3500, 3500, 3500]
    guitarbot_udp.send_msg_left(iplaycommand, bstartplay, ifretnumber, bdamp, bopenstr, bvibrato, bglide, tnotelen)

if __name__ == '__main__':
    main()
