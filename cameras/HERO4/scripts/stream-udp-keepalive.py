import socket
import sys
import time
import threading


class Heartbeat:
    def __init__(self, ip='10.5.5.9', port=8554, interval=2500, keepalive_cmd=2):
        self.ip = ip
        self.port = port
        self.interval = interval
        self.keepalive_cmd = keepalive_cmd
        self.keepalive_message = self.get_command_msg(keepalive_cmd)
        self.thread = None
        if sys.version_info.major >= 3:
            self.keepalive_message = bytes(self.keepalive_message, "utf-8")

    @staticmethod
    def get_command_msg(payload):
        return "_GPHD_:%u:%u:%d:%1lf\n" % (0, 0, payload, 0)

    def start_pulse(self):
        if self.thread is None:
            self.thread = threading.Thread(target=self.pulse)
            self.thread.should_pulse = True
            self.thread.start()

    def stop_pulse(self):
        if self.thread is not None:
            self.thread.should_pulse = False
            self.thread = None

    def pulse(self):
        while getattr(threading.current_thread(), 'should_pulse', False):
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(self.keepalive_message, (self.ip, self.port))
            time.sleep(self.interval/1000)

if __name__ == '__main__':
    hb = Heartbeat()
    hb.start_pulse()
    time.sleep(10)
    while True:
        pass
    hb.stop_pulse()
