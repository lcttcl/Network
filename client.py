# -*- encoding: utf-8 -*-
"""
---------------------------------------
@File        :   client.py   
@Modify Time :   2020/2/22 21:27           
@Author      :   urchin_lct
@Contact     :   lichangtai17@gmail.com
@Version     :   0.0
---------------------------------------
"""
import socket


def client(index):
    """create"""
    s = socket.socket()

    """connect"""
    s.connect(('115.34.98.164', 8888))

    print('Recv msg: %s, Client: %d' % (s.recv(1024), index))
    s.close()


if __name__ == '__main__':
    for i in range(10):
        client(i)
