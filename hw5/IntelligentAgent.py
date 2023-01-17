from random import randint
from BaseAI import BaseAI
import time
import random
import math

#
# Time Limit Before Losing
maxTime = 0.2


#
# random fill
# class IntelligentAgent(BaseAI):
#     def getMove(self, grid):
#     # Selects a random move and returns it
#         moveset = grid.getAvailableMoves()
#         return random.choice(moveset)[0] if moveset else None

class IntelligentAgent(BaseAI):
    def getMove(self, grid):
        self.prevTime = time.process_time()
        self.depth_max = 8
        self.over = False
        moves = grid.getAvailableMoves()
        # print(moves)
        i = 0
        # while True:
        i +=1
        print(i)
        # self.depth_max += 2
        player_move = self.maximize(grid, -10 ** 9, 10 ** 9, 0)[0]
        # print(player_move)
        if player_move != None:
            final_move = player_move
        else:
            final_move = random.choice(moves)
        return final_move[0] if moves else None

    def updateAlarm(self, currTime):
        if currTime - self.prevTime > maxTime:
            self.over = True

    def minimize(self, num, grid, alpha, beta, depth):
        if grid.getAvailableCells() == []:
            return self.evaluate(grid)

        if depth == self.depth_max:
            return self.evaluate(grid)

        self.updateAlarm(time.process_time())
        if self.over:
            return beta

        (min_cell, min_utility) = (None, 10 ** 9)

        for child_cell in grid.getAvailableCells():
            gridCopy = grid.clone()
            gridCopy.setCellValue(child_cell, num)
            utility = self.maximize(gridCopy, alpha, beta, depth + 1)[1]

            if utility < min_utility:  min_utility = utility
            if min_utility <= alpha: break
            if min_utility < beta: beta = min_utility

        return min_utility

    def maximize(self, grid, alpha, beta, depth):
        if grid.getAvailableMoves() == []:
            return (None, self.evaluate(grid))

        self.updateAlarm(time.process_time())
        if self.over:
            return (None, alpha)
        # Iniatilizing final move and utility
        (max_move, max_utility) = (None, -10 ** 9)

        for child_move in grid.getAvailableMoves():

            gridCopy = grid.clone()
            gridCopy.move(child_move)
            utility = self.chance(gridCopy, alpha, beta, depth)

            if utility > max_utility: (max_move, max_utility) = (child_move, utility)
            if max_utility >= beta: break
            if max_utility > alpha: alpha = max_utility
        # print("alpha" , alpha)
        return (max_move, max_utility)

    def chance(self, grid, alpha, beta, depth):
        chance_utility = 0.9 * self.minimize(2, grid, alpha, beta, depth) + 0.1 * self.minimize(4, grid, alpha, beta, depth)

        return chance_utility

    def evaluate(self, grid):
        (w1, w2, w3) = (0.2, 1, 1)
        ##heuristic number one : available number of tiles
        num = len(grid.getAvailableCells())
        mon = self.monotonicity(grid)
        id = self.identicity(grid)
          #* grid.getMaxTile()
        eval = w1 * num * grid.getMaxTile()  + w2 * mon + w3 * id
        return eval


    def monotonicity(self, grid):
        value = 0
        for i in range(grid.size - 1):
            for j in range(grid.size):
                if grid.map[i][j] == grid.map[i + 1][j] / 2:
                    value += grid.map[i + 1][j]

        for i in range(grid.size):
            for j in range(grid.size - 1):
                if grid.map[i][j] == grid.map[i][j + 1] / 2:
                    value += grid.map[i][j + 1]
        if value == 0:
            return value
        else:
            return math.log2(abs(value))

    def identicity(self, grid):
        value = 0
        
        for i in range(grid.size - 1):
            for j in range(grid.size):
                if grid.map[i][j] == grid.map[i + 1][j]:
                    value += grid.map[i][j]

        for i in range(grid.size):
            for j in range(grid.size - 1):
                if grid.map[i][j] == grid.map[i][j + 1]:
                    value += grid.map[i][j]
        if value == 0:
            return value
        else:
            return math.log2(abs(value))



