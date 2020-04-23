# -*- encoding: utf-8 -*-
"""
---------------------------------------
@File        :   task.py   
@Modify Time :   2020/2/23 20:13           
@Author      :   urchin_lct
@Contact     :   lichangtai17@gmail.com
@Version     :   0.0
---------------------------------------
"""
import uuid
import threading

class Task:
    def __init__(self, func, *args, **kwargs):
        self.callable = func  # 任务具体逻辑
        self.args = args  # 任务参数
        self.kwargs = kwargs  # 任务参数
        self.id = uuid.uuid4()

    def __str__(self):
        return 'Task id ' + str(id)


class AsyncTask(Task):
    def __init__(self, func, *args, **kwargs):
        self.result = None
        self.condition = threading.Condition()
        super().__init__(func, *args, **kwargs)

    def set_result(self, result):
        self.condition.acquire()
        self.result = result
        self.condition.notify()
        self.condition.release()

    def get_result(self):
        self.condition.acquire()
        if not self.result:
            self.condition.wait()
        result = self.result
        self.condition.release()
        return result


def my_function():
    print('hello')


if __name__ == '__main__':
    task = Task(func=my_function)
