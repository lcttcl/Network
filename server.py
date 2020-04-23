# -*- encoding: utf-8 -*-
"""
---------------------------------------
@File        :   server.py   
@Modify Time :   2020/2/22 18:41           
@Author      :   urchin_lct
@Contact     :   lichangtai17@gmail.com
@Version     :   0.0
---------------------------------------
"""
import socket


def server():
    """create"""
    s = socket.socket()
    host = '127.0.0.1'
    port = 6666

    """bind"""
    s.bind((host, port))

    """listen"""
    s.listen(5)

    while True:
        client, addr = s.accept()
        print('Addr:', addr)
        client.send(b'Welcome')
        client.close()


if __name__ == '__main__':
    server()
