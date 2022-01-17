import pytest

from ..board import Board, Piece, WHITE, BLACK


def test_board_init_empty():
    board = Board()
    assert board.nr_of_files == 8
    assert board.nr_of_ranks == 8
    assert board.turn == WHITE


def test_board_init_nr_of_files_and_ranks():
    board = Board(nr_of_files=5, nr_of_ranks=5)
    assert board.nr_of_files == 5
    assert board.nr_of_ranks == 5
    assert board.squares == [0] * 25
    assert str(board) == ". . . . . \n. . . . . \n. . . . . \n. . . . . \n. . . . . \n"


def test_board_init_from_fen():
    board = Board(board_fen="rnbqk/ppppp/5/PPPPP/RNBQK")
    assert board.nr_of_files == 5
    assert board.nr_of_ranks == 5
    assert len(board.squares) == 25
    assert str(board) == "♖ ♘ ♗ ♕ ♔ \n♙ ♙ ♙ ♙ ♙ \n. . . . . \n♟ ♟ ♟ ♟ ♟ \n♜ ♞ ♝ ♛ ♚ \n"


def test_board_init_with_turn():
    board = Board(turn=BLACK)
    assert board.turn == BLACK
    board = Board(turn=WHITE)
    assert board.turn == WHITE


@pytest.mark.parametrize("int_code", [-1, 0, 7, 8, 15, 16, 17, 18])
def test_piece_from_int_value_error(int_code):
    with pytest.raises(ValueError):
        Piece.from_int(int_code)
