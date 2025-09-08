import math

class Node:
    def __init__(self, id_number):
        # Number [0,3] which helps us identify which node we are talking about
        self.id = id_number
        self.layer = 0
        self.input_value = 0 # Sum of the weighted inputs
        self.output_value = 0
        self.connections = []  # List of outgoing connections that emerge from this node


    def activate(self):
        # Using sigmoid activation function
        def sigmoid(x):
            return 1 / (1 + math.exp(-x))
        
        # If the layer which the node is on is on the output layer
        if self.layer == 1:
            # Output value set to the result of the activation function if we pass the weighted inputs in the activation function
            self.output_value = sigmoid(self.input_value)
        
        for connection in self.connections:
            connection.to_node.input_value += self.output_value * connection.weight

    def clone(self):
        clone = Node(self.id)
        clone.id = self.id
        clone.layer = self.layer

        return clone
