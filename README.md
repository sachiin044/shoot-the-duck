# Duck Hunt - Production Quality

A modular, production-quality Duck Hunt clone built with Python and Pygame.

## 🚀 Architecture

The game follows a clean, modular architecture with clear separation of concerns:

- **Entities**: Independent objects like `Duck` and `Player` (Crosshair).
- **Systems**: Decoupled managers for `Collision`, `Spawner`, `ScoreManager`, and `StateManager`.
- **UI**: Dedicated `HUD` and screen rendering logic.
- **Config**: Centralized game constants and tuning parameters.

### Tech Stack
- **Python 3.10+**
- **Pygame**

## 🎮 How to Play

1. **Start**: Click anywhere on the menu screen.
2. **Aim**: Move your mouse to control the crosshair.
3. **Shoot**: Click the left mouse button to fire.
4. **Reload**: Automatic reload happens when you run out of bullets (3 shots).
5. **Goal**: Shoot ducks to score points. The game gets faster and harder every round.
6. **Game Over**: If you miss 5 ducks, the game ends.

## 🛠️ Run Instructions

Ensure you have Pygame installed:
```bash
pip install pygame
```

Run the game:
```bash
python main.py
```

## 📂 Project Structure

- `main.py`: Entry point and game loop orchestration.
- `config.py`: Game settings and constants.
- `assets_util.py`: Utility for generating programmatic placeholder assets.
- `entities/`: Duck and Player classes.
- `systems/`: Spawner, Score, State management.
- `ui/`: Head-up display and menus.
