import random
from agent import SearchAgent

class GridHuntGame:
    """A small Pacman-style grid environment (4x4) where an agent collects food."""

    def __init__(self, width=4, height=4):
        self.width = width
        self.height = height
        self.agent_pos = [0, 0]  # Starting position (x, y)

        # Fixed: Tuple elements inside sets
        self.food_positions = {(1, 2), (2, 3), (3, 0), (2, 1)}
        self.walls = {(1, 1), (2, 2)}

        # Add toxic traps avoiding (0,0), walls, and food
        self.toxic_traps = {(0, 3), (3, 2)}

        self.score = 0
        self.steps = 0

    def get_percept(self, agent) -> dict:
        x, y = self.agent_pos
        wall_ahead = (x + 1, y) in self.walls or (x + 1) >= self.width
        food_here = tuple(self.agent_pos) in self.food_positions

        return {
            'agent_pos': tuple(self.agent_pos),
            'wall_ahead': wall_ahead,
            'food_here': food_here,
            'score': self.score,
            'grid_size': (self.width, self.height),
            'walls': list(self.walls),
            'all_food': list(self.food_positions)
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
        if percept['food_here']:
            action = 'Eat'
        elif percept['wall_ahead']:
            action = 'Down' if 'Left' in self.visited_cells else 'Left'
        else:
            action = 'Right'

        self.visited_cells.add(action)
        self.last_action = action
        return action


if __name__ == '__main__':
    # Instantiate Game and SearchAgent (Change active_algo to 'BFS', 'DFS', or 'UCS')
    game = GridHuntGame()
    agent = SearchAgent(active_algo='DFS')

    print(f"--- Starting Simulation ({agent.active_algo}) ---")
    while not game.is_done():
        percept = game.get_percept(agent)
        action = agent.sense_and_act(percept)
        game.execute_action(agent, action)
        print(f"Step {game.steps}: Action={action:5s} | Position={game.agent_pos} | Score={game.score}")

    print("--- Simulation Ended ---")