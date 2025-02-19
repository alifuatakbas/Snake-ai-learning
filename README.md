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
```
git clone https://github.com/alifuatakbas/Snake-ai-learning.git
```
3. Set up virtual environment:
```
python -m venv .venv

.venv\Scripts\activate

pip install -r "requirements.txt"
```

## Structure
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

## Training Results
 ![WhatsApp Görsel 2025-02-19 saat 04 24 39_a1672c0e](https://github.com/user-attachments/assets/ae7fc071-648b-4936-9c04-493214bc4aef)

 ### Analysis of Training Progress

The graph demonstrates the learning progression of our DQN agent over 777 episodes:

- **Blue Line (Score)**: Individual episode scores showing high variance
  - Initial scores (0-100 episodes): Low performance with scores around 0-2
  - Mid-training (200-400 episodes): Increasing volatility with occasional high scores
  - Late training (400+ episodes): Consistent high peaks reaching 20-25 points

- **Red Line (Mean Score)**: Moving average showing overall learning trend
  - Steady improvement from episodes 0 to 400
  - Stabilization around score 10 after episode 500
  - Final convergence at approximately score 10-11

This training pattern is characteristic of DQN learning:
1. Initial exploration phase with low scores
2. Rapid improvement during primary learning phase
3. Convergence to stable performance in later episodes

The variance in scores (blue line) indicates the agent still explores different strategies while maintaining a stable average performance, demonstrating successful learning without overfitting.

