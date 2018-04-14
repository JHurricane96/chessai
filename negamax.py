import chess
from evaluator import evaluator
import transTable

class MoveSelector(object):
	def __init__(self, maxIterMtd, maxSearchDepth, maxEvalScore):
		self._maxIterMtd = maxIterMtd
		self._maxSearchDepth = maxSearchDepth
		self._maxEvalScore = maxEvalScore
		self._transTable = transTable.transTable()

	def _abNegamax(self, board, maxDepth, depth, alpha, beta):
		alphaOriginal = alpha

		zhash = board.zobrist_hash()
		entry = self._transTable.table.get(zhash)
		if entry and entry.depth >= maxDepth - depth:
			if entry.scoreType == self._transTable.EXACT_SCORE:
				self._transTable.hits = self._transTable.hits + 1
				return (entry.move, entry.score, entry.finalBoard)
			elif entry.scoreType == self._transTable.LOWER_BOUND_SCORE:
				alpha = max(alpha, entry.score)
			else:
				beta = min(beta, entry.score)
			if alpha >= beta:
				return (entry.move, entry.score, entry.finalBoard)

		newEntry = False
		if not entry:
			entry = transTable.transTableEntry()
			entry.zobristHash = zhash
			newEntry = True
			entry.result = board.result()
		entry.depth = maxDepth - depth
		entry.move = None

		#result = board.result()
		if (depth == maxDepth or entry.result != "*"):
			entry.score = evaluator(board, entry.result)
			entry.finalBoard = board
			if (self._transTable.size == self._transTable.maxSize and newEntry):
				self._transTable.table.popitem()
				self._transTable.size = self._transTable.size - 1
			self._transTable.table[entry.zobristHash] = entry
			self._transTable.size = self._transTable.size + 1
			return ('', entry.score, board)

		maxScore = -(1<<64)
		score = maxScore
		bestMove = None
		finalBoard = None

		for move in board.legal_moves:
			board.push(move)
			_, score, finalBoard = self._abNegamax(board, maxDepth, depth + 1, -beta, -alpha)
			score = -score
			board.pop()

			if score > maxScore:
				maxScore = score
				bestMove = move

			alpha = max(alpha, score)
			if alpha >= beta:
				break

		entry.score = maxScore
		entry.move = bestMove
		entry.finalBoard = finalBoard
		if maxScore <= alphaOriginal:
			entry.scoreType = self._transTable.UPPER_BOUND_SCORE
		elif maxScore >= beta:
			entry.scoreType = self._transTable.LOWER_BOUND_SCORE
		else:
			entry.scoreType = self._transTable.EXACT_SCORE
		if (self._transTable.size == self._transTable.maxSize and newEntry):
			self._transTable.table.popitem()
			self._transTable.size = self._transTable.size - 1
		self._transTable.table[entry.zobristHash] = entry
		self._transTable.size = self._transTable.size + 1
		return (bestMove, maxScore, finalBoard)

	def _mtd(self, board, maxDepth, firstGuess):
		guess = firstGuess
		finalBoard = None
		upperBound = self._maxEvalScore
		lowerBound = -self._maxEvalScore
		i = 0

		while lowerBound < upperBound and i < self._maxIterMtd:
			if guess == lowerBound:
				gamma = guess + 1
			else:
				gamma = guess
			move, guess, finalBoard = self._abNegamax(board, maxDepth, 0, gamma - 1, gamma)
			if guess < gamma:
				upperBound = guess
			else:
				lowerBound = guess
				i = i + 1
		return (move, guess, finalBoard)

	#MTDf
	def selectMove(self, board):
		guess1 = 1<<64
		guess2 = 1<<64
		finalBoard1 = None
		finalBoard2 = None

		for depth in range(2, self._maxSearchDepth + 1):
			if depth % 2 == 0:
				move, guess1, finalBoard1 = self._mtd(board, depth, guess1)
			else:
				move, guess2, finalBoard2 = self._mtd(board, depth, guess2)

		if self._maxSearchDepth % 2 == 0:
			return (move, guess1, finalBoard1)
		else:
			return (move, guess2, finalBoard2)

	def clearTransTable(self):
		self._transTable.table.clear()
		self._transTable.size = 0