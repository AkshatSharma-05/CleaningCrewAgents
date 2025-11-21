# 🧹 Robot Cleaning Crew Simulation

### A simple yet visually engaging robot cleaning crew simulation built with Python 3.11 and Pygame.
Multiple autonomous cleaner robots move around the environment, pick up dirt, and dispose of it in a dustbin — all in real time.

## 🚀 Features

🤖 Autonomous robot cleaners with individual behaviors

🗑️ Smart dirt collection and disposal at a central dustbin

🔁 Continuous simulation with smooth movement

🧱 Grid-based floor tiles for a clean visual environment

👆 Interactive dirt placement — click anywhere to add new dirt

🧠 Coordinator system that assigns nearest tasks to each robot

## 🛠 Requirements

Python 3.11

Pygame must be installed beforehand

## 📝 How It Works

### The environment is rendered using Pygame and updated at 60 FPS.

### Robots look for the nearest dirt spot and move toward it.

### After collecting dirt, they automatically navigate to the dustbin.

### Clicking anywhere on the screen adds a new dirt spot.