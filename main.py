import chess
import config
from negamax import MoveSelector
from pp_board import pp_board

MAX_ITER_MTD = 100
MAX_DEPTH = 4

def handle_ai_move(board, move_selector):
	move = move_selector.selectMove(board)[0]
	print("AI does " + move.uci())
	board.push(move)
	print(pp_board(board))

def handle_human_move(board):
	while True:
		raw_move = input("Enter your move: ")
		try:
			move = chess.Move.from_uci(raw_move)
			if move in board.legal_moves:
				break
			else:
				print("Invalid move, please enter a valid move!")
		except ValueError:
			print("Invalid UCI, please enter a valid UCI move!")

	board.push(move)
	print(pp_board(board))


def main():
	board = chess.Board()
	move_selector = MoveSelector(MAX_ITER_MTD, MAX_DEPTH, config.MAX_SCORE)

	color_choice = input("Do you want to play as black or white? [W/B]: ")
	while color_choice is not "W" and color_choice is not "B":
		color_choice = input("Invalid choice, please enter W for white or B for black: ")

	print(pp_board(board))

	if color_choice == "W":
		while True:
			if board.is_game_over():
				break

			handle_human_move(board)

			if board.is_game_over():
				break

			handle_ai_move(board, move_selector)
	else:
		while True:
			if board.is_game_over():
				break

			handle_ai_move(board, move_selector)

			if board.is_game_over():
				break

			handle_human_move(board)

	print(board.result())

if __name__ == "__main__":
	main()
