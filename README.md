# Asteroids-Vectors

A Python game inspired by the classic Asteroids arcade title. The objective is to destroy incoming asteroids to earn points while avoiding collisions and managing movement, shooting, and survival under increasing difficulty.

This project was built to make mathematical vector concepts more concrete and visual. Instead of relying on a standard physics library, the game uses a custom 2D vector system to manage motion, acceleration, rotation, and collision behavior.

## Project Goals

- create a playable Asteroids-style game in Python
- model movement and physics using a custom vector mathematics system
- demonstrate object-oriented design in a game context
- implement collision behavior using a design pattern that cleanly separates logic

## Design Highlights

- Object-oriented game structure with distinct classes for the ship, asteroids, lasers, and game manager
- Custom 2D vector math used for movement, velocity, and position updates
- Collision handling implemented through the Double Dispatch pattern
- Centralized game loop and entity interaction logic in the game manager

## Tech Stack

- Python 3
- Pygame
- Custom 2D vector math engine
- Object-oriented programming
- Double Dispatch collision logic

## Local Setup

1. Clone the repository:
```bash
git clone https://github.com/jasonbussiere/asteroids-python-vectors.git
cd asteroids-python-vectors
```

2. Install dependencies:
```bash
pip install pygame-ce
```

3. Run the game:
```bash
python main.py
```

## Preview

![Asteroids gameplay](https://github.com/user-attachments/assets/fc4b4353-4e61-4703-80cf-addd80291b4b)

## Notes

This project is useful as a portfolio piece because it shows:
- game development fundamentals
- mathematics applied in software
- custom physics modeling
- clean object-oriented architecture
- practical problem-solving through simulation
