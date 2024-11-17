from __future__ import annotations

from typing import Dict, Optional, List, Tuple
from abc import ABC
from random import Random

class Pirate(ABC):
    
    def __str__(self):
        return self.__class__.__name__
    
    def __repr__(self):
        return f"<Pirate: {self.__str__()}>"
    
    def __hash__(self):
        return self.__str__().__hash__()
    
    def __eq__(self, value):
        if isinstance(value, Pirate):
            return self.__repr__() == value.__repr__()
        else:
            return False


class Samuel(Pirate):
    pass

class Astrid(Pirate):
    pass

class Billy(Pirate):
    pass

class Elena(Pirate):
    pass

class IllegalMove(Exception):
    pass

class GameBoard:
    """
    The Angry Kraken's Game Board

    To initialize, one needs to supply at least 1 Pirate and quadrant location
    quadrants are numbered 0,1,2,3
    quadrants 0,1 are on the left side
    quadrants 2,3 are on the right side
    
    The ship has 8 shields in locations 0,1,...7 such that modulo location falls in a quadrant
    lanes 0,1,2,3 are colored blue and are on the left side
    lanes 4,5,6,7 are colored red and are on the right side
    the karken starts at location 0 and ends at 9 which means he is on the board
    the arms are positioned in lanes, the lanes have the same indices as the shields

    ship holes are a tuple of ints and can be repeated, the ints need to be like the quadrants
    """

    def __init__(self, pirate_quadrants: Dict[Pirate, int], seed: int=42):
        assert len(pirate_quadrants) > 0, f"there needs to be at least 1 pirate"
        for p, q in pirate_quadrants.items():
            assert 0 <= q <= 3, f"the pirate {p} is in an illegal quadrant {q}"
        self.pirate_quadrants: Dict[Pirate, int] = pirate_quadrants
        self.shield_status: Dict[int, bool] = {_: True for _ in range(8)}
        self.arm_locations: Dict[int, int] = {
            0: 2,
            1: 1,
            2: 1,
            3: 0,
            4: 2,
            5: 1,
            6: 1,
            7: 0
            }
        self.kraken_location: int = 0
        self.kraken_lane: Optional[int] = None
        self.kraken_damage: int = 0
        self.ship_hole_positions: Tuple[int,...] = ()
        self.rng = Random(seed)
    
    def __eq__(self, value):
        if isinstance(value, GameBoard):
            result = True
            result &= self.pirate_quadrants == value.pirate_quadrants
            result &= self.shield_status == value.shield_status
            result &= self.arm_locations == value.arm_locations
            result &= self.kraken_location == value.kraken_location
            result &= self.kraken_lane == value.kraken_lane
            result &= self.kraken_damage == value.kraken_damage
            result &= self.ship_hole_positions == self.ship_hole_positions
            result &= self.rng == value.rng
            return result
        else:
            return False
        
    def __ne__(self, value):
        return not self.__eq__(value)

    def draw_lane(self, lane: int) -> str:
        assert 0 <= lane <= 7
        result = "| | | | |"
        arm_index = self.arm_locations[lane]*2 + 1
        if self.kraken_lane is not None:
            if self.kraken_lane == lane:
                result = result[:arm_index] + '🐙' + result[arm_index+1:]
        else:
            result = result[:arm_index] + '𝛿' + result[arm_index+1:]
        if lane >= 4:
            result = result[::-1]
        return result
    
    def draw_ship_lane(self, lane: int) -> str:
        assert 0 <= lane <= 7
        result = "|__"
        if self.shield_status[lane]:
            result = '🛡️' + result
        else:
            result = '.' + result
        if lane >= 4:
            result = result[::-1]
        return result
    
    def draw_kraken_location(self) -> str:
        result = "| | |🟥| |🟦| |🟥| |🟦|"
        if self.kraken_location <= 8:
            result = result[:self.kraken_location*2 + 1] + '🐙' + result[self.kraken_location*2 + 2:]
        for i in range(self.kraken_location):
            result = result[:i*2 + 1] + ' ' + result[i*2 + 2:]
        return result
    
    def draw(self) -> str:
        result = '      KRAKEN ATTACK\n\n'
        result += self.draw_kraken_location()
        result += '\n\n'
        for left, right in [(0,4),(1,5),(2,6),(3,7)]:
            result += self.draw_lane(left)
            result += self.draw_ship_lane(left)
            result += self.draw_ship_lane(right)
            result += self.draw_lane(right)
            result += '\n'
        result += '\n'
        result += f'Ship damage: {len(self.ship_hole_positions)}\n'
        result += f'Kraken damage: {self.kraken_damage}\n'
        result += f'Pirates: {', '.join([str(_) for _ in self.pirates])}'
        return result

    @property
    def pirates(self) -> List[Pirate]:
        return list(self.pirate_quadrants.keys())

    @property
    def dice_counts(self):
        """Dice counts grow according to the location of the Kraken"""
        if self.kraken_location < 2:
            return {'red': 1, 'blue': 1}
        elif self.kraken_location < 4:
            return {'red': 2, 'blue': 1}
        elif self.kraken_location < 6:
            return {'red': 2, 'blue': 2}
        elif self.kraken_location < 8:
            return {'red': 3, 'blue': 2}
        elif self.kraken_location < 10:
            return {'red': 3, 'blue': 3}

    def game_outcome(self) -> Optional[str]:
        """The game is concluded when either
        The kraken recieves 3 points of damage
        Or
        When there are 4 holes in the ship
        Otherwise, the game outcome is None
        """
        outcome = None
        if len(self.ship_hole_positions) == 4:
            outcome = 'Kraken drowns ship'
        elif self.kraken_damage == 3:
            outcome = 'Kraken retreats'
        else:
            pass
        return outcome

    def roll_dice(self) -> List[Tuple[str, int]]:
        """returns a list of (dice color, dice outcome)
        dice outcomes are:
        0 to 3 - depict a lane number
        4 - depicts the "eye" facet, meaning that the kraken advances all arms for that color
        5 - depicts a blank facet, meaning no movement by the Kraken
        """
        roll_outcome = []
        for color, num in self.dice_counts.items():
            for _ in range(num):
                roll_outcome.append((color, self.rng.randint(0,5)))
        return roll_outcome

    def determine_kraken_moves(self, roll_outcome: List[Tuple[str, int]]) -> List[int]:
        """based on the outcome of a roll of the dice this method 
        returns a list of ints, each int points to a lane that 
        will perform an advance or an attack by the Kraken"""
        
        assert set(('red', 'blue')) == {t[0] for t in roll_outcome}
        assert all(0 <= t[1] <= 5 for t in roll_outcome)
        moves = []
        for color, dice_roll in roll_outcome:
            if dice_roll == 5: # blank facet
                pass 
            elif 0 <= dice_roll <= 3: # single lane
                move = dice_roll + (4 if color == 'red' else 0)
                moves.append(move)
            else: # the eye!
                if color == 'blue':
                    moves = [*moves, *[0,1,2,3]]
                else:
                    moves = [*moves, *[4,5,6,7]]
        return moves
    
    def determine_board_after_kraken_move(self, kraken_moves: List[int]):
        for lane in kraken_moves:
            if self.arm_locations[lane] < 3:
                self.arm_locations[lane] += 1
            elif self.arm_locations[lane] == 3:
                if self.shield_status[lane]: # break a shield
                    self.shield_status[lane] = False 
                else: # add a hole to the ship
                    self.ship_hole_positions = (*self.ship_hole_positions, lane // 2)
            else:
                raise Exception(f"illegal lane, got {lane}")

    @property
    def legal_pirate_moves(self):
        return {
            0: (1,2),
            1: (0,3),
            2: (0,3),
            3: (1,2)
        }

    def move_pirate(self, pirate: Pirate, to: int):
        """checks for the legality of the move and updates the board"""
        pirate_quadrant = self.pirate_quadrants.get(pirate)
        if pirate_quadrant is None:
            raise IllegalMove(f'{pirate} is not on the board')
        legal_moves = self.legal_pirate_moves[pirate_quadrant]
        if to in (legal_moves):
            self.pirate_quadrants[pirate] = to
        else:
            raise IllegalMove(f'can only go to quadrants {legal_moves} from quadrant {pirate_quadrant}')
        
    def perform_pirate_attack(self, pirate: Pirate, attack: str, lane: int):
        hit = False
        pirate_quadrant = self.pirate_quadrants.get(pirate)
        if pirate_quadrant is None:
            raise IllegalMove(f'{pirate} is not on the board')
        if lane // 2 != pirate_quadrant:
            raise IllegalMove(f'{pirate} cannot attack lane {lane} from quadrant {pirate_quadrant}')
        else:
            match attack, self.arm_locations[lane]:
                case 'sword', 3:
                    hit = True
                case 'pistol', 2:
                    hit = True
                case 'cannon', 1:
                    hit = True
                case _:
                    pass
        if hit:
            self.arm_locations[lane] -= 1
            if self.kraken_lane is not None:
                if self.kraken_lane == lane:
                    self.kraken_damage += 1
        
    
    def perform_repair(self, pirate: Pirate, lane: int):
        pirate_quadrant = self.pirate_quadrants.get(pirate)
        if pirate_quadrant is None:
            raise IllegalMove(f'{pirate} is not on the board')
        if lane // 2 != pirate_quadrant:
            raise IllegalMove(f'{pirate} cannot repair lane {lane} from quadrant {pirate_quadrant}')
        else:
            if self.shield_status[lane] == False:
                self.shield_status[lane] = True
            else:
                pass

    def annoy_kraken(self, lane: Optional[int]=None):
        if self.kraken_location > 8:
            pass # Kraken is already on the board
        elif self.kraken_location == 8:
            if lane is None:
                raise IllegalMove('must specify to which lane the Kraken will go')
            else:
                self.kraken_location = 9
                self.kraken_lane = lane
        else:
            self.kraken_location += 1

    @property
    def is_kraken_on_board(self) -> bool:
        return (self.kraken_location == 9) and (self.kraken_lane is not None)
            