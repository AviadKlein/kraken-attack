from unittest import TestCase

from kraken_attack.game import *

class TestGameBoard(TestCase):

    def test_annoy_kraken(self):
        board = GameBoard({Elena(): 0})
        result = board.draw_kraken_location()
        self.assertEqual(result, '|🐙| |🟥| |🟦| |🟥| |🟦|')
        self.assertDictEqual(board.dice_counts, {'red': 1, 'blue': 1})

        board.annoy_kraken()
        result = board.draw_kraken_location()
        self.assertEqual(result, '| |🐙|🟥| |🟦| |🟥| |🟦|')
        self.assertDictEqual(board.dice_counts, {'red': 1, 'blue': 1})

        board.annoy_kraken()
        result = board.draw_kraken_location()
        self.assertEqual(result, '| | |🐙| |🟦| |🟥| |🟦|')
        self.assertDictEqual(board.dice_counts, {'red': 2, 'blue': 1})

        board.annoy_kraken()
        result = board.draw_kraken_location()
        self.assertEqual(result, '| | | |🐙|🟦| |🟥| |🟦|')
        self.assertDictEqual(board.dice_counts, {'red': 2, 'blue': 1})

        board.annoy_kraken()
        result = board.draw_kraken_location()
        self.assertEqual(result, '| | | | |🐙| |🟥| |🟦|')
        self.assertDictEqual(board.dice_counts, {'red': 2, 'blue': 2})

        board.annoy_kraken()
        result = board.draw_kraken_location()
        self.assertEqual(result, '| | | | | |🐙|🟥| |🟦|')
        self.assertDictEqual(board.dice_counts, {'red': 2, 'blue': 2})

        board.annoy_kraken()
        result = board.draw_kraken_location()
        self.assertEqual(result, '| | | | | | |🐙| |🟦|')
        self.assertDictEqual(board.dice_counts, {'red': 3, 'blue': 2})

        board.annoy_kraken()
        result = board.draw_kraken_location()
        self.assertEqual(result, '| | | | | | | |🐙|🟦|')
        self.assertDictEqual(board.dice_counts, {'red': 3, 'blue': 2})

        board.annoy_kraken()
        result = board.draw_kraken_location()
        self.assertEqual(result, '| | | | | | | | |🐙|')
        self.assertDictEqual(board.dice_counts, {'red': 3, 'blue': 3})

        with self.assertRaises(IllegalMove) as cm:
            board.annoy_kraken()
        self.assertEqual(board.kraken_location, 8)
        self.assertEqual(str(cm.exception), 'must specify to which lane the Kraken will go')

        board.annoy_kraken(0)
        self.assertEqual(board.kraken_location, 9)
        self.assertEqual(board.kraken_lane, 0)
        result = board.draw_kraken_location()
        self.assertEqual(result, '| | | | | | | | | |')

    def test_1(self):
        board = GameBoard({Elena(): 0})
        print(board.draw())