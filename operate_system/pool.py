# -*- encoding: utf-8 -*-
"""
---------------------------------------
@File        :   pool.py   
@Modify Time :   2020/2/24 18:38           
@Author      :   urchin_lct
@Contact     :   lichangtai17@gmail.com
@Version     :   0.0
---------------------------------------
"""
import threading
import psutil
from operate_system.task import Task, AsyncTask
from operate_system.queue_ import ThreadSafeQueue


class ProcessThread(threading.Thread):
    """任务处理线程"""

    def __init__(self, task_queue, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        self.task_queue = task_queue
        self.args = args
        self.kwargs = kwargs
        self.dismiss_flag = threading.Event()  # 线程停止的标记

    def run(self):
        """执行线程"""
        while True:
            if self.dismiss_flag.is_set():
                break
            task = self.task_queue.pop()
            if not isinstance(task, Task):
                continue
            """执行任务具体逻辑"""
            result = task.callable(*task.args, **task.kwargs)
            if isinstance(task, AsyncTask):
                task.set_result(result)

    def dismiss(self):
        self.dismiss_flag.set()

    def stop(self):
        self.dismiss()


class ThreadPool:
    def __init__(self, size=0):
        if not size:
            size = psutil.cpu_count() * 2
        self.pool = ThreadSafeQueue(size)  # 线程池
        self.task_queue = ThreadSafeQueue()  # 任务队列

        for i in range(size):
            self.pool.put(ProcessThread(self.task_queue))

    def start(self):
        """启动线程池"""
        for i in range(self.pool.size()):
            thread = self.pool.get(i)
            thread.start()

    def join(self):
        """终止线程池"""
        for i in range(self.pool.size()):
            thread = self.pool.get(i)
            thread.stop()
        while self.pool.size():
            thread = self.pool.pop()
            thread.join()

    def put(self, item):
        """添加任务"""
        if not isinstance(item, Task):
            raise TaskTypeErrorException()

        self.task_queue.put(item)

    def batch_put(self, item_list):
        """批量添加任务"""
        if not isinstance(item_list, list):
            item_list = list(item_list)
        for item in item_list:
            self.task_queue.put(item)

    def size(self):
        return self.pool.size()


class TaskTypeErrorException(Exception):
    pass
