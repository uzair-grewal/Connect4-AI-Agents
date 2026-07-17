import unittest

from engine import ConnectFour


class ConnectFourEngineTests(unittest.TestCase):
    def test_horizontal_win(self) -> None:
        game = ConnectFour()
        for col in [0, 6, 1, 5, 2, 4, 3]:
            game.apply_move(col)

        self.assertEqual(game.winner(), 1)
        self.assertTrue(game.is_terminal())

    def test_vertical_win(self) -> None:
        game = ConnectFour()
        for col in [0, 1, 0, 1, 0, 1, 0]:
            game.apply_move(col)

        self.assertEqual(game.winner(), 1)
        self.assertTrue(game.is_terminal())

    def test_diagonal_wins(self) -> None:
        for direction, board in [
            ("ascending", [
                [1, 0, 0, 0, 0, 0, 0],
                [2, 1, 0, 0, 0, 0, 0],
                [2, 2, 1, 0, 0, 0, 0],
                [2, 2, 2, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
            ]),
            ("descending", [
                [0, 0, 0, 1, 0, 0, 0],
                [0, 0, 1, 2, 0, 0, 0],
                [0, 1, 2, 2, 0, 0, 0],
                [1, 2, 2, 2, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
            ]),
        ]:
            with self.subTest(direction=direction):
                game = ConnectFour()
                game.board = [row[:] for row in board]
                self.assertEqual(game.winner(), 1)

    def test_draw_with_no_winner(self) -> None:
        game = ConnectFour()
        board = [
            [1, 1, 2, 2, 1, 1, 2],
            [2, 2, 1, 1, 2, 2, 1],
            [1, 1, 2, 2, 1, 1, 2],
            [2, 2, 1, 1, 2, 2, 1],
            [1, 1, 2, 2, 1, 1, 2],
            [2, 2, 1, 1, 2, 2, 1],
        ]
        game.board = [row[:] for row in board]

        self.assertIsNone(game.winner())
        self.assertTrue(game.is_draw())
        self.assertTrue(game.is_terminal())

    def test_illegal_move_on_full_column_raises(self) -> None:
        game = ConnectFour()
        for _ in range(6):
            game.apply_move(0)

        with self.assertRaises(ValueError):
            game.apply_move(0)


if __name__ == "__main__":
    unittest.main()
