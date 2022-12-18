# tap-ninja-bot
Visual bot for Tap Ninja. I made it in my spare time since the game is played alone, right, and now totally alone.

## Works ONLY for Windows

So, the bot is not user-friendly, you need to have some basic knowledge about programming in Python

Steps:
* Install Python 3
  * Mark the checkbox to add PATH
  * Accept to remove line length restriction (after installation)
* Clone the repo to any path
* Create a virtual environment, inside the root folder of the repo you just cloned, in the cmd or PowerShell
  * `python -m venv venv`
* Activate env
  * `.\venv\Scripts\activate`
* install requirements
  * `pip install -r requirements.txt`
* Calibrate buttons positions and stuff (Press 'F' to set). Follow the steps provided
  * `python manage.py cee`
  * You have to open Tap Ninja
  * Then move to where it tells you
* Run the bot with
  * `python manage.py runbot`

You can see the color or positions with
* `python manage.py mcc` color
* `python manage.py mcp` position
