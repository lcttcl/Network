# -*- encoding: utf-8 -*-
"""
---------------------------------------
@File        :   queue_.py
@Modify Time :   2020/2/23 11:58           
@Author      :   urchin_lct
@Contact     :   lichangtai17@gmail.com
@Version     :   0.0
---------------------------------------
"""
import threading
import time


class ThreadSafeQueueException(Exception):
    pass


class ThreadSafeQueue(object):
    """线程安全的队列"""

    def __init__(self, max_size=0):
        self.queue = []  # 队列（列表）
        self.max_size = max_size
        self.lock = threading.Lock()  # 锁
        self.condition = threading.Condition()  # 条件变量

    def size(self):
        self.lock.acquire()
        size = len(self.queue)
        self.lock.release()
        return size

    def put(self, item):
        """添加至队列"""
        if self.max_size != 0 and self.size() > self.max_size:  # ?
            return ThreadSafeQueueException()
        self.lock.acquire()
        self.queue.append(item)
        self.lock.release()
        self.condition.acquire()
        self.condition.notify()
        self.condition.release()

    def put_list(self, item_list):
        """批量添加至队列"""
        if not isinstance(item_list, list):
            item_list = list(item_list)
        for item in item_list:
            self.put(item)

    def pop(self, block=False, timeout=0):
        """从队列取出"""
        if self.size() == 0:
            if block:
                """需要阻塞等待"""
                self.condition.acquire()
                self.condition.wait(timeout=timeout)
                self.condition.release()
            else:
                return None

        self.lock.acquire()
        item = None
        if len(self.queue) > 0:
            item = self.queue.pop()
        self.lock.release()
        return item

    def get(self, index):
        """按序号取出"""
        self.lock.acquire()
        item = self.queue[index]
        self.lock.release()
        return item


if __name__ == '__main__':
    queue = ThreadSafeQueue(max_size=100)


    def produce():
        for i in range(20):
            queue.put(i)
            print('Produce: %d', i)
            time.sleep(3)


    def consume():
        while True:
            item = queue.pop()
            print('Consume: %d', item)
            time.sleep(1)


    thread1 = threading.Thread(target=produce)
    thread2 = threading.Thread(target=consume)
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
