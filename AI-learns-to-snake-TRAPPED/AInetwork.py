import numpy as np
import random, math

def sigmoid(num):
    return 1/(1+(math.e**(-num)))

sigmoid_array = np.vectorize(sigmoid)

def randomise(num, chance, multiplier):
    if random.random() < chance:
        return num + random.uniform(-multiplier, multiplier)
    else:
        return num

randomise_array = np.vectorize(randomise)

def get_fitness(ai):
    return -ai.fitness

def average(arr):
    return sum(arr) / len(arr)

def max_in_list(input_list):
    max = input_list[0]
    index = 0
    for i in range(1,len(input_list)):
        if input_list[i] > max:
            max = input_list[i]
            index = i
    return index

def max_value_in_list(input_list):
    max = input_list[0]
    index = 0
    for i in range(1,len(input_list)):
        if input_list[i] > max:
            max = input_list[i]
            index = i
    return max

def max_value(a, b):
    if a > b:
        return a
    else:
        return b

def new_network(input_num, hidden_nums, out_num, init_range):
    network = []
    if hidden_nums == []:
        network.append(np.array([[random.uniform(*init_range) for j in range(input_num)] for i in range(out_num)]))
        return {"network" : network, "coefficients" : [random.uniform(*init_range) for i in range(2 + len(hidden_nums))]}
    network.append(np.array([[random.uniform(*init_range) for j in range(input_num)] for i in range(hidden_nums[0])]))
    for num in range(len(hidden_nums[0:-1])):
        network.append(np.array([[random.uniform(*init_range) for j in range(hidden_nums[num])] for i in range(hidden_nums[num + 1])]))
    network.append(np.array([[random.uniform(*init_range) for j in range(hidden_nums[-1])] for i in range(out_num)]))
    return {"network" : network, "coefficients" : [random.uniform(*init_range) for i in range(2 + len(hidden_nums))]}

def simular_network(old_brain, chance, multiplier):
    copy_of_brain = {
        "network" : [randomise_array(np.copy(array), chance, multiplier) for array in old_brain["network"]],
        "coefficients" : randomise_array(np.copy(old_brain["coefficients"]), chance, multiplier)
    }
    return copy_of_brain
    
def generate_initial_ais(num_of_ais, input_num, hidden_nums, out_num, init_range):
    array_of_ais = []
    for i in range(num_of_ais):
        array_of_ais.append(AI(new_network(input_num, hidden_nums, out_num, init_range)))
    return array_of_ais

def generate_next_ais(previous_array_of_ais, chance, multiplier, elitism, randoms, input_num, hidden_nums, out_num, init_range):
    array_of_ais =[]
    previous_array_of_ais = sorted(previous_array_of_ais, key=get_fitness)
    elite_ais = [AI(simular_network(ai.brain, 0, 0)) for ai in previous_array_of_ais[0:elitism:1]]
    for i in range(len(previous_array_of_ais) - randoms - elitism):
        array_of_ais.append(AI(simular_network(random.choice(elite_ais).brain, chance, multiplier)))
    for i in range(randoms):
        array_of_ais.append(AI(new_network(input_num, hidden_nums, out_num, init_range)))
    return [*array_of_ais, *elite_ais]

class AI():
    def __init__(self, brain):
        self.brain = brain
        self.fitness = 0
    
    def gen_outs(self, inputs):
        arr = np.array(inputs)
        for index, layer in enumerate(self.brain["network"]):
            arr = layer.dot(arr) + self.brain["coefficients"][index]
            arr = sigmoid_array(arr)
        return arr
    
    def gen_layer_outs(self, inputs):
        arr = np.array(inputs)
        layer_outs = [arr]
        for index, layer in enumerate(self.brain["network"]):
            arr = layer.dot(arr) + self.brain["coefficients"][index]
            arr = sigmoid_array(arr)
            layer_outs.append(arr)
        return layer_outs