from typing import List
import unittest

OCCUPIED = '#'
FLOOR = '.'
EMPTY = 'L'
OFFSETS = {'N': (0, -1), 'NE': (1, -1), 'E': (1, 0), 'SE': (1, 1),
           'S': (0, 1), 'SW': (-1, 1), 'W': (-1, 0), 'NW': (-1, -1)}


class GameOfSeats:
    def __init__(self, inputs):
        if type(inputs) == str:
            self.seating = [line.strip() for line in open(inputs)]
        elif type(inputs) == list:
            self.seating = inputs

    def __eq__(self, other) -> bool:
        return self.seating == other.seating

    def __ne__(self, other) -> bool:
        return not (self == other)

    def width(self) -> int:
        return len(self.seating[0])

    def height(self) -> int:
        return len(self.seating)

    def seat(self, p: (int, int)) -> str:
        if self.in_bounds(p):
            return self.seating[p[1]][p[0]]
        else:
            return FLOOR

    def within_outer_ring(self, p: (int,int)) -> bool:
        return self.width() >= p[0] >= -1 and self.height() >= p[1] >= -1

    def in_bounds(self, p: (int, int)) -> bool:
        return self.width() > p[0] >= 0 and self.height() > p[1] >= 0

    def num_adj_occupied(self, p: (int, int)) -> int:
        return len([d for d in OFFSETS if self.seat(self.projection(d, p)) == OCCUPIED])

    def create_next(self) -> 'GameOfSeats':
        return self.create_from([''.join([self.iterated_seat_at((col, row))
                                          for col in range(len(self.seating[row]))])
                                 for row in range(len(self.seating))])

    def iterated_seat_at(self, p: (int, int)) -> str:
        seat = self.seat(p)
        adj = self.num_adj_occupied(p)
        if seat == EMPTY and adj == 0:
            return OCCUPIED
        elif seat == OCCUPIED and adj >= self.too_many_adj:
            return EMPTY
        else:
            return seat

    def num_occupied(self) -> int:
        return sum(row.count(OCCUPIED) for row in self.seating)


def num_occupied_at_stable(start: GameOfSeats) -> int:
    prev = start
    count = 1
    current = start.create_next()
    while prev != current:
        prev = current
        current = current.create_next()
        count += 1
    return current.num_occupied()


class Puzzle1(GameOfSeats):
    def __init__(self, inputs):
        super().__init__(inputs)
        self.too_many_adj = 4

    def create_from(self, seating: List[List[str]]) -> 'Puzzle1':
        return Puzzle1(seating)

    def projection(self, d: str, p: (int, int)) -> (int, int):
        return neighbor(d, p)


def neighbor(d: str, p: (int, int)) -> (int, int):
    x, y = OFFSETS[d]
    return p[0] + x, p[1] + y


class Puzzle2(GameOfSeats):
    def __init__(self, inputs):
        super().__init__(inputs)
        self.too_many_adj = 5

    def create_from(self, seating: List[List[str]]) -> 'Puzzle2':
        return Puzzle2(seating)

    def projection(self, d: str, p: (int, int)) -> (int, int):
        while True:
            p = neighbor(d, p)
            if not self.within_outer_ring(p) or self.seat(p) != FLOOR:
                return p


class Test(unittest.TestCase):
    def test_projection(self):
        p = Puzzle2("day11_ex1.txt")
        self.assertEqual((-2, 0), p.projection('W', (0, 0)))

    def test_adj(self):
        p = Puzzle1("day11_ex1.txt")
        p = p.create_next()
        self.assertEqual(2, p.num_adj_occupied((0, 0)))
        self.assertEqual(4, p.num_adj_occupied((2, 0)))

    def test_puzzle_1(self):
        self.assertEqual(num_occupied_at_stable(Puzzle1("day11_ex1.txt")), 37)

    def test_puzzle_2(self):
        self.assertEqual(num_occupied_at_stable(Puzzle2("day11_ex1.txt")), 26)


if __name__ == '__main__':
    unittest.main()
