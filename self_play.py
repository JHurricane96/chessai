import chess
import config
from negamax import MoveSelector
from pp_board import pp_board
import os

MAX_ITER_MTD = 100
WHITE_MAX_DEPTH = 2
BLACK_MAX_DEPTH = 3

console_width = os.get_terminal_size().columns

def clear_screen():
	os.system("cls" if os.name == "nt" else "clear")

def print_move(board, move_uci):
	clear_screen()
	color = "Black" if board.turn else "White"
	other_color = "White" if board.turn else "Black"
	print("\n")
	print("{} does {}".format(color, move_uci).center(console_width))
	print("{} to move".format(other_color).center(console_width))
	str_board = pp_board(board)
	str_board = "\n".join([row.center(console_width) for row in str_board.split("\n")])
	print(str_board)

def make_move(board, move_selector):
	move = move_selector.selectMove(board)[0]
	board.push(move)
	print_move(board, move.uci())

def main():
	board = chess.Board()
	white_move_selector = MoveSelector(MAX_ITER_MTD, WHITE_MAX_DEPTH, config.MAX_SCORE)
	black_move_selector = MoveSelector(MAX_ITER_MTD, BLACK_MAX_DEPTH, config.MAX_SCORE)
	clear_screen()

	while True:
		if board.is_game_over():
			break

		make_move(board, white_move_selector)

		if board.is_game_over():
			break

		make_move(board, black_move_selector)

	print(board.result().center(console_width))

if __name__ == "__main__":
	main()
