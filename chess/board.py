class Square:
    def __init__(self, is_last_of_rank=False, piece="."):
        self.is_last_of_rank = is_last_of_rank
        self.piece = piece


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
            builder.append(square.piece)
            if square.is_last_of_rank:
                builder.append("\n")
            else:
                builder.append(" ")

        return "".join(builder)
