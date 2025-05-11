# Tower Defense

## Overview

Tower Defense is a strategic game where players must defend their base by placing towers to stop waves of enemies. The game is designed to challenge players' planning and resource management skills, offering various tower and enemy types, as well as multiple maps for diverse gameplay experiences.

## Motivation

We created this game to help players practice strategic thinking and resource management in a fun and interactive way. The challenge of defending against increasingly difficult waves of enemies encourages players to plan ahead and adapt their strategies.

## User Story

As a player, I want to place different types of towers to stop enemies from reaching my base, so that I can achieve a high score and improve my tactical skills.

## Game Concept

Players must defend their base by strategically placing towers to stop waves of enemies. When players defeat monsters, they earn money, which can be used to place additional towers or upgrade existing ones. The game ends only when the monsters successfully reach the final destination, and the player's score along with the time taken to play the game will be displayed.

## UML Class Diagram

![UML Diagram](https://raw.githubusercontent.com/Skiffet/Tower-Defense/main/Diagram.jpg)

## Class Responsibility Table

| Class      | Responsibility                        |
|------------|---------------------------------------|
| Game       | Game loop, state management           |
| Tower      | Tower logic, attack, upgrade          |
| Monster    | Enemy movement, health        |
| MapLoader  | Load and manage map data              |
| MainMenu   | Main menu and navigation              |
| Analyze    | Data collection and visualization     |

## Game Metrics Table

| Metric              | Description                                                                                         | How to Measure / Calculate                              | Variable / Field in Code                | Visualization / Output Type                |
|---------------------|-----------------------------------------------------------------------------------------------------|---------------------------------------------------------|-----------------------------------------|--------------------------------------------|
| **Damage**          | Measures total offensive output from all towers.                                                    | Sum damage dealt during each game.                      | total_damage in the Game class          | Graph (Line Chart / Stacked Bar)           |
| **Score**           | Overall measure of performance and game success.                                                    | Accumulate score through monster kills.                 | score in the Game class                 | Table (Average, Max, Percentile)           |
| **Tower Type Usage**| Identify which towers are most used. Useful for game balance and player preference analysis.         | Count how many times each of Tower1, Tower2, Tower3 is placed | tower_count[10/20/30] in Game class    | Graph (Pie Chart)                          |

## Data Component

The game collects and visualizes the following data:
- **Damage:** Total offensive output from all towers.
- **Score:** Overall measure of performance and game success.
- **Tower Type Usage:** Which towers are most used.
- **Tower Upgrade Usage:** How often each tower is upgraded.
- **Money Spent:** Total in-game currency spent.
- **Enemies Killed:** Number of enemies defeated.
- **Waves Survived:** Number of enemy waves survived.
- **Play Time:** Total time spent in a game session.

These data are visualized in tables and graphs (line charts, bar charts, pie charts) to help analyze player performance and game balance.

## Design Patterns

- **Singleton:** Used for managing game state.
- **Factory:** For creating different types of towers and enemies.
- **Observer:** For updating UI elements when game state changes.

## Extra Features

- Map selection with unique layouts and challenges.
- Data visualization page for performance analysis.
- [Add any other extra features here.]

## Limitations / Known Issues

- No save/load feature in this version.

## Future Work / Improvements

- Add multiplayer support.
- Implement save/load functionality.
- More tower and enemy types.

## YouTube Presentation

[Watch the project presentation on YouTube](https://youtu.be/XCsNagxhAAg)

## GitHub Repository

[https://github.com/Skiffet/Tower-Defense](https://github.com/Skiffet/Tower-Defense)