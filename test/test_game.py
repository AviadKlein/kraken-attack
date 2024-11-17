from unittest import TestCase

from kraken_attack.game import *
from collections import Counter

class TestPirate(TestCase):

    def test_str(self):
        self.assertEqual(str(Elena()), 'Elena')
        self.assertEqual(str(Billy()), 'Billy')
        self.assertEqual(str(Samuel()), 'Samuel')
        self.assertEqual(str(Astrid()), 'Astrid')

    def test_hash(self):
        d = {Elena(): 1, Billy(): 2}
        self.assertEqual(d[Elena()], 1)
        self.assertEqual(d[Billy()], 2)

        d = {Elena(): 1, Elena(): 2}
        self.assertEqual(len(d), 1)

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

    def test_draw_lane(self):
        board = GameBoard({Elena(): 0})
        self.assertEqual('| | |𝛿| |', board.draw_lane(0))
        self.assertEqual('| |𝛿| | |', board.draw_lane(1))
        self.assertEqual('| |𝛿| | |', board.draw_lane(2))
        self.assertEqual('|𝛿| | | |', board.draw_lane(3))

        self.assertEqual('| |𝛿| | |', board.draw_lane(4))
        self.assertEqual('| | |𝛿| |', board.draw_lane(5))
        self.assertEqual('| | |𝛿| |', board.draw_lane(6))
        self.assertEqual('| | | |𝛿|', board.draw_lane(7))

    def test_draw_ship_lane(self):
        board = GameBoard({Elena(): 0})
        self.assertEqual('🛡️|__', board.draw_ship_lane(0))
        self.assertEqual('🛡️|__', board.draw_ship_lane(1))
        self.assertEqual('🛡️|__', board.draw_ship_lane(2))
        self.assertEqual('🛡️|__', board.draw_ship_lane(3))
        self.assertEqual('__|️🛡', board.draw_ship_lane(4))
        self.assertEqual('__|️🛡', board.draw_ship_lane(5))
        self.assertEqual('__|️🛡', board.draw_ship_lane(6))
        self.assertEqual('__|️🛡', board.draw_ship_lane(7))

    def test_draw(self):
        board = GameBoard({Elena(): 0})
        result = board.draw()
        self.assertEqual("""      KRAKEN ATTACK

|🐙| |🟥| |🟦| |🟥| |🟦|

| | |𝛿| |🛡️|____|️🛡| |𝛿| | |
| |𝛿| | |🛡️|____|️🛡| | |𝛿| |
| |𝛿| | |🛡️|____|️🛡| | |𝛿| |
|𝛿| | | |🛡️|____|️🛡| | | |𝛿|

Ship damage: 0
Kraken damage: 0
Pirates: Elena""", result)
        
    def test_roll_dice(self):
        board = GameBoard({Elena(): 0})
        blue = []
        red = []
        for _ in range(10000):
            r = board.roll_dice()
            [blue.append(t[1]) for t in r if t[0] == 'blue']
            [red.append(t[1]) for t in r if t[0] == 'red']
        blue = dict(Counter(blue))
        red = dict(Counter(red))
        self.assertDictEqual(blue, {0: 1652, 5: 1751, 1: 1630, 3: 1680, 4: 1613, 2: 1674})
        self.assertDictEqual(red, {5: 1725, 0: 1632, 2: 1625, 1: 1673, 4: 1620, 3: 1725})

        board = GameBoard({Elena(): 0}, seed=6767)
        blue = []
        red = []
        for _ in range(10000):
            r = board.roll_dice()
            [blue.append(t[1]) for t in r if t[0] == 'blue']
            [red.append(t[1]) for t in r if t[0] == 'red']
        blue = dict(Counter(blue))
        red = dict(Counter(red))
        self.assertDictEqual(blue, {2: 1581, 1: 1694, 3: 1737, 4: 1691, 5: 1618, 0: 1679})
        self.assertDictEqual(red, {5: 1645, 4: 1617, 2: 1686, 0: 1690, 1: 1662, 3: 1700})

    def test_determine_kraken_moves(self):
        board = GameBoard({Elena(): 0}, seed=22)
        roll_outcome = [('red', 0), ('blue', 0)]
        result = board.determine_kraken_moves(roll_outcome)
        self.assertListEqual(result , [4,0])

        roll_outcome = [('red', 1), ('blue', 0)]
        result = board.determine_kraken_moves(roll_outcome)
        self.assertListEqual(result , [5,0])

        roll_outcome = [('red', 1), ('blue', 3), ('blue', 3)]
        result = board.determine_kraken_moves(roll_outcome)
        self.assertListEqual(result , [5,3,3])

        roll_outcome = [('red', 5), ('blue', 5)]
        result = board.determine_kraken_moves(roll_outcome)
        self.assertListEqual(result , [])

        roll_outcome = [('red', 4), ('blue', 4)]
        result = board.determine_kraken_moves(roll_outcome)
        self.assertListEqual(result , [4,5,6,7,0,1,2,3])

        roll_outcome = [('red', 4), ('blue', 4), ('blue', 4)]
        result = board.determine_kraken_moves(roll_outcome)
        self.assertListEqual(result , [4,5,6,7,0,1,2,3,0,1,2,3])

    def test_determine_board_after_kraken_moves(self):
        board = GameBoard({Elena(): 0}, seed=22)
        km = []
        board.determine_board_after_kraken_move(km)
        print(board.draw())
        self.assertEqual(board.arm_locations[0], 2)

        km = [0]
        board.determine_board_after_kraken_move(km)
        print(board.draw())
        self.assertEqual(board.arm_locations[0], 3)
        
        km = [0]
        board.determine_board_after_kraken_move(km)
        print(board.draw())
        self.assertEqual(board.arm_locations[0], 3)
        self.assertFalse(board.shield_status[0])

        km = [6]
        board.determine_board_after_kraken_move(km)
        print(board.draw())
        self.assertEqual(board.arm_locations[0], 3)
        self.assertEqual(board.arm_locations[6], 2)
        self.assertFalse(board.shield_status[0])

        km = [6, 6]
        board.determine_board_after_kraken_move(km)
        print(board.draw())
        self.assertEqual(board.arm_locations[0], 3)
        self.assertEqual(board.arm_locations[6], 3)
        self.assertFalse(board.shield_status[0])
        self.assertFalse(board.shield_status[6])

        km = [6, 6]
        board.determine_board_after_kraken_move(km)
        print(board.draw())
        self.assertEqual(board.arm_locations[0], 3)
        self.assertEqual(board.arm_locations[6], 3)
        self.assertFalse(board.shield_status[0])
        self.assertFalse(board.shield_status[6])
        self.assertEqual(len(board.ship_hole_positions), 2)

    def test_move_pirate(self):
        board = GameBoard({Elena(): 0, Astrid(): 0, })
        with self.assertRaises(IllegalMove) as cm:
            board.move_pirate(Billy(), 3)
        self.assertEqual(str(cm.exception), 'Billy is not on the board')

        with self.assertRaises(IllegalMove) as cm:
            board.move_pirate(Astrid(), 3)
        self.assertEqual(str(cm.exception), 'can only go to quadrants (1, 2) from quadrant 0')

        board.move_pirate(Astrid(), 1)
        self.assertEqual(board.pirate_quadrants[Astrid()], 1)
        board.move_pirate(Astrid(), 3)
        self.assertEqual(board.pirate_quadrants[Astrid()], 3)
        board.move_pirate(Astrid(), 2)
        self.assertEqual(board.pirate_quadrants[Astrid()], 2)
        board.move_pirate(Astrid(), 0)
        self.assertEqual(board.pirate_quadrants[Astrid()], 0)

    def test_pirate_attack(self):
        board = GameBoard({Astrid(): 2})
        self.assertEqual(board.arm_locations[4], 2)
        self.assertEqual(board.arm_locations[5], 1)
        
        board.perform_pirate_attack(Astrid(), attack='pistol', lane=4)
        board.perform_pirate_attack(Astrid(), attack='cannon', lane=5)
        
        self.assertEqual(board.arm_locations[4], 1)
        self.assertEqual(board.arm_locations[5], 0)

        # Illegal move
        with self.assertRaises(IllegalMove) as cm:
            board.perform_pirate_attack(Astrid(), attack='pistol', lane=0)
        self.assertEqual(str(cm.exception), 'Astrid cannot attack lane 0 from quadrant 2')

    def test_pirate_attack_on_kraken(self):
        board = GameBoard({Astrid(): 2})

        self.assertFalse(board.is_kraken_on_board)
        [board.annoy_kraken(4) for _ in range(9)]
        self.assertTrue(board.is_kraken_on_board)
        self.assertEqual(board.kraken_lane, 4)
        self.assertEqual(board.kraken_damage, 0)

        board.perform_pirate_attack(Astrid(), 'pistol', 4)
        self.assertEqual(board.kraken_damage, 1)
        self.assertEqual(board.arm_locations[4], 1)

        board.perform_pirate_attack(Astrid(), 'cannon', 4)
        self.assertEqual(board.kraken_damage, 2)
        self.assertEqual(board.arm_locations[4], 0)

        # null attack
        board.perform_pirate_attack(Astrid(), 'pistol', 4)
        self.assertEqual(board.kraken_damage, 2)
        self.assertEqual(board.arm_locations[4], 0)

    def test_perform_repair(self):
        pass
        
        

        