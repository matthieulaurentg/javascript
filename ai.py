import pygame
import sys
import numpy as np
import random
from collections import defaultdict

# Initialize Pygame
pygame.init()

# Constants
GRID_SIZE = 5
CELL_SIZE = 100
WINDOW_SIZE = GRID_SIZE * CELL_SIZE
FPS = 5

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

# Set up the display
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("AI Tag Game")
clock = pygame.time.Clock()

class TagEnvironment:
    def __init__(self, size=GRID_SIZE):
        self.size = size
        self.reset()

    def reset(self):
        self.chaser_pos = (random.randint(0, self.size-1), random.randint(0, self.size-1))
        self.runner_pos = (random.randint(0, self.size-1), random.randint(0, self.size-1))
        while self.chaser_pos == self.runner_pos:
            self.runner_pos = (random.randint(0, self.size-1), random.randint(0, self.size-1))
        return self.get_state()

    def get_state(self):
        return self.chaser_pos + self.runner_pos

    def step(self, chaser_action, runner_action):
        # Move chaser
        self.chaser_pos = self.move(self.chaser_pos, chaser_action)
        
        # Check if chaser caught runner
        if self.chaser_pos == self.runner_pos:
            return self.get_state(), 1, True  # state, reward, done
        
        # Move runner
        self.runner_pos = self.move(self.runner_pos, runner_action)
        
        # Check if chaser caught runner after runner's move
        if self.chaser_pos == self.runner_pos:
            return self.get_state(), 1, True  # state, reward, done
        
        return self.get_state(), 0, False  # state, reward, done

    def move(self, pos, action):
        x, y = pos
        if action == 0:  # up
            y = max(0, y - 1)
        elif action == 1:  # down
            y = min(self.size - 1, y + 1)
        elif action == 2:  # left
            x = max(0, x - 1)
        elif action == 3:  # right
            x = min(self.size - 1, x + 1)
        return (x, y)

class QLearningAgent:
    def __init__(self, actions, learning_rate=0.1, discount_factor=0.95, epsilon=0.1):
        self.q_table = defaultdict(lambda: np.zeros(actions))
        self.lr = learning_rate
        self.gamma = discount_factor
        self.epsilon = epsilon
        self.actions = actions

    def get_action(self, state):
        if random.uniform(0, 1) < self.epsilon:
            return random.randint(0, self.actions - 1)  # Explore
        else:
            return np.argmax(self.q_table[state])  # Exploit

    def learn(self, state, action, reward, next_state):
        predict = self.q_table[state][action]
        target = reward + self.gamma * np.max(self.q_table[next_state])
        self.q_table[state][action] += self.lr * (target - predict)

def draw_grid():
    for x in range(0, WINDOW_SIZE, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, WINDOW_SIZE))
    for y in range(0, WINDOW_SIZE, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WINDOW_SIZE, y))

def draw_agents(chaser_pos, runner_pos):
    chaser_x, chaser_y = chaser_pos
    runner_x, runner_y = runner_pos
    
    pygame.draw.circle(screen, RED, (chaser_x * CELL_SIZE + CELL_SIZE // 2, chaser_y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)
    pygame.draw.circle(screen, BLUE, (runner_x * CELL_SIZE + CELL_SIZE // 2, runner_y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)

def play_game(env, chaser, runner, episodes=1000):
    for episode in range(episodes):
        state = env.reset()
        done = False
        
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            screen.fill(WHITE)
            draw_grid()
            draw_agents(env.chaser_pos, env.runner_pos)
            pygame.display.flip()
            clock.tick(FPS)

            chaser_action = chaser.get_action(state)
            runner_action = runner.get_action(state)
            
            next_state, reward, done = env.step(chaser_action, runner_action)
            
            chaser.learn(state, chaser_action, reward, next_state)
            runner.learn(state, runner_action, -reward, next_state)
            
            state = next_state

        print(f"Episode {episode + 1} completed")

    print("Training completed.")

# Create environment and agents
env = TagEnvironment()
chaser = QLearningAgent(actions=4)  # 4 actions: up, down, left, right
runner = QLearningAgent(actions=4)

# Train the agents
play_game(env, chaser, runner, episodes=1000)

pygame.quit()