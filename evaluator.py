import chess
import weights
import config

pawnScore = config.PAWN_SCORE
materialPnts = [pawnScore, 4 * pawnScore, int(round(4.1 * pawnScore)), 6 * pawnScore, 12 * pawnScore, 0]
phasePnts = [0, 1, 1, 2, 4, 0]

def evaluator(board, result):
	pnts = 0

	if not result == "*":
		if result[0] == "1":
			if result[1] == "/":
				pnts = 0
			else:
				pnts = config.MAX_SCORE
		else:
			pnts = -config.MAX_SCORE
		if (board.turn == False):
			pnts = -pnts
		return pnts

	matPnts = initPnts = endPnts = 0
	phase = totalPhase = 24

	for i in xrange(0, 64):
		piece = board.piece_at(i)
		if piece:
			phase -= phasePnts[piece.piece_type - 1]
			if piece.color:
				matPnts += materialPnts[piece.piece_type - 1]
				initPnts += weights.initPosPnts[piece.piece_type - 1][i]
				endPnts += weights.finalPosPnts[piece.piece_type - 1][i]
			else:
				matPnts -= materialPnts[piece.piece_type - 1]
				initPnts -= weights.initPosPnts[piece.piece_type - 1][63 - i]
				endPnts -= weights.finalPosPnts[piece.piece_type - 1][63 - i]


	phase = (phase * 256 + (totalPhase / 2)) / totalPhase
	pnts = matPnts + ((initPnts * (256 - phase)) + (endPnts * phase)) / 256

	if (board.turn == False):
		pnts = -pnts
	return pnts

def findFeatures(board, color):

	featuresRawInit = [[0 for i in range (0, 64)] for j in range (0, 6)]
	featuresRawFin = [[0 for i in range (0, 64)] for j in range (0, 6)]
	featuresInit = []
	featuresFin = []
	colorType = 1 if color else -1
	phase = totalPhase = 24

	for i in xrange(0, 64):
		piece = board.piece_at(i)
		if piece:
			phase -= phasePnts[piece.piece_type - 1]

	phase = (phase * 256 + (totalPhase / 2)) / totalPhase

	for i in xrange(0, 64):
		piece = board.piece_at(i)
		if piece:
			if piece.color:
				featuresRawInit[piece.piece_type - 1][i] += (256.0 - phase) / 256.0 * colorType
				featuresRawFin[piece.piece_type - 1][i] += phase / 256.0 * colorType
			else:
				featuresRawInit[piece.piece_type - 1][63 - i] -= (256.0 - phase) / 256.0 * colorType
				featuresRawFin[piece.piece_type - 1][63 - i] -= phase / 256.0 * colorType

	for j in range(6):
		for i in range(64):
			featuresInit.append(featuresRawInit[j][i])
			featuresFin.append(featuresRawFin[j][i])

	return (featuresInit, featuresFin)