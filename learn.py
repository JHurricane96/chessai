import chess
import random
import chess.pgn
from negamax import MoveSelector
from weightsHandler import WeightsHandler
import evaluator
import config

def main():
	# Open PGN file with games database
	gamesFile = open(config.GAMES_FILE_NAME)

	# Initialize counter
	gamesCounter = 0
	# Initialize move selection module
	moveSelector = MoveSelector(config.MAX_ITER_MTD, config.MAX_DEPTH, config.MAX_SCORE)
	# Initialize weight-handling module
	weightsHandler = WeightsHandler("weights.py")
	# Initialize learning rate
	learningRate = config.ALPHA_INIT

	# Loop over recorded games in file until counter reaches limit
	while gamesCounter < config.MAX_GAMES:
		# Get a game
		game = chess.pgn.read_game(gamesFile)
		try:
			game.variation(0)
		except KeyError:
			continue
		if not game:
			break

		# Find the winner
		whitePnt = game.headers["Result"][0]
		if whitePnt == "1" and game.headers["Result"][1] != "/":
			winColor = chess.WHITE
		elif whitePnt == "0":
			winColor = chess.BLACK
		else:
			continue

		print("\nGame ", gamesCounter + 1)

		# Clear transposition table
		moveSelector.clearTransTable()

		# Play as both black and white
		for color in range(2):
			# Use local copy of game
			state = game
			# Get board object from game
			board = state.board()
			# Initialize list of board and board scores
			scores = []
			boards = [board.copy()]
			# Initialize features list
			featuresInit = []
			featuresFinal = []
			# Initialize turn counter
			turnCounter = 0
			if color:
				print("White")
			else:
				print("Black")

			# Loop through game, move by move
			while not state.is_end():
				# Get next board position
				state = state.variation(0)
				board = state.board()
				# If computer's turn to move
				if board.turn == color:
					# Get score of board and position that computer aims to reach
					_, score, finalBoard = moveSelector.selectMove(board)
					# Store score, finalBoard and features of finalBoard
					scores.append(score)
					boards.append(finalBoard)
					fI, fF = evaluator.findFeatures(finalBoard, color)
					featuresInit.append(fI)
					featuresFinal.append(fF)

					turnCounter = turnCounter + 1
					print("Turn ", turnCounter, '\r', end='')
			print('\n', end='')

			# Depending on winner, store final score
			if winColor == color:
				scores.append(config.MAX_SCORE)
			else:
				scores.append(-config.MAX_SCORE)

			# Learn weights
			initPosWeights, finalPosWeights = weightsHandler.getWeights()
			initPosWeights, finalPosWeights = learn(
				initPosWeights,
				finalPosWeights,
				featuresInit,
				featuresFinal,
				scores,
				learningRate,
				config.LAMBDA,
				config.MAX_POSITION_SCORE
			)
			# Store weights
			weightsHandler.setWeights(initPosWeights, finalPosWeights)
			weightsHandler.writeWeightsToFile()
			# Decrease learning rate
			learningRate /= config.ALPHA_DEC_FACTOR

			# Debug info
			# print scores
			# print featuresInit[10]
			# print featuresFinal[10]
			# print moveSelector._transTable.hits
			# print moveSelector._transTable.notHits
			# print moveSelector._transTable.size
			# print initPosWeights

		# Done learning from one game, so increment game counter
		gamesCounter = gamesCounter + 1

	# Close file handlers when learning is complete
	weightsHandler.closeWeightsFile()
	gamesFile.close()

def learn(wRawInit, wRawFin, fInit, fFinal, J, alpha, lambdaDecay, clampVal):
	wInit = []
	wFin = []
	sizeJ = len(J)

	# Unrolling parameters into vector
	for j in range(6):
		for i in range(64):
			wInit.append(wRawInit[j][i])
			wFin.append(wRawFin[j][i])
	sizeW = len(wInit)

	# Calculate update amount (with sign) for parameters	
	updateMagInit = [0 for i in range(sizeW)]
	updateMagFinal = [0 for i in range(sizeW)]
	for t in range(sizeJ - 1):
		propTempDiff = 0 # Propagated temporal difference
		for j in range(t, sizeJ - 1):
			propTempDiff += lambdaDecay**(j - t) * (J[j + 1] - J[j])
		updateMagInit = [updateMagInit[i] + (propTempDiff * fInit[t][i]) for i in range(sizeW)]
		updateMagFinal = [updateMagFinal[i] + (propTempDiff * fFinal[t][i]) for i in range(sizeW)]

	# Update parameters
	for i in range(len(wInit)):
		wInit[i] += alpha * updateMagInit[i]
		wFin[i] += alpha * updateMagFinal[i]

	# Rolling parameter vector
	wRawInit = [[max(min(int(round(wInit[i + 64*j])), clampVal), -clampVal) for i in range (0, 64)] for j in range (0, 6)]
	wRawFin = [[max(min(int(round(wFin[i + 64*j])), clampVal), -clampVal) for i in range (0, 64)] for j in range (0, 6)]

	# Return final weights
	return (wRawInit, wRawFin)

if __name__ == "__main__":
	main()
