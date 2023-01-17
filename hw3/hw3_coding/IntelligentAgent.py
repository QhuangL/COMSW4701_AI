from random import randint

from BaseAI import BaseAI
import time
import random
import math
from Displayer import Displayer

#
# Time Limit Before Losing
maxTime = 0.15

mon_matrix = [[1, 2, 3, 4],
              [2, 3, 4, 5],
              [3, 4, 7, 6],
              [4, 5, 6, 7]]



class IntelligentAgent(BaseAI):

    def getMove(self, grid):
        self.prevTime = time.process_time()
        self.depth_max = 3
        self.over = False
        while self.over == False:
            moves = grid.getAvailableMoves()
            player_move = self.maximize(grid, -float('inf'), float('inf'), 0)[0]
            # print(player_move)
            if player_move != None:
                final_move = player_move

        return final_move[0] if moves else None

    def updateAlarm(self, currTime):
        if currTime - self.prevTime > maxTime:
            self.over = True

    def minimize(self, grid, alpha, beta, depth):
        self.updateAlarm(time.process_time())
        if grid.getAvailableCells() == [] or self.over or depth >= self.depth_max:
            return self.evaluate(grid)

        min_utility = float('inf')

        for child_cell in grid.getAvailableCells():
            # gridCopy = grid.clone()

            # grid.setCellValue(child_cell, num)
            utility = self.chance(grid, child_cell, alpha, beta, depth)

            if utility < min_utility:  min_utility = utility
            if min_utility <= alpha: break
            if min_utility < beta: beta = min_utility

        return min_utility

    def maximize(self, grid, alpha, beta, depth):
        self.updateAlarm(time.process_time())
        if grid.getAvailableMoves() == [] or self.over or depth >= self.depth_max:
            return (None, self.evaluate(grid))

        (max_move, max_utility) = (None, -float('inf'))

        for child_move in grid.getAvailableMoves():
            utility = self.minimize(child_move[1], alpha, beta, depth + 1)
            if utility > max_utility: (max_move, max_utility) = (child_move, utility)
            if max_utility >= beta: break
            if max_utility > alpha: alpha = max_utility
        return (max_move, max_utility)

    def chance(self, grid, cell, alpha, beta, depth):
        chance_utility = 0
        if depth >= self.depth_max:
            return self.evaluate(grid)

        for tile, pro in {(2, 0.9), (4, 0.1)}:
            gridCopy = grid.clone()
            gridCopy.insertTile(cell, tile)
            (_, utility) = self.maximize(gridCopy, alpha, beta, depth)
            chance_utility += utility * pro
        return chance_utility

    def evaluate(self, grid):
        num = len(grid.getAvailableCells())
        mon = self.monotonicity(grid)
        id = self.smoothness(grid)

        # print(mon * num, id * 100 * grid.getMaxTile())
        eval = mon * num* 8  - id * 100 * grid.getMaxTile()
        return eval

    def monotonicity(self, grid):
        value  =0
        for i in range(4):
            for j in range(4):
                    value += (mon_matrix[i][j]**4) * grid.map[i][j]

        return value


    def smoothness(self, grid):
        value = 0
        for i in range(3):
            for j in range(4):
                if grid.map[i][j] - grid.map[i + 1][j] != 0:
                    # value += 1
                    value += abs(grid.map[i][j] - grid.map[i + 1][j])

        for i in range(4):
            for j in range(3):
                if grid.map[i][j] - grid.map[i][j + 1] != 0:
                    # value += 1
                    value += (abs(grid.map[i][j] - grid.map[i][j + 1]))

        return value

