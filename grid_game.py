# grid_game.py
import random


class GridHuntGame:
    """A small Pacman-style grid environment (4x4) where an agent collects food."""

    def __init__(self, width=4, height=4):
        self.width = width
        self.height = height
        self.agent_pos = [0, 0]  # Starting position (x, y)

        # Place a few random food pellets and obstacles (walls)
        self.food_positions = {[1, 2], [2, 3], [3, 0], [2, 1]}
        self.walls = {[1, 1], [2, 2]}

        # Add toxic traps avoiding (0,0), walls, and food
        self.toxic_traps = {(0, 3), (3, 2)}

        self.score = 0
        self.steps = 0

    def get_percept(self, agent) -> dict:
        # Determine adjacent position based on current agent facing direction
        # Local percepts only (partially observable environment)
        x, y = self.agent_pos
        
        # Example checking local adjacent cells
        wall_ahead = (x + 1, y) in self.walls or x + 1 >= self.width
        food_here = tuple(self.agent_pos) in self.food_positions
        
        return {
            'wall_ahead': wall_ahead,
            'food_here': food_here,
            'score': self.score
        }

    def execute_action(self, agent, action: str):
        self.steps += 1
        new_pos = list(self.agent_pos)

        if action == 'Up':
            new_pos[1] = min(self.height - 1, new_pos[1] + 1)
        elif action == 'Down':
            new_pos[1] = max(0, new_pos[1] - 1)
        elif action == 'Left':
            new_pos[0] = max(0, new_pos[0] - 1)
        elif action == 'Right':
            new_pos[0] = min(self.width - 1, new_pos[0] + 1)

        # Check collision with walls
        if tuple(new_pos) in self.walls:
            self.score -= 5  # Penalty for hitting a wall
        else:
            self.agent_pos = new_pos

        # Check if eating food
        tuple_pos = tuple(self.agent_pos)
        if tuple_pos in self.food_positions:
            self.food_positions.remove(tuple_pos)
            self.score += 20  # Reward for eating food pellet
        
        # Check collision with toxic traps
        if tuple_pos in self.toxic_traps:
            self.score -= 15  # Penalty for stepping on a trap

    def is_done(self) -> bool:
        return len(self.food_positions) == 0 or self.steps >= 20

class SimpleReflexAgent:
    
    def sense_and_act(self, percept: dict) -> str:
        # Condition-Action Rules
        if percept['food_here']:
            return 'Eat'
        elif percept['wall_ahead']:
            return 'Left'  # Turn left when facing a wall
        else:
            return 'Right'  # Move/explore otherwise

class ModelBasedAgent:
    
    def __init__(self):
        self.visited_cells = set()  # Internal memory/state tracking
        self.last_action = None

    def sense_and_act(self, percept: dict) -> str:
        # Update internal state (Transition & Sensor Model)
        # Using current percepts and past actions to update memory
        
        if percept['food_here']:
            action = 'Eat'
        elif percept['wall_ahead']:
            # Use memory state to choose an alternate action and break infinite loops
            action = 'Down' if 'Left' in self.visited_cells else 'Left'
        else:
            action = 'Right'
            
        self.visited_cells.add(action)
        self.last_action = action
        return action