from __future__ import division
from __future__ import print_function
import resource

import sys
import math
import time
import queue as Q
import numpy as np


#### SKELETON CODE ####
## The Class that Represents the Puzzle
class PuzzleState(object):
    """
        The PuzzleState stores a board configuration and implements
        movement instructions to generate valid children.
    """
    def __init__(self, config, n, parent=None, action="Initial", cost=0):
        """
        :param config->List : Represents the n*n board, for e.g. [0,1,2,3,4,5,6,7,8] represents the goal state.
        :param n->int : Size of the board
        :param parent->PuzzleState
        :param action->string
        :param cost->int
        """
        if n*n != len(config) or n < 2:
            raise Exception("The length of config is not correct!")
        if set(config) != set(range(n*n)):
            raise Exception("Config contains invalid/duplicate entries : ", config)

        self.n        = n
        self.cost     = cost
        self.parent   = parent
        self.action   = action
        self.config   = config
        self.children = []

        self.depth = 0

        # Get the index and (row, col) of empty block
        self.blank_index = self.config.index(0)

    def display(self):
        """ Display this Puzzle state as a n*n board """
        for i in range(self.n):
            print(self.config[3*i : 3*(i+1)])
            # 0 1 2 (no last indexNum)
        print('\n')

    def move_up(self):
        """ 
        Moves the blank tile one row up.
        :return a PuzzleState with the new configuration
        """
        new_config = self.config.copy()
        x = self.blank_index        
        if x == 0 or x == 1 or x == 2:
            return None
        else:
            new_config[x] = new_config[x-3]
            new_config[x-3] = 0
            new_state = PuzzleState(new_config, int(math.sqrt(len(new_config))), parent=self, action='Up')    
        return new_state
      
    def move_down(self):
        """
        Moves the blank tile one row down.
        :return a PuzzleState with the new configuration
        """
        new_config = self.config.copy()
        x = self.blank_index 
        if x == 6 or x == 7 or x == 8:
            return None
        else:
            new_config[x] = new_config[x+3]
            new_config[x+3] = 0
            new_state = PuzzleState(new_config, int(math.sqrt(len(new_config))), parent=self, action='Down')    
        return new_state
            
    def move_left(self):
        """
        Moves the blank tile one column to the left.
        :return a PuzzleState with the new configuration
        """
        new_config = self.config.copy()
        x = self.blank_index 
        if x == 0 or x == 3 or x == 6:
            return None
        else:
            new_config[x] = new_config[x-1]
            new_config[x-1] = 0
            new_state = PuzzleState(new_config, int(math.sqrt(len(new_config))), parent=self, action='Left')    
        return new_state
        
    def move_right(self):
        """
        Moves the blank tile one column to the right.
        :return a PuzzleState with the new configuration
        """     
        new_config = self.config.copy()
        x = self.blank_index 
        if x == 2 or x == 5 or x == 8:
            return None
        else:
            new_config[x] = new_config[x+1]
            new_config[x+1] = 0
            new_state = PuzzleState(new_config, int(math.sqrt(len(new_config))), parent=self, action='Right')    
        return new_state
      
    def expand(self):
        """ Generate the child nodes of this node """
        
        # Node has already been expanded
        if len(self.children) != 0:
            return self.children
        
        # Add child nodes in order of UDLR
        children = [
            self.move_up(),
            self.move_down(),
            self.move_left(),
            self.move_right()]

        # Compose self.children of all non-None children states
        self.children = [state for state in children if state is not None]
        for child in self.children:
            child.depth = self.depth + 1
        return self.children

      
# Function that Writes to output.txt

### Students need to change the method to have the corresponding parameters
def writeOutput(output):
    ### Student Code Goes here
    with open('output.txt', 'w') as f:
        f.writelines(output)
    f.close()
    pass

def total_output(state, nodes, max_depth,runt, max_ram):
    path = get_path(state)
    cost = len(path)
    search_depth = len(path)
    a = 'path_to_goal: {q0}\n'.format(q0 = path)    
    b = 'cost_of_path: {q1}\n'.format(q1 =cost)
    c = 'nodes_expanded: {q2}\n'.format(q2 =nodes)
    d = 'search_depth: {q3}\n'.format(q3 =search_depth)
    e = 'max_search_depth: {q4}\n'.format(q4 = max_depth)
    f = 'running_time: {q5}\n'.format(q5 = runt)
    g = 'max_ram_usage: {q6}\n'.format(q6 = max_ram)
    output = [a,b,c,d,e,f,g]
   
    return output


def bfs_search(initial_state):
    """BFS search"""
    ### STUDENT CODE GOES HERE ###
    dfs_start_ram = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    start_time  = time.time()
    frontier = []
    frontier.append(initial_state)
    unvisit = set()
    unvisit.add(tuple(initial_state.config))
    explored = set()
    nodes = 0
    max_depth = 0

    while frontier:
        state = frontier.pop(0)
        explored.add(tuple(state.config))

        if state.config == [0,1,2,3,4,5,6,7,8]:
            if frontier:
                x = frontier.pop(-1)
            else:
                x = state
            max_depth = max(x.depth,state.depth)
            dfs_ram = (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss-dfs_start_ram)/(2**20)
            end_time = time.time()
            output = total_output(state,nodes,max_depth,end_time-start_time,dfs_ram) 
            writeOutput(output) 
            return True
        nodes += 1
        
        for neighbor in state.expand():      
            if tuple(neighbor.config) not in unvisit:
                if tuple(neighbor.config) not in explored:
                    frontier.append(neighbor)
                    unvisit.add(tuple(neighbor.config))
            
    return False

def dfs_search(initial_state):
    """DFS search"""
    ### STUDENT CODE GOES HERE ###
    dfs_start_ram = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    start_time  = time.time()
    frontier = []
    frontier.append(initial_state)
    unvisit = set()
    unvisit.add(tuple(initial_state.config))
    explored = set()
    nodes = 0
    max_depth = 0

    while frontier:
        state = frontier.pop(-1)
        explored.add(tuple(state.config))
        max_depth = max(state.depth,max_depth)

        if state.config == [0,1,2,3,4,5,6,7,8]:
            dfs_ram = (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss-dfs_start_ram)/(2**20)
            end_time = time.time()
            output = total_output(state,nodes,max_depth,end_time-start_time,dfs_ram)
            writeOutput(output) 
            return True
        nodes += 1

        for neighbor in reversed(state.expand()):      
            if tuple(neighbor.config) not in unvisit:
                if tuple(neighbor.config) not in explored:
                    frontier.append(neighbor)
                    unvisit.add(tuple(neighbor.config))
    return False

def A_star_search(initial_state):
    """A * search"""
    ### STUDENT CODE GOES HERE ###
    start_time  = time.time()
    dfs_start_ram = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    frontier = []
    initial_state = calculate_total_cost(initial_state)
    frontier.append(initial_state)
    unvisit = set()
    unvisit.add(tuple(initial_state.config))
    explored = set()
    nodes = 0
    max_depth = 0
    
    while frontier:
        frontier = sorted(frontier, key = lambda state: state.cost)
        state = frontier.pop(0)
        explored.add(state)
        max_depth = max(state.depth,max_depth)

        if state.config == [0,1,2,3,4,5,6,7,8]:
            dfs_ram = (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss-dfs_start_ram)/(2**20)
            end_time = time.time()
            output = total_output(state,nodes,max_depth,end_time-start_time,dfs_ram)
            writeOutput(output) 
            return True
        nodes += 1

        for neighbor in state.expand():
            neighbor = calculate_total_cost(neighbor)
            if tuple(neighbor.config) not in unvisit:
                if tuple(neighbor.config) not in explored:
                    frontier.append(neighbor)
                    unvisit.add(tuple(neighbor.config))
                
    print()
    return False

def calculate_total_cost(state):
    """calculate the total estimated cost of a state"""
    ### STUDENT CODE GOES HERE ###
    dis = 0

    for idx in range(len(state.config)):
        value = state.config[idx]
        est_cost = calculate_manhattan_dist(idx,value,int(math.sqrt(len(state.config))))
        dis = dis + est_cost
    ecost = dis + len(get_path(state))    
    state.cost = ecost 
    return state

def calculate_manhattan_dist(idx, value, n):
    """calculate the manhattan distance of a tile"""
    ### STUDENT CODE GOES HERE ###
    if value == 0:
        dis = 0
    else:
        x1 =idx % n
        y1 = idx // n
        x2 = value % n
        y2 = value // n
        dis = abs(x1-x2) +abs(y1-y2)
    return dis

def get_path(state):
    path =[]
    while not state.parent == None:
        path.insert(0, state.action)
        state = state.parent
    return path
    


# Main Function that reads in Input and Runs corresponding Algorithm
def main():

    search_mode = sys.argv[1].lower()
    begin_state = sys.argv[2].split(",")
    # search_mode = 'ast'
    # # begin_state =   6,1,8,4,0,2,7,3,5
    # begin_state =     8,6,4,2,1,3,5,7,0
    # # begin_state = 1,0,2,3,4,5,6,7,8

    begin_state = list(map(int, begin_state))
    board_size  = int(math.sqrt(len(begin_state)))
    hard_state  = PuzzleState(begin_state, board_size)
    start_time  = time.time()
    
    if   search_mode == "bfs": bfs_search(hard_state)
    elif search_mode == "dfs": dfs_search(hard_state)
    elif search_mode == "ast": A_star_search(hard_state)
    else: 
        print("Enter valid command arguments !")
        
    end_time = time.time()
    print("Program completed in %.3f second(s)"%(end_time-start_time))

if __name__ == '__main__':
    main()
