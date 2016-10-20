import chess
import config
from negamax import MoveSelector

MAX_ITER_MTD = 100
MAX_DEPTH = 4

def main():

	board = chess.Board()
	moveSelector = MoveSelector(MAX_ITER_MTD, MAX_DEPTH, config.MAX_SCORE)

	while True:
		if board.is_game_over():
			break

		move = moveSelector.selectMove(board)[0]
		print move.uci()
		board.push(move)
		print board

		if board.is_game_over():
			break

		rawMove = ""
		while rawMove == "":
			rawMove = raw_input("Enter your move: ")
			try:
				move = chess.Move.from_uci(rawMove)
			except ValueError:
				rawMove = ""
				continue
			if (not move in board.legal_moves):
				rawMove = ""

		board.push(move)
		print board

main()