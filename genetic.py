import random
import yaml
import copy
import time
config = yaml.load(open('config.yml'), Loader=yaml.FullLoader)

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

    def __init__(self, processors = 0, tasks = [], assignments = []):
        self.tasks = []
        self.processors = processors

        for taskLength in tasks:
            self.tasks.append(Task(taskLength))
        if len(assignments):
            for i in range(len(assignments)):
                self.tasks[i].processorID = assignments[i]
        else:
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
        for i in range(self.config['population_size']):
            self.population.append(Individual(processors, tasks))
        # self.population[0].greedy()

    def crossover(self, _a, _b):
        cutoff_end = int(len(_a.tasks) * random.random())
        cutoff_start = int((cutoff_end-1) * random.random())
        c = Individual(_a.processors, self.tasks, _a.getAssignments())
        for i in range(cutoff_start, cutoff_end + 1):
            c.tasks[i].processorID = _b.tasks[i].processorID
        return c

    def run(self):
        size = self.config['population_size']
        lastFitness = 0
        lastIndex = 0
        pop_to_mutate = int(self.config['population_size']/10)
        half_pop = int(self.config['population_size']/2)
        start_mutate = half_pop-int(pop_to_mutate/2)
        end_mutate = start_mutate + pop_to_mutate
        for generation in range(self.config['iterations']):
            for i in range(start_mutate, end_mutate+1):
                if random.random() <= self.config['mutation_chance']:
                    self.population[i].mutate(3)
            for i in range(self.config['population_size']):
                for j in range(self.config['population_size']):
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
            self.population.sort(key=lambda individual: individual.fitness())
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
                        self.population[-i].random()
        print(f'Generacja {generation}, fitness {self.population[0].fitness()}')

population = Population(config, 25, [198, 157, 462, 779, 6, 98, 316, 450, 901, 372, 941, 94, 366, 781, 23, 16, 200, 686, 45, 311, 744, 784, 842, 168, 467, 214, 547, 74, 14, 499, 283, 981, 822, 621, 140, 895, 364, 185, 128, 794, 18, 646, 260, 419, 751, 532, 743, 923, 490, 478, 527, 543, 60, 915, 359, 90, 28, 44, 907, 18, 484, 718, 17, 820, 592, 11, 431, 657, 428, 373, 3, 58, 618, 7, 60, 980, 508, 813, 15, 568, 832, 625, 300, 2, 29, 6, 11, 8, 198, 701, 150, 500, 480, 478, 878, 380, 193, 367, 971, 276, 846, 590, 923, 961, 777, 241, 16, 91, 6, 419, 403, 456, 982, 41, 557])
population.run()
