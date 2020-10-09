#!/usr/bin/python
# -*- coding: utf-8 -*-
import random

colors = [
    '\033[95m', # header
    '\033[94m', # okblue
    '\033[92m', # okgreen
    '\033[93m', # warning
    '\033[91m', # fail
]

class styles:
    endc = '\033[0m'
    bold = '\033[1m'
    underline = '\033[4m'


class Task:
    id = 'task'
    length = 0
    def __init__(self, id, length):
        self.id = id
        self.length = length

    def __repr__(self):
        return f'{self.id} <{self.length}>'

    def __str__(self):
        return self.__repr__()

class Processor:
    id = 'cpu0'
    def __init__(self, name='cpu0'):
        self.id = name
        self.tasks = []
        self.queue_size = 0

    def add_task(self, task):
        self.tasks.append(task)
        self.queue_size += task.length

    def __str__(self):
        return f'{self.id} | {self.tasks}'

    def __repr__(self):
        return self.__str__()

    def print_tasks(self):
        random.shuffle(colors)
        print(f'{self.id} | ', end='')
        for index, task in enumerate(self.tasks):
            print(f'{colors[index % len(colors)]}t{task.id} <{task.length}>{styles.endc} | ', end='')
        print(f'\n{self.id} | ', end='')
        for index, task in enumerate(self.tasks):
            print(f'{colors[index % len(colors)]}' + ('#' * task.length) + f'{styles.endc}', end='')
        print('\n')



number_of_processors = int(input("Liczba procesorów: "))
processors = []
for i in range(number_of_processors):
    processors.append(Processor(f'cpu{i}'))

number_of_tasks = int(input("Liczba zadań: "))
tasks = []
for i in range(number_of_tasks):
    length = int(input(f'Długość zadania {i}: '))
    tasks.append(Task(i, length))

tasks = sorted(tasks,key=lambda t: t.length)

while len(tasks):
    min_cpu = processors[0]
    min_queue_size = processors[0].queue_size
    for cpu in processors:
        if cpu.queue_size < min_queue_size:
            min_queue_size = cpu.queue_size
            min_cpu = cpu
    min_cpu.add_task(tasks.pop())
for cpu in processors:
    cpu.print_tasks()
