from main import *


def main():
    board = Board(5, 5)

    testTile1 = Board.Tile(3, 2, addToBoard=board)
    testTile2 = Board.Tile(2, 2, addToBoard=board)
    testTile3 = Board.Tile(4, 1, addToBoard=board)
    print(board)
    board.sort()
    print(board)


if __name__ == "__main__":
    main()
