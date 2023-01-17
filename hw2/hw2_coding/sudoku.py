#!/usr/bin/env python
#coding:utf-8

"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""

import sys
import time



ROW = "ABCDEFGHI"
COL = "123456789"

flag = True

def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)


def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)


def Blanks(board):
    blanks = set()
    for r in ROW:
        for c in COL:
            if board[r + c] == 0:
                blanks.add(r + c)
    return blanks


def RV(var):

    R = var[0]
    C = var[1]
    RV = set()
    _RV = set()
    for r in ROW:
        if board[r + C] != 0 :
            _RV.add(board[r + C])
    for c in COL:
        if board[R + c] != 0:
            _RV.add(board[R + c])
     
    boxr = (ord(R)-65) - (ord(R)-65)%3
    boxc = (int(C)-1) - (int(C)-1)%3
    for i in range(3):
        for j in range(3):
            tempx  = chr(i + 64 + boxr + 1) 
            tempy = str(j + boxc + 1)
            if board[tempx+tempy] !=0:
                _RV.add(board[tempx+tempy])
    RV = {1,2,3,4,5,6,7,8,9} - _RV
    return RV

def alldone(board):
    for r in ROW:
        for c in COL:
            if board[r+c] == 0:
                return False
    return True

def val(board):
    blanks = Blanks(board)
    val = {}
    for i in blanks:
        val[i] = RV(i)
    return val

def checkempty(val):
    for i in val.keys():
        if len(val[i]) == 0:
            return True
    return False

def getBlank(valls):
    if len(valls) == 0:
        return 0
    # s_val = sorted(valls, key=lambda k: len(valls[k]), reverse=False)
    s_val= min(valls, key=lambda k: len(valls[k]))
    return s_val



def backtracking(board):
    """Takes a board and returns solved board."""
    # TODO: implement this
    valls = val(board)
    
    if len(valls) == 0:
        return board

        
    else:  
        blank = getBlank(valls)

        for value in valls[blank]:
          
            board[blank] = value
            
            if not checkempty(val(board)): 
                backtracking(board)
                if  alldone(board):
                    return board

            board[blank] = 0

    

        
    



if __name__ == '__main__':
    if len(sys.argv) > 1:
        
        # Running sudoku solver with one board $python3 sudoku.py <input_string>.
        # print(sys.argv[1])
        # Parse boards to dict representation, scanning board L to R, Up to Down
        board = { ROW[r] + COL[c]: int(sys.argv[1][9*r+c])
                  for r in range(9) for c in range(9)}       
        
        solved_board = backtracking(board)
        
        # Write board to file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")
        outfile.write(board_to_string(board))
        outfile.write('\n')

    else:
        # Running sudoku solver for boards in sudokus_start.txt $python3 sudoku.py
        start_time = time.time()

        #  Read boards from source.
        src_filename = 'sudokus_start.txt'
        try:
            srcfile = open(src_filename, "r")
            sudoku_list = srcfile.read()
        except:
            print("Error reading the sudoku file %s" % src_filename)
            exit()

        # Setup output file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")
        number_sudoku =0
        # Solve each board using backtracking
        for line in sudoku_list.split("\n"):
            # start_time = time.time()
            number_sudoku += 1
            if len(line) < 9:
                continue

            # Parse boards to dict representation, scanning board L to R, Up to Down
            board = { ROW[r] + COL[c]: int(line[9*r+c])
                      for r in range(9) for c in range(9)}

            
            # Print starting board. TODO: Comment this out when timing runs.
            
            # print_board(board)

            # Solve with backtracking
            solve_board = backtracking(board)

            # Print solved board. TODO: Comment this out when timing runs.
            
            print_board(board)

            # Write board to file
            outfile.write(board_to_string(board))
            outfile.write('\n')
            # end_time = time.time()
            # totime = end_time - start_time
            # outfile.write(str(totime))
            # outfile.write('\n')
        
        end_time = time.time()
        print("Program completed in %.3f second(s)" % (end_time - start_time))
        print(number_sudoku)
        print("Finishing all boards in file.")