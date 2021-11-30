from ..board import Board


def test_board_init_nr_of_files_and_ranks():
    board = Board(nr_of_files=5, nr_of_ranks=5)
    assert str(board) == ". . . . .\n. . . . .\n. . . . .\n. . . . .\n. . . . .\n"


def test_board_init_from_fen():
    board = Board(board_fen="rnbqk/ppppp/5/PPPPP/RNBQK")
    assert str(board) == "♖ ♘ ♗ ♕ ♔\n♙ ♙ ♙ ♙ ♙\n. . . . .\n♟ ♟ ♟ ♟ ♟\n♜ ♞ ♝ ♛ ♚\n"
