# graph_r_uniformity
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## Description

The provided Python code consists of two main classes, Node and Graph, along with several utility functions for working with graphs and quantum states. The classes and functions in the code facilitate the creation, manipulation, and visualization of graph structures that represent quantum states.

Class Node:
The Node class represents a node in the graph. Each node is associated with a node_type attribute, indicating whether it represents a qubit (0), a traced node (1), or an open wire (2). The class contains methods to connect and disconnect nodes, change the node type, and display information about the node and its neighbors.

Class Graph:
The Graph class represents a graph composed of interconnected nodes. It stores a list of nodes, a list of rules (to be applied during simplification steps), and additional information about starred nodes and whether the graph has changed during the last simplification step. The class includes methods to add wires, simplify the graph through a series of rule applications, set rules, print the nodes, and plot the graph using the NetworkX library.

Utility Functions:

generate_graph: Creates a graph based on an adjacency matrix.
generate_given_state: Colors the graph based on a given array of qubits (non-starred nodes).
generate_random_state: Randomly colors the graph with a specified number of non-starred nodes (qubits).
spread: A rule applied during simplification, where a starred node has only one connection to a non-starred node.
disconnect: A rule applied during simplification, where two starred nodes have a direct connection between them.
adjacency_matrix_binomial: Generates a random adjacency matrix using a binomial distribution.
adjacency_matrix_regular: Generates an adjacency matrix for a regular graph with a specified degree.
Overall, this code provides a framework for working with quantum graph states and simplifying them through the application of specific rules. By leveraging this code, researchers and developers can explore quantum graph structures and their properties in the context of quantum information theory and quantum cryptography.

## Table of Contents

- [Project Name](#project-name)
  - [Description](#description)
  - [Table of Contents](#table-of-contents)
  - [Examples](#examples)
 
  ## Examples
  You can see examples in example1 and example2 

