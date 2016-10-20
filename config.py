MAX_ITER_MTD = 100 # Maximum number of iterations in MTD
MAX_DEPTH = 3 # Maximum depth of negamax
PAWN_SCORE = 100 # Material score of a single pawn
MAX_POSITION_SCORE = PAWN_SCORE / 2 # Maximum score awarded in piece square tables
MAX_SCORE = PAWN_SCORE * 100 # Maximum score that is awarded in static evaluation

ALPHA_INIT = 0.001 # Initial learning rate
ALPHA_DEC_FACTOR = 1.0001 # Learning rate gets divided by this after every game
LAMBDA = 0.7 # Temporal decay factor
MAX_GAMES = 3 # Number of games to learn from

GAMES_FILE_NAME = "GMallboth.pgn"