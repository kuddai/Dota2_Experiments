from unittest import TestCase
from PairsContainer import OppositeTeamPairsContainer
__author__ = 'kuddai'


class TestOppositeTeamPairsContainer(TestCase):
    def setUp(self):
        self.otpc = OppositeTeamPairsContainer()

    def test_init(self):
        self.assertEqual(self.otpc.get_matches_count(1, 2), 0)

    def test_increment_win(self):
        otpc = self.otpc
        #ordered keys
        otpc.increment_win(3, 5)
        otpc.increment_win(3, 5)
        otpc.increment_win(4, 5)

        self.assertEqual(otpc.get_wins_loses(3, 5), (2, 0))
        self.assertEqual(otpc.get_wins_loses(5, 3), (0, 2))

        self.assertEqual(otpc.get_wins_loses(4, 5), (1, 0))
        self.assertEqual(otpc.get_wins_loses(5, 4), (0, 1))

        #reverse keys
        otpc.increment_win(9, 6)
        otpc.increment_win(9, 6)
        otpc.increment_win(9, 8)

        self.assertEqual(otpc.get_wins_loses(9, 6), (2, 0))
        self.assertEqual(otpc.get_wins_loses(6, 9), (0, 2))

        self.assertEqual(otpc.get_wins_loses(9, 8), (1, 0))
        self.assertEqual(otpc.get_wins_loses(8, 9), (0, 1))

    def test_increment_lose(self):
        otpc = self.otpc
        otpc.increment_lose(3, 5)
        otpc.increment_lose(3, 5)
        otpc.increment_lose(4, 5)

        self.assertEqual(otpc.get_matches_count(3, 5), 2)
        self.assertEqual(otpc.get_matches_count(4, 5), 1)

        self.assertEqual(otpc.get_wins_loses(3, 5), (0, 2))
        self.assertEqual(otpc.get_wins_loses(4, 5), (0, 1))



