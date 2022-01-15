"""Classes for a rectangular chess board with any amount of ranks and files.

Large parts of this were taken from https://github.com/niklasf/python-chess/.
"""
import dataclasses
import typing


Color = bool

COLORS = [WHITE, BLACK] = [True, False]
COLOR_NAMES = ["black", "white"]

PieceType = int
PIECE_TYPES = [PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING] = range(1, 7)
PIECE_SYMBOLS = [None, "p", "n", "b", "r", "q", "k"]
PIECE_NAMES = [None, "pawn", "knight", "bishop", "rook", "queen", "king"]

UNICODE_PIECE_SYMBOLS = {
    # displayed as black on terminal
    "r": "♖",
    "n": "♘",
    "b": "♗",
    "q": "♕",
    "k": "♔",
    "p": "♙",
    # displayed as white on terminal
    "K": "♚",
    "Q": "♛",
    "B": "♝",
    "N": "♞",
    "R": "♜",
    "P": "♟",
}

FEN_RANK_END = "/"


def piece_symbol(piece_type: PieceType) -> str:
    return typing.cast(str, PIECE_SYMBOLS[piece_type])


@dataclasses.dataclass
class Piece:
    """A piece with type and color."""

    piece_type: PieceType
    """The piece type."""

    color: Color
    """The piece color."""

    def __int__(self) -> int:
        color_int = 0 if self.color else 8
        return self.piece_type + color_int

    def symbol(self) -> str:
        """
        Gets the symbol ``P``, ``N``, ``B``, ``R``, ``Q`` or ``K`` for white
        pieces or the lower-case variants for the black pieces.
        """
        symbol = piece_symbol(self.piece_type)
        return symbol.upper() if self.color else symbol

    def unicode_symbol(self, *, invert_color: bool = False) -> str:
        """
        Gets the Unicode character for the piece.
        """
        symbol = self.symbol().swapcase() if invert_color else self.symbol()
        return UNICODE_PIECE_SYMBOLS[symbol]

    @classmethod
    def from_symbol(cls, symbol: str):
        """
        Creates a :class:`~chess.Piece` instance from a piece symbol.

        :raises: :exc:`ValueError` if the symbol is invalid.
        """
        return cls(PIECE_SYMBOLS.index(symbol.lower()), symbol.isupper())

    @classmethod
    def from_int(cls, int_code: int):
        """
        Creates a :class:`~chess.Piece` instance from an integer.

        :raises: :exc:`ValueError` if the integer is invalid.
        """
        if int_code < 0:
            raise ValueError(f"A piece_type integer should be positive")

        if int_code > 16:
            raise ValueError(f"A piece_type integer cannot be larger than 16")

        piece_type = int_code % 8

        if piece_type not in PIECE_TYPES:
            raise ValueError(f"'{piece_type}' is an unknown piece_type")

        if int_code < 8:
            color = WHITE
        else:
            color = BLACK

        return Piece(piece_type=piece_type, color=color)


class Board:
    """A rectangular chess board.

    The `squares` list starts at the top rank on the left, as in FEN notation.
    """

    turn: Color
    nr_of_files: int
    nr_of_ranks: int
    squares: typing.List[int]

    def __init__(
        self, board_fen=None, nr_of_files: int = 8, nr_of_ranks: int = 8, turn=WHITE
    ):
        """Create a new board."""
        self.squares = []
        if board_fen:
            self._set_board_fen(board_fen)
        else:
            self._init_from_nr_of_ranks_and_files(nr_of_ranks, nr_of_files)
        self.turn = turn

    def _set_board_fen(self, fen: str) -> None:
        square_index = 0
        nr_of_files_in_rank = 0
        nr_of_ranks = 1
        for char in fen:
            if char == FEN_RANK_END:
                if hasattr(self, "nr_of_files"):
                    # TODO move fen validation to separate method
                    assert (
                        self.nr_of_files == nr_of_files_in_rank
                    ), "This rank has a different number of squares than the other rank(s)"
                else:
                    self.nr_of_files = nr_of_files_in_rank
                nr_of_ranks += 1
                nr_of_files_in_rank = 0
            else:
                if char.isdigit():
                    nr_of_empty_squares = int(char)
                    for _idx in range(nr_of_empty_squares):
                        self.squares.append(0)
                        nr_of_files_in_rank += 1
                else:
                    piece = Piece.from_symbol(char)
                    self.squares.append(int(piece))
                    square_index += 1
                    nr_of_files_in_rank += 1
        self.nr_of_ranks = nr_of_ranks

    def _init_from_nr_of_ranks_and_files(
        self, nr_of_files: int, nr_of_ranks: int
    ) -> None:
        """Create empty board with given dimensions."""
        self.nr_of_ranks = nr_of_ranks
        self.nr_of_files = nr_of_files
        self.squares = [0] * nr_of_files * nr_of_ranks

    def __str__(self) -> str:
        builder = []

        for rank_idx in range(self.nr_of_ranks):
            for file_idx in range(self.nr_of_files):
                square_idx = rank_idx * self.nr_of_ranks + file_idx
                square_value = self.squares[square_idx]
                if square_value == 0:
                    builder.append(".")
                else:
                    piece = Piece.from_int(square_value)
                    builder.append(piece.unicode_symbol())
                builder.append(" ")
            builder.append("\n")

        return "".join(builder)
