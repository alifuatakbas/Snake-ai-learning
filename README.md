# Snake AI Learning with Deep Q-Learning

A sophisticated implementation of an autonomous Snake game agent using Deep Q-Learning (DQN). This project demonstrates the application of reinforcement learning techniques in game environments, specifically focusing on the classic Snake game.

## Overview

This project implements a Deep Q-Network (DQN) to train an AI agent to play Snake. The agent learns optimal strategies through experience replay and neural network-based Q-value approximation, showcasing practical applications of reinforcement learning concepts.

## Technical Architecture

### Core Components

- **DQN Agent**: Implements the Deep Q-Learning algorithm with experience replay
- **Game Environment**: Custom Snake game implementation optimized for AI training
- **Neural Network**: TensorFlow-based architecture for Q-value approximation

### Key Features

- Deep Q-Learning implementation with experience replay memory
- Configurable neural network architecture and hyperparameters
- Real-time visualization of training progress and metrics
- Modular codebase with clear separation of concerns

## Installation
1. Clone the repository:
bash
git clone https://github.com/alifuatakbas/Snake-ai-learning.git
cd Snake-ai-learning

3. Set up virtual environment:
```
python -m venv .venv

.venv\Scripts\activate
```


  ai/ # AI Implementation
	
    agent.py # DQN Agent implementation
    memory.py # Experience replay mechanism
    model.py # Neural network architecture
    trainer.py
  
  game/ # Game Environment
	
    snake.py # Snake game mechanics
    food.py # Food generation logic
    game_state.py
    constants.py

  ui/ # Visualization
	
    menu.py
    game_window.py

## Technical Details

### DQN Implementation
- State space: Current game state representation
- Action space: Four possible movements
- Reward structure: Optimized for learning efficient pathfinding
- Experience replay: Randomized batch sampling for stable learning

### Neural Network Architecture
- Input layer: Game state representation
- Hidden layers: Configurable dense layers
- Output layer: Q-values for each possible action

## Requirements

- Python 3.10
- TensorFlow
- NumPy
- Pygame

## Usage

Execute the main training script: 
```
python main.py
```
## Contact
- GitHub: [alifuatakbas](https://github.com/alifuatakbas)


sadadsada

 
