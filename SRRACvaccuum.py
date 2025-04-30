import random
from collections import namedtuple

class Environment:
    def __init__(self, width, height, dirt_probability , obstacle_probability):
        self.width = width
        self.height = height
        self.grid = [[random.random() < dirt_probability for _ in range(width)] for _ in range(height)]
        self.obstacles = [[random.random() < obstacle_probability for _ in range(width)] for _ in range(height)]
        self.agent_position = (0, 0)

    def is_dirty(self, x, y):
        return self.grid[y][x]

    def is_obstacle(self, x, y):
        return self.obstacles[y][x]

    def clean(self, x, y):
        self.grid[y][x] = False

    def move_agent(self, new_x, new_y):
        if 0 <= new_x < self.width and 0 <= new_y < self.height:
            self.agent_position = (new_x, new_y)

    def display(self):
        
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if (x, y) == self.agent_position:
                    print("V", end=" ")
                elif self.is_obstacle(x, y):
                    print("X", end=" ")
                else:
                    print("D" if cell else "_", end=" ")
            print()
        print()
        

class VacuumCleaner:
    def __init__(self, environment):
        self.env = environment
        self.x, self.y = self.env.agent_position
        self.performance = 0
        self.visited = set()

    def perceive(self):
        return self.env.is_dirty(self.x, self.y)

    def clean(self):
        if self.perceive():
            self.env.clean(self.x, self.y)
            self.performance += 10

    def move(self, direction):
        dx, dy = direction
        new_x, new_y = self.x + dx, self.y + dy
        if 0 <= new_x < self.env.width and 0 <= new_y < self.env.height and not self.env.is_obstacle(new_x, new_y):
            self.env.move_agent(new_x, new_y)
            self.x, self.y = new_x, new_y
            self.performance -= 1
            self.visited.add((self.x,self.y))

    def act(self):
        if self.perceive():
            self.clean()
        else:
            self.move(self.check_surr())

    def check_surr(self):
        options = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        valid_options = []

        for dx, dy in options:
            new_x, new_y = self.x + dx, self.y + dy
            if (0 <= new_x < self.env.width and 0 <= new_y < self.env.height and
                    not self.env.is_obstacle(new_x, new_y)):
                valid_options.append((dx, dy))

        for dx, dy in valid_options:
            if self.env.is_dirty(self.x + dx, self.y + dy):
                return (dx, dy)
        
                # Use visited set to avoid revisiting
        unvisited_options = [(dx, dy) for dx, dy in valid_options if (self.x + dx, self.y + dy) not in self.visited]

        if unvisited_options:
            return random.choice(unvisited_options)
        elif valid_options:
            # Randomly choose from valid options
            return random.choice(valid_options)
        else:
            return (0, 0)
        
    def run(self, steps):
        for _ in range(steps):
            self.env.display()
            self.act()
        print("Final Performance Score:", self.performance)

if __name__ == "__main__":
    width=4
    height=4
    env = Environment(width, height, dirt_probability=0.5, obstacle_probability=0.25)
    vacuum = VacuumCleaner(env)
    vacuum.run(steps=width * height *2) 