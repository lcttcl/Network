# -*- encoding: utf-8 -*-
"""
---------------------------------------
@File        :   server.py   
@Modify Time :   2020/2/23 11:22           
@Author      :   urchin_lct
@Contact     :   lichangtai17@gmail.com
@Version     :   0.0
---------------------------------------
"""
import json
import socket

from computer_network.processor.net.parser import IPParser
from computer_network.processor.trans.parser import UDPParser, TCPParser
from operate_system.pool import ThreadPool as tp
from operate_system.task import AsyncTask


class ProcessTask(AsyncTask):

    def __init__(self, packet, *args, **kwargs):
        self.packet = packet
        super(ProcessTask, self).__init__(func=self.process, *args, **kwargs)

    def process(self):
        headers = {
            'network_header': None,
            'transport_header': None
        }

        ip_header = IPParser.parse(self.packet)
        headers['network_header'] = ip_header
        if ip_header['protocol'] == 17:
            udp_header = UDPParser.parse(self.packet)
            headers['transport_header'] = udp_header
        elif ip_header['protocol'] == 6:
            tcp_header = TCPParser.parse(self.packet)
            headers['transport_header'] = tcp_header
        return headers


class Server():
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
        self.ip = '192.168.0.106'
        # self.ip = '118.74.236.251'
        self.port = 8888
        self.sock.bind((self.ip, self.port))
        self.sock.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
        self.pool = tp(10)
        self.pool.start()

    def loop_serve(self):
        while True:
            # 接收
            packet, addr = self.sock.recvfrom(65535)
            # 生成任务并提交至线程池
            task = ProcessTask(packet)
            self.pool.put(task)
            # 获取结果并打印
            result = task.get_result()
            result = json.dumps(
                result,
                indent=4
            )
            print(result)


if __name__ == '__main__':
    server = Server()
    server.loop_serve()