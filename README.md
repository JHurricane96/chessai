# Chess AI

A chess artificial intelligence using the MTD-f algorithm for move selection  
and that can learn from old games. It uses the python-chess library for board  
representation, move generation, zobrist hashing and reading .pgn files.

----------

## Building

### Environment setup

1. Clone the repo.
2. Install python and virtualenv.
3. [Download pypy binary](http://pypy.org/download.html).
4. Run `virtualenv -p <pypy binary location here> <virtual env name here>`  
to set up your virtual environment.
5. Run `source <name of env>/bin/activate` to activate your virtual  
environment.
6. Run `pip install -r requirements.txt` to install dependencies.
7. Run `pypy main.py` to play against the AI.
8. Run `deactivate` to deactivate the virtual environment.

### Learning from dataset

1. Find and download a database of chess games in PGN format, or use [this](https://drive.google.com/file/d/0BwU3DiBuFdpWYnBBQWUtWXJTenM/view?usp=sharing).
2. Place the downloaded .pgn file in the project root.
3. In `config.py`, set `GAMES_FILE_NAME` to the name of the .pgn file. Feel  
free to tweak with other parameters too.
4. Run `pypy learn.py` to learn.