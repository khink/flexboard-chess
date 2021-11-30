"""Classes for a rectangular chess board with any amount of ranks and files.

Large parts of this were taken from https://github.com/niklasf/python-chess/.
"""
import dataclasses


Color = bool
COLORS = [WHITE, BLACK] = [True, False]
COLOR_NAMES = ["black", "white"]

PieceType = int
PIECE_TYPES = [PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING] = range(1, 7)
PIECE_SYMBOLS = [None, "p", "n", "b", "r", "q", "k"]
PIECE_NAMES = [None, "pawn", "knight", "bishop", "rook", "queen", "king"]


UNICODE_PIECE_SYMBOLS = {  # black and white are opposite to python-chess
    # black pieces
    "r": "♖",
    "n": "♘",
    "b": "♗",
    "q": "♕",
    "k": "♔",
    "p": "♙",
    # white pieces
    "K": "♚",
    "Q": "♛",
    "B": "♝",
    "N": "♞",
    "R": "♜",
    "P": "♟",
}


@dataclasses.dataclass
class Piece:
    """A piece with type and color."""

    piece_type: PieceType
    """The piece type."""

    color: Color
    """The piece color."""

    def symbol(self) -> str:
        """
        Gets the symbol ``P``, ``N``, ``B``, ``R``, ``Q`` or ``K`` for white
        pieces or the lower-case variants for the black pieces.
        """
        symbol = PIECE_SYMBOLS[self.piece_type]
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


class Square:
    def __init__(self, is_last_of_rank=False, piece=None):
        self.is_last_of_rank = is_last_of_rank
        if piece:
            self.piece = Piece.from_symbol(piece)
        else:
            self.piece = None


class Board:
    """A rectangular chess board.

    `squares` is a list of Square objects. The list starts at the top rank on
    the left, just like in FEN notation.
    A rank is terminated if square.is_last_of_rank is True.
    """

    def __init__(self, board_fen=None, nr_of_files=8, nr_of_ranks=8):
        """Create a new board."""
        self.squares = []
        if board_fen:
            self._init_from_fen(board_fen)
        else:
            self._init_from_nr_of_ranks_and_files(nr_of_ranks, nr_of_files)

    def _init_from_fen(self, board_fen):
        """Populate board with pieces from Forsyth-Edwards Notation."""
        for fen_rank in board_fen.split("/"):
            rank_squares = []
            for char in fen_rank:
                if char.isdigit():
                    # Add empty squares
                    for _idx in range(int(char)):
                        rank_squares.append(Square())
                else:
                    rank_squares.append(Square(piece=char))
            rank_squares[-1].is_last_of_rank = True
            self.squares.extend(rank_squares)

    def _init_from_nr_of_ranks_and_files(self, nr_of_files, nr_of_ranks):
        """Create empty board with given dimensions."""
        for file_idx in range(nr_of_files):
            for rank_idx in range(nr_of_ranks):
                is_last_of_rank = rank_idx == nr_of_ranks - 1
                square = Square(is_last_of_rank=is_last_of_rank)
                self.squares.append(square)

    def __str__(self) -> str:
        """Represent board as string.

        At the very least, this is handy for testing Board.__init__().
        """
        builder = []

        for square in self.squares:
            if square.piece:
                builder.append(square.piece.unicode_symbol())
            else:
                builder.append(".")
            if square.is_last_of_rank:
                builder.append("\n")
            else:
                builder.append(" ")

        return "".join(builder)
