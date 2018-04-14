def pp_board(board):
	str_board = str(board)
	rows = str_board.split("\n")
	nrows = len(rows)
	rows = [rows[i] + "   " + str(nrows - i - 1) for i in range(nrows)]
	rows.append("")
	rows.append("a b c d e f g h     ")
	str_board = "\n".join(rows)
	return str_board
