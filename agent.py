import random
from collections import deque
import heapq
import math


class GreedyGridAgent:
    """A simple agent that tries to move around systematically to clear the grid."""

    def __init__(self):
        self.actions_pool = ['Up', 'Down', 'Left', 'Right']

    def sense_and_act(self, percept: dict) -> str:
        pos = percept['agent_pos']
        return random.choice(self.actions_pool)


class SearchAgent:
    """Part 1: Goal-Based Search Agent using BFS, DFS, and UCS strategies."""

    def __init__(self, active_algo='BFS'):
        self.plan = []
        self.active_algo = active_algo  # Options: 'BFS', 'DFS', 'UCS'

    def get_neighbors(self, state, grid_size, walls):
        x, y = state
        width, height = grid_size
        neighbors = []
        moves = [(0, 1, 'Up'), (0, -1, 'Down'), (-1, 0, 'Left'), (1, 0, 'Right')]

        for dx, dy, action in moves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in walls:
                neighbors.append(((nx, ny), action))
        return neighbors

    def bfs_search(self, start, goal, grid_size, walls):
        frontier = deque([(start, [])])
        reached = {start}

        while frontier:
            state, path = frontier.popleft()
            if state == goal:
                return path

            for neighbor, action in self.get_neighbors(state, grid_size, walls):
                if neighbor not in reached:
                    reached.add(neighbor)
                    frontier.append((neighbor, path + [action]))
        return []

    def dfs_search(self, start, goal, grid_size, walls):
        frontier = [(start, [])]
        reached = {start}

        while frontier:
            state, path = frontier.pop()
            if state == goal:
                return path

            for neighbor, action in self.get_neighbors(state, grid_size, walls):
                if neighbor not in reached:
                    reached.add(neighbor)
                    frontier.append((neighbor, path + [action]))
        return []

    def ucs_search(self, start, goal, grid_size, walls):
        frontier = [(0, start, [])]
        reached = {start: 0}

        while frontier:
            cost, state, path = heapq.heappop(frontier)
            if state == goal:
                return path

            for neighbor, action in self.get_neighbors(state, grid_size, walls):
                new_cost = cost + 1
                if neighbor not in reached or new_cost < reached[neighbor]:
                    reached[neighbor] = new_cost
                    heapq.heappush(frontier, (new_cost, neighbor, path + [action]))
        return []

    def sense_and_act(self, percept: dict) -> str:
        if not self.plan:
            start = percept['agent_pos']
            foods = percept['all_food']
            if not foods:
                return 'Up'

            goal = min(foods, key=lambda f: abs(f[0] - start[0]) + abs(f[1] - start[1]))
            grid_size = percept['grid_size']
            walls = set(percept['walls'])

            if self.active_algo == 'BFS':
                self.plan = self.bfs_search(start, goal, grid_size, walls)
            elif self.active_algo == 'DFS':
                self.plan = self.dfs_search(start, goal, grid_size, walls)
            elif self.active_algo == 'UCS':
                self.plan = self.ucs_search(start, goal, grid_size, walls)

        if self.plan:
            return self.plan.pop(0)
        return 'Up'
    
    def manhattan_distance(self, pos, goal):
        """Calculates Manhattan distance h(n) = |x1 - x2| + |y1 - y2|"""
        return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

    def euclidean_distance(self, pos, goal):
        """Calculates Euclidean distance h(n) = sqrt((x1 - x2)^2 + (y1 - y2)^2)"""
        return math.sqrt((pos[0] - goal[0]) ** 2 + (pos[1] - goal[1]) ** 2)

        if __name__ == '__main__':
            agent = SearchAgent()
            print("Manhattan (0,0) to (3,4):", agent.manhattan_distance((0, 0), (3, 4)))  # Returns 7
            print("Euclidean (0,0) to (3,4):", agent.euclidean_distance((0, 0), (3, 4)))  # Returns 5.0

    def sense_and_act(self, percept: dict) -> str:
        if not self.plan:
            start = percept['agent_pos']
            foods = percept['all_food']
            if not foods:
                return 'Up'

            # Find closest food pellet by Manhattan distance
            goal = min(foods, key=lambda f: self.manhattan_distance(start, f))
            grid_size = percept['grid_size']
            walls = set(percept['walls'])

            if self.active_algo == 'BFS':
                self.plan = self.bfs_search(start, goal, grid_size, walls)
            elif self.active_algo == 'DFS':
                self.plan = self.dfs_search(start, goal, grid_size, walls)
            elif self.active_algo == 'UCS':
                self.plan = self.ucs_search(start, goal, grid_size, walls)
            elif self.active_algo == 'AStar':
                self.plan = self.astar_search(start, goal, walls, grid_size, heuristic_type='manhattan')

        if self.plan:
            return self.plan.pop(0)
        return 'Up'