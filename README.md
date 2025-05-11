# Tower Defense

This project is a strategic tower defense game where players must defend their base by strategically placing towers to stop waves of enemies. The game includes various tower types, enemy types, and mechanics to enhance the gameplay experience.

## Project Screenshot

![Gameplay Screenshot](screenshots/gameplay/menu.png)

## Python Version

Requires Python >= 3.10

## Current Features

- Multiple tower types with unique abilities and upgrade options.
- Various enemy types with different behaviors and strengths.
- A wave system that increases in difficulty as the game progresses.
- Resource management mechanics for building and upgrading towers.
- The game ends only when the enemies successfully reach the final destination.
- Map Selection: Players can choose from multiple maps to play, each offering unique layouts and challenges.

## How to run the application

1. Clone the repository
    ```bash
    git clone https://github.com/Skiffet/Tower-Defense.git
    ```
2. cd into the project directory
    ```bash
    cd Tower-Defense
    ```
3. Create a virtual environment by running the following command in the terminal:
    ```bash
    python -m venv venv
    ```
4. Activate the virtual environment by running the following command in the terminal:

    **MacOS or Linux:**
    ```bash
    source venv/bin/activate
    ```

    **Windows:**
    ```bash
    venv\Scripts\activate
    ```
5. Install the required packages by running the following command in the terminal:
    ```bash
    pip install -r requirements.txt
    ```
6. Run the application by executing the following command:
    ```bash
    python main_menu.py
    ```