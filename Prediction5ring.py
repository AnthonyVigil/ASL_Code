from math import exp
from random import seed
from random import random
import sys
import random
import ast
import serial
import datetime
import time

def load_file(filename):
	with open(filename, 'r') as f:
	    dataset = [[int(num) for num in line.split()] for line in f]
	return dataset

def normalize_data(row):
	for i in range(len(row)):
		row[i] = row[i]/float(1023)
	return row

def normalize_dataset_with_class(dataset):
    for row in dataset:
        for i in range(len(row)-1):
            row[i] = row[i]/float(1023)
        row[-1] = int(row[-1])
    return dataset

def normalize_dataset_no_class(dataset):
    for row in dataset:
        for i in range(len(row)):
            row[i] = row[i]/float(1023)
    return dataset

def alpha(weights, inputs):
	alpha = weights[-1]
	for i in range(len(weights)-1):
		alpha += weights[i] * inputs[i]
	return alpha

def activation_function(activation):
	return round(1.0 / (1.0 + exp(-activation)),4)

def forward_propagate(network,row):
	inputs = row
	for layer in network:
		new_inputs = []
		for neuron in layer:
			alpha_value = alpha(neuron['weights'],inputs)
			neuron['output'] = activation_function(alpha_value)
			new_inputs.append(neuron['output'])
		inputs = new_inputs
	return inputs
	
# def forward_propagate(network, row):
    # inputs = row
    # for layer in network:
		# new_inputs = []
		# for neuron in layer:
			# alpha_value = alpha(neuron['weights'], inputs)
			# neuron['output'] = activation_function(alpha_value)
			# new_inputs.append(neuron['output'])
		# inputs = new_inputs
    # return inputs

def predict_sign(network, test_data):
    outputs = forward_propagate(network,test_data)
    max_output = max(outputs)
    predict = outputs.index(max_output)
    return predict


def fun(network,gesture):
    serial_port='COM7'
    acc = []
    ser = serial.Serial(serial_port,115200)
    ser.reset_input_buffer()
    j = 0
    while True:
        try:
            for i in range(0,5):
                row = ser.readline().decode('utf-8')
                temp = [float(num) for num in row.split()]
                dataset = normalize_data(temp)
                dataset.append(j)
                sign = predict_sign(network,dataset)
                print(gesture[sign])
                sys.stdout.flush()
        except KeyboardInterrupt:
            file.close()
            break
    ser.close()
    return acc


print('Start Testing')
file = open("network.txt","r")
contents = file.read()
network = ast.literal_eval(contents)
file.close()
accuracy = []
gesture = ["A","D"]
if len(sys.argv) >= 2:
    data = load_file(sys.argv[1])
    if (len(sys.argv) == 3):
        if (sys.argv[2] == "trueclass"):
            response = "y"
        elif (sys.argv[2] == "notrueclass"):
            response = "n"
    else:
        response = raw_input('Does the input file include true class? ')
    if response == "n":
        data = normalize_dataset_no_class(data)
        for row in data:
            sign = predict_sign(network, row)
            print(gesture[sign])
    elif response == "y":
        data = normalize_dataset_with_class(data)
        print("\n\nActual           |   Predicted")
        print("----------------------------------")
        for row in data:
            sign = predict_sign(network, row)
            print(gesture[row[-1]]+"    |   "+gesture[sign])
            if row[-1] == sign:
                accuracy.append(1)
            else:
                accuracy.append(0)
        prediction_acc = round((sum(accuracy)/float(len(accuracy)))*100,2)
        print("\nPrediction accuracy is "+str(prediction_acc)+"%")
else:
    accuracy = fun(network,gesture)
print('\nEnd Testing')
