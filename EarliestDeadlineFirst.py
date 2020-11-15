#reference to Diego PERINI's Earlies deadline first scheduling implementation

import string
import random
import fractions


#A task instance
class TaskIns(object):

     #Constructor (should only be invoked with keyword parameters)
    def __init__(self, start, end, priority, name):
        self.start    = start
        self.end      = end
        self.usage    = 0
        self.priority = priority
        self.name     = name.replace("\n", "")
        self.id = int(random.random() * 10000)

    #Allow an instance to use the cpu (periodic)
    def use(self, usage):
        self.usage += usage
        if self.usage >= self.end - self.start:
            return True
        return False

    #Default representation
    def __repr__(self):
        return str(self.name) + "#" + str(self.id) + " - start: " + str(self.start) + " priority: " + str(self.priority) + budget_text

    #Get name as Name#id
    def get_unique_name(self):
        return str(self.name) + "#" + str(self.id)

#Task types (templates for periodic tasks)
class TaskType(object):

    #Constructor
    def __init__(self, period, release, execution, deadline, name):
        self.period    = period
        self.release   = release
        self.execution = execution
        self.deadline  = deadline
        self.name      = name

# LCM of the tasks
def _lcm(a,b): return abs(a * b) / fractions.gcd(a,b) if a and b else 0
def lcm(a):
    return reduce(_lcm, a)


#Priority comparison
def priority_cmp(one, other):
    if one.priority < other.priority:
        return -1
    elif one.priority > other.priority:
        return 1
    return 0

#Deadline monotonic comparison
def tasktype_cmp(self, other):
    if self.deadline < other.deadline:
        return -1
    if self.deadline > other.deadline:
        return 1
    return 0

if __name__ == '__main__':
    html_color = { 'Task1':'red', 'Task2':'blue', 'Task3':'green', 'Task4':'aqua', 'Task5':'coral', 'Empty':'grey', 'Finish':'black'}
    taskfile = open('tasks.txt')
    lines = taskfile.readlines()
    task_types = []
    tasks = []
    hyperperiod = []

    #Allocate task types
    for line in lines:
        line = line.split(' ')
        for i in range (0,4):
            line[i] = int(line[i])
        if len(line) == 5:
            name = line[4]
        elif len(line) == 4:
            name = 'Task'
        else:
            raise Exception('Invalid tasks.txt file structure')
        if int(line[0])>0:
            task_types.append(TaskType(period=line[0], release=line[1], execution=line[2], deadline=line[3], name=name))

    #Calculate hyperperiod
    for task_type in task_types:
        hyperperiod.append(task_type.period)
    hyperperiod = lcm(hyperperiod)

    #Sort types rate monotonic
    task_types = sorted(task_types, tasktype_cmp)


    #Create task instances
    for i in xrange(0, hyperperiod):
        for task_type in task_types:
            if  (i - task_type.release) % task_type.period == 0 and i >= task_type.release:
                start = i
                end = start + task_type.execution
                priority = start + task_type.deadline
                tasks.append(TaskIns(start=start, end=end, priority=priority, name=task_type.name))


    #Simulate clock
    clock_step = 1
    for i in xrange(0, hyperperiod, clock_step):
        #Fetch possible tasks that can use cpu and sort by priority
        possible = []
        for t in tasks:
            if t.start <= i:
                possible.append(t)
        possible = sorted(possible, priority_cmp)

        #Select task with highest priority
        if len(possible) > 0:
            on_cpu = possible[0]
            print on_cpu.get_unique_name() , " uses the processor. " ,
            if on_cpu.use(clock_step):
                tasks.remove(on_cpu)
                print "Finish!" ,
        else:
            print 'No task uses the processor. '
        print "\n"

    #Print remaining periodic tasks
    for p in tasks:
        print p.get_unique_name() + " is dropped due to overload at time: " + str(i)