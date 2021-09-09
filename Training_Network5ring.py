#Prissha Krishna Moorthy, 1001354261
from math import exp
from random import seed
from random import random
import sys
import random


#Load file
def load_file(filename):
	with open(filename, 'r') as f:
	    dataset = [[int(num) for num in line.split()] for line in f]
	dataset = normalize_data(dataset)
	return dataset

#Normalize Data
def normalize_data(dataset):
	#max_value = max(max(dataset))
	for row in dataset:
		for i in range(len(row)-1):
			row[i] = row[i]/float(1023)
		row[-1] = int(row[-1])
	return dataset

# Initialize a network
def initialize_network(n_inputs, n_hidden, n_outputs, n_layer):
	network = list()
	for n in range(n_layer-2):
		hidden_layer = [{'weights':[random.uniform(-0.5,0.5) for i in range(n_inputs + 1)]} for i in range(n_hidden)]
		network.append(hidden_layer)
		n_inputs = len(hidden_layer)
	if n_layer == 2:
		n_hidden = n_inputs
	output_layer = [{'weights':[random.uniform(-0.5,0.5) for i in range(n_hidden + 1)]} for i in range(n_outputs)]
	network.append(output_layer)
	return network

# Calculate neuron activation for an input
def alpha(weights, inputs):
	alpha = weights[-1]
	for i in range(len(weights)-1):
		alpha += weights[i] * inputs[i]
	return alpha

# Transfer neuron activation
def activation_function(activation):
	return round(1.0 / (1.0 + exp(-activation)),4)

# Forward propagate input to a network output
def forward_propagate(network, row):
	inputs = row
	for layer in network:
		new_inputs = []
		for neuron in layer:
			alpha_value = alpha(neuron['weights'], inputs)
			neuron['output'] = activation_function(alpha_value)
			new_inputs.append(neuron['output'])
		inputs = new_inputs
	return inputs

# Calculate the derivative of an neuron output
def transfer_derivative(output):
	return output * (1.0 - output)

# Backpropagate error and store in neurons
def backward_propagate_error(network, expected):
	for i in reversed(range(len(network))):
		layer = network[i]
		errors = list()
		if i != len(network)-1:
			for j in range(len(layer)):
				error = 0.0
				for neuron in network[i + 1]:
					error += (neuron['weights'][j] * neuron['delta'])
				errors.append(error)
		else:
			for j in range(len(layer)):
				neuron = layer[j]
				errors.append(neuron['output'] - expected[j])
		for j in range(len(layer)):
			neuron = layer[j]
			neuron['delta'] = errors[j] * transfer_derivative(neuron['output'])

# Update network weights with error
def update_weights(network, row, l_rate):
	for i in range(len(network)):
		inputs = row[:-1]
		if i != 0:
			inputs = [neuron['output'] for neuron in network[i - 1]]
		for neuron in network[i]:
			for j in range(len(inputs)):
				neuron['weights'][j] -= l_rate * neuron['delta'] * inputs[j]
			neuron['weights'][-1] -= l_rate * neuron['delta']

# Train a network for a fixed number of epochs
def train_network(network, train, classes, n_epoch, n_outputs):
	for r in range(n_epoch):
		sum_error = 0
		l_rate = 0.98**((r+1)-1);
		for row in train:
			outputs = forward_propagate(network, row)
			expected = [0 for i in range(n_outputs)]
			ind = classes.index(row[-1])
			expected[ind] = 1
			sum_error += sum([(expected[i]-outputs[i])**2 for i in range(len(expected))])
			backward_propagate_error(network, expected)
			update_weights(network, row, l_rate)
		print('>epoch=%d, lrate=%.3f, error=%.3f' % (r+1, l_rate, sum_error))

def create_class(dataset):
	dataset = load_file(dataset)
	classes = []
	for x in dataset:
		if x[-1] not in classes:
			classes.append(x[-1])
	classes.sort()
	return classes

# Test training backprop algorithm
def fun(layers,units_per_layer,rounds,filename):
	dataset = load_file(filename) #'Training_Data2.txt'
	n_inputs = len(dataset[0]) - 1
	n_outputs = len(set([row[-1] for row in dataset])) #output labels (True Class)
	network = initialize_network(n_inputs, units_per_layer, n_outputs, layers)
	classes = create_class(filename)
	train_network(network, dataset, classes, rounds, n_outputs)
	return network


layers = int(sys.argv[1])
units_per_layer = int(sys.argv[2])
rounds = int(sys.argv[3])
filename = sys.argv[4]
network = fun(layers,units_per_layer,rounds,filename)
with open("network.txt","w") as files:
    files.write(str(network))
files.close()
