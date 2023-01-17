from random import randint

from BaseAI import BaseAI
import time
import random
import math
from Displayer import Displayer

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
        self.depth_max = 4
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
        # if self.over:
        #     return self.evaluate(grid)
        # if depth >= self.depth_max:
        #     return self.evaluate(grid)
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
        # if self.over:
        #     return (None, self.evaluate(grid))
        #
        # if depth >= self.depth_max:
        #     return (None, self.evaluate(grid))

        # Iniatilizing final move and utility
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
        cor = self.corner(grid)
        if num >= 5:
            (w1, w2, w3, w4) = (1.5, 0.5, 1.8, 2)
        else:
            (w1, w2, w3, w4) = (1.5, 0.9, 2, 2)
        # print(" w1", num*w1, "w2:", mon*w2, "w3", id*w3/(16-num), "w4", w4*cor)  #, "id:", id, "sim:" , sim)
        eval = w1 * num + w2 * mon / (16 - num) + w3 * id / (16 - num) + w4 * cor
        return eval

    def monotonicity(self, grid):
        value = -self.col_mon(grid) - self.row_mon(grid)
        return value

    def col_mon(self, grid):
        value1 = 0
        value2 = 0
        for i in range(3):
            for j in range(4):
                if grid.map[i][j] == grid.map[i + 1][j] / 2:
                    value1 += 1

        for i in range(3):
            for j in range(4):
                if grid.map[i][j] == grid.map[i + 1][j] * 2:
                    value2 += 1
        return min(value1, value2)

    def row_mon(self, grid):
        value1 = 0
        value2 = 0
        for i in range(4):
            for j in range(3):
                if grid.map[i][j] == grid.map[i][j + 1] / 2:
                    value1 += 1

        for i in range(4):
            for j in range(3):
                if grid.map[i][j] == grid.map[i][j + 1] * 2:
                    value2 += 1
        return min(value1, value2)

    def smoothness(self, grid):
        value = 0
        for i in range(3):
            for j in range(4):
                if grid.map[i][j] - grid.map[i + 1][j] != 0:
                    value += -math.log2(abs(grid.map[i][j] - grid.map[i + 1][j]))

        for i in range(4):
            for j in range(3):
                if grid.map[i][j] - grid.map[i][j + 1] != 0:
                    value += -math.log2(abs(grid.map[i][j] - grid.map[i][j + 1]))

        return value

    def corner(self, grid):
        value = 0
        if grid.getCellValue((0, 0)) == grid.getMaxTile():
            return 1
        elif grid.getCellValue((0, 4)) == grid.getMaxTile():
            return 1
        elif grid.getCellValue((4, 0)) == grid.getMaxTile():
            return 1
        elif grid.getCellValue((4, 4)) == grid.getMaxTile():
            return 1
        else:
            value = -min(grid.getCellValue((0, 0)) if grid.getCellValue((0, 0)) else 0,
                         grid.getCellValue((0, 4)) if grid.getCellValue((0, 4)) else 0,
                         grid.getCellValue((4, 0)) if grid.getCellValue((4, 0)) else 0,
                         grid.getCellValue((4, 4)))if grid.getCellValue((4, 4)) else 0
            return (grid.getMaxTile()- value)/grid.getMaxTile()
        return 0
