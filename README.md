# Chess AI

A chess artificial intelligence using the MTD-f algorithm for move selection and that can learn from old games. It uses the python-chess library for board representation, move generation, zobrist hashing and reading .pgn files.

Temporal difference learning, a type of reinforcement learning, was used to train the AI. The inspiration for this work was [this paper](https://www.ismll.uni-hildesheim.de/lehre/semKIML-13w/script/chess.pdf).

## Demo

This is a match played by the AI against itself. White has a search depth of 2, and black has a search depth of 3. Black wins.

![](https://i.imgur.com/RGJON84.gif)

## Building

### Environment setup

1. Clone the repo.
2. Install python and virtualenv.
3. [Download pypy binary](http://pypy.org/download.html).
4. Run `virtualenv -p <pypy binary location here> venv` to set up your virtual environment.
5. Run `source venv/bin/activate` to activate your virtual environment.
6. Run `pip install -r requirements.txt` to install dependencies.
7. Run `pypy main.py` to play against the AI and `pypy self_play.py` to watch the AI play against itself.
8. Run `deactivate` to deactivate the virtual environment.

**Note:** `main.py` and `self_play.py` both have `MAX_DEPTH` constants that can be adjusted to change the AI's strength. Increase it to increase the strength and decrease it to decrease the strength.

### Learning from dataset

1. Find and download a database of chess games in PGN format, or use [this](https://drive.google.com/file/d/0BwU3DiBuFdpWYnBBQWUtWXJTenM/view?usp=sharing).
2. Place the downloaded .pgn file in the project root.
3. In `config.py`, set `GAMES_FILE_NAME` to the name of the .pgn file. Feel free to tweak with other parameters too.
4. Run `pypy learn.py` to learn.
