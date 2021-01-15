import random
import yaml
import copy
import time
import sys
import operator
config = yaml.load(open('config.yml'), Loader=yaml.FullLoader)

fitness_operator = operator.attrgetter("fitness_factor")

class Task:
    length = 0
    processorID = 0
    def __init__(self, taskLength, processorID = 0):
        self.length = taskLength
        self.processorID = processorID

    def __str__(self):
        # return f'Task length {self.length} at cpu {self.processorID}'
        return f'{self.processorID}/{self.length}'

    def __repr__(self):
        return self.__str__()

class Individual:

    def __init__(self, processors = 0, tasks = [], initialize=True):
        self.tasks = []
        self.processors = processors
        self.fitness_factor = 0

        self.tasks = [Task(taskLength) for taskLength in tasks]
        if initialize:
            self.random()

    def getAssignments(self):
        return list(map(lambda t: t.processorID, self.tasks))

    def random(self):
        for task in self.tasks:
            task.processorID = random.randint(0, self.processors-1)

    def getProcessors(self):
        processors = [0] * self.processors
        for task in self.tasks:
            processors[task.processorID] += task.length
        return processors


    def greedy(self):
        processors = [0] * self.processors
        for task in sorted(self.tasks, key=lambda t: t.length, reverse=True):
            minProcessorIndex = 0
            minProcessorTasksLength = processors[minProcessorIndex]
            for processorIndex, processorTasksLength in enumerate(processors):
                if processorTasksLength < minProcessorTasksLength:
                    minProcessorIndex = processorIndex
                    processorTasksLength = minProcessorTasksLength
            task.processorID = minProcessorIndex
            processors[minProcessorIndex] += task.length

    def __str__(self):
        processors = self.getProcessors()
        output = ''
        for index, length in enumerate(processors):
            output += f'cpu {index}: {length}\n'
        return output

    def __repr__(self):
        return self.__str__()

    def fitness(self):
        return max(self.getProcessors())

    def mutate(self, rounds = 1): # losowe przemieszczenie zadania
        for i in range(rounds):
            task = self.tasks[random.randint(0, len(self.tasks) - 1)]
            newProcessorID = task.processorID
            while newProcessorID == task.processorID:
                newProcessorID = random.randint(0, self.processors - 1)
            task.processorID = newProcessorID

class Population:
    population = []
    config = {}
    def __init__(self, config, processors = 0, tasks = []):
        self.config = config
        self.tasks = tasks
        self.number_of_tasks = len(tasks)
        for i in range(self.config['population_size']):
            self.population.append(Individual(processors, tasks))
        # self.population[0].greedy()

    def update_fitness(self):
        for individual in self.population:
            individual.fitness_factor = individual.fitness()

    def crossover(self, _a, _b):

        cutoff_end = int(self.number_of_tasks * random.random())
        cutoff_start = int((cutoff_end-1) * random.random())
        c = Individual(_a.processors, self.tasks, False)
        for i in range(0, cutoff_start):
            c.tasks[i].processorID = _a.tasks[i].processorID
        for i in range(cutoff_start, cutoff_end + 1):
            c.tasks[i].processorID = _b.tasks[i].processorID
        for i in range(cutoff_end + 1, self.number_of_tasks):
            c.tasks[i].processorID = _a.tasks[i].processorID
        return c

    def run(self):
        size = self.config['population_size']
        lastFitness = 0
        lastIndex = 0
        pop_to_mutate = int(self.config['population_size']/(1/self.config['part_of_pop_to_mutate']))
        half_pop = int(self.config['population_size']/2)
        start_mutate = half_pop-int(pop_to_mutate/2)
        end_mutate = start_mutate + pop_to_mutate
        for generation in range(self.config['iterations']):
            for i in range(start_mutate, end_mutate+1):
                if random.random() <= self.config['mutation_chance']:
                    self.population[i].mutate(self.config['mutation_rounds'])
            for i in range(self.config['population_size']):
                for j in range(0, i):
                    self.population.append(self.crossover(
                        self.population[i],
                        self.population[j]
                    ))
            # while len(self.population) < 2 * size:
            #     child = self.crossover(
            #         random.choice(self.population),
            #         random.choice(self.population),
            #     )
            #     self.population.append(child)
            self.update_fitness()
            self.population.sort(key=fitness_operator)
            # print(generation)
            # print(list(map(lambda i: i.fitness(), self.population)))
            while len(self.population) > size:
                self.population.pop()
            bestFitness = self.population[0].fitness()

            if bestFitness != lastFitness:
                lastFitness = bestFitness
                lastIndex = generation
                print(f'Generacja {generation}, fitness {self.population[0].fitness()}')
            else:
                if generation - lastIndex > 100:
                    lastIndex = generation
                    for i in range(int(len(self.population)/2)):
                        # self.population[-i].mutate(50)
                        self.population[-i].random()
        print(f'Generacja {generation}, fitness {self.population[0].fitness()}')

lines = []
with open(sys.argv[1], "r") as file:
    for line in file:
        lines.append(int(line))

cpus = lines[0]
tasks = sorted(lines[2:], reverse=True)

population = Population(config, cpus, tasks)
population.run()
