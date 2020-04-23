# -*- encoding: utf-8 -*-
"""
---------------------------------------
@File        :   t0.py
@Modify Time :   2020/2/25 18:21           
@Author      :   urchin_lct
@Contact     :   lichangtai17@gmail.com
@Version     :   0.0
---------------------------------------
"""
import time
from operate_system import pool
from operate_system import task


class SimpleTask(task.Task):
    def __init__(self, callable):
        super(SimpleTask, self).__init__(callable)


def process():
    time.sleep(1)
    print('simple task test 1')
    time.sleep(1)
    print('simple task test 2')


def test():
    test_pool = pool.ThreadPool()
    test_pool.start()

    for i in range(10):
        simple_task = SimpleTask(process)
        test_pool.put(simple_task)


def test_async_task():
    def async_process():
        num = 0
        for i in range(101):
            num += i
        return num

    test_pool = pool.ThreadPool()
    test_pool.start()
    for i in range(10):
        async_task = task.AsyncTask(async_process)
        test_pool.put(async_task)
        result = async_task.get_result()
        print('result: %d' % result)


if __name__ == '__main__':
    test_async_task()
