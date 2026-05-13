# ==========================================
# AI LAB PROJECT
# Members: Muhammad Haris Hamid (24F-0699)
#          Muhammad Ahmad (24F-0513)
#          Waleed Bin Nasir (24F-0516)
# ==========================================

# PHASE 1: Python and Data Foundation
# Step 1: Installing and importing libraries
# (Ensure you run: pip install pandas numpy matplotlib scikit-learn)

import pandas as pd
from collections import deque

# Step 2: Loading Dataset
df = pd.read_csv("mental-heath-in-tech-2016_20161114.csv")

# Step 3: Inspecting Dataset
print("First 5 rows:")
print(df.head())

print("\nDataset Shape:")
print(df.shape)

print("\nMissing Values:")
print(df.isnull().sum())

# Target column inspection
target_col = "Have you been diagnosed with a mental health condition by a medical professional?"
print(f"\nOur Target column is: {target_col}")
print("Unique values in our target column are as follows :")
print(df[target_col].unique())

# Step 4: Apply Python Fundamentals
target_col_class_count = {}
for value in df[target_col]:
    value = str(value)
    if value in target_col_class_count:
        target_col_class_count[value] += 1
    else:
        target_col_class_count[value] = 1

print("\nThe class Distribution in target col is as follows:")
print(target_col_class_count)        

columns_list = list(df.columns)
sample_data = df[:50]

def describe_dataset():
    print("\nDataset Description\n")
    print(f"Dataset Shape: {df.shape}\n")
    print(f"Dataset Column Names: {columns_list}\n")
    print(f"Dataset Class Distribution: {target_col_class_count}\n")

describe_dataset()

# Step 5: Object-Oriented Representation
class DataRecord:
    def __init__(self, record_id, features, label):
        self.record_id = record_id
        self.features = features
        self.label = label
        
    def Display(self):
        print(f"Record ID: {self.record_id}\n")
        print(f"Features: {self.features}\n")
        print(f"Label: {self.label}\n")
        print("-" * 15)

object_list = []
for row_index in range(5):
    row = df.iloc[row_index]
    obj_id = row_index
    obj_label = row[target_col]
    obj_features = row.drop(target_col).to_dict()
    
    new_record_object = DataRecord(record_id=obj_id, label=obj_label, features=obj_features)
    object_list.append(new_record_object)

print("\nSample Data Records:")
for obj in object_list:
    obj.Display()

# Step 6: Build a Graph from Your Data
col1 = "Have you ever sought treatment for a mental health issue from a mental health professional?"
col2 = "If you have a mental health issue, do you feel that it interferes with your work when NOT being treated effectively?"

graph = {}
for index in range(len(df)):
    row = df.iloc[index]
    raw_val = str(row[col1]).strip()
    
    if (raw_val == '1') or (raw_val == '1.0'):
        val = 'yes'
    else:
        val = 'no'
        
    node_A = val.strip().title() + "(Sought Treatment)"
    node_B = str(row[col2]).strip().title() + "(Interference)"
    
    if (node_A not in graph):
        graph[node_A] = []
    if (node_B not in graph):
        graph[node_B] = []
        
    if (node_B not in graph[node_A]):
         graph[node_A].append(node_B)
    if (node_A not in graph[node_B]):
        graph[node_B].append(node_A)

print("\nDataset Graph\n")
for node, connected_nodes in graph.items():
    print(f"{node} is connected to -->{connected_nodes}")

print(f"the total number of nodes in the graph are {len(graph)}\n")
print(f"the total number of edges in the graph are {sum(len(connections) for connections in graph.values())//2}\n")


# ==========================================
# PHASE 2: Intelligent Agent and Search Algorithms
# ==========================================

# Step 1: Define the Agent and State Space
class Agent:
    def __init__(self, graph, goal):
        self.graph = graph
        self.goal = goal
        
    def perceive(self, state):
        return self.graph[state]
        
    def action(self, act):
        return act
        
    def goal_test(self, state):
        if (state == self.goal):
            return True
            
    def get_cost(self, state1, state2):
        return 1

test_agent = Agent(graph, "Often(Interference)")

# Step 2: Uninformed Search (BFS)
def BFS(agent, start_node):
    visited = [] 
    queue = deque([start_node]) 
    
    came_from = {}
    came_from[start_node] = None 
    
    nodes_explored = 0
    
    while len(queue) > 0: 
        returned_node = queue.popleft()
        nodes_explored += 1 
        
        if returned_node in visited:
            continue
        else:
            visited.append(returned_node)
            
        if agent.goal_test(returned_node): 
            print("\nGoal Found!")
            print(f"Total Nodes Explored: {nodes_explored}")
            
            path = []
            step = returned_node
            while step is not None:
                path.append(step)
                step = came_from[step] 
                
            path.reverse() 
            
            print(f"Path Length: {len(path) - 1}") 
            print("Direct Path to Goal:", path)
            return path
            
        else:
            for neighbor in agent.perceive(returned_node): 
                if neighbor not in visited and neighbor not in queue:
                    came_from[neighbor] = returned_node
                queue.append(neighbor)
                
    print("goal not found")

# Test the BFS Agent
BFS(test_agent, "Yes(Sought Treatment)")
