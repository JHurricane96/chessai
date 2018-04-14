class transTableEntry:
	zobristHash = 0
	scoreType = 0 #0 accurate; 1 lower bound; 2 upper bound
	score = 0
	bestMove = None
	finalBoard = None
	depth = 0 #From bottom
	result = ''

class transTable:
	table = {}
	size = 0
	maxSize = 10**8
	#debug info below
	hits = 0
	notHits = 0
	EXACT_SCORE = 0
	LOWER_BOUND_SCORE = 1
	UPPER_BOUND_SCORE = 2