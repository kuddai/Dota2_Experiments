from unittest import TestCase
from PairsContainer import OppositeTeamPairsContainer
__author__ = 'kuddai'


class TestOppositeTeamPairsContainer(TestCase):
    def setUp(self):
        self.otpc = OppositeTeamPairsContainer()

    def test_get_wins_loses(self):
        opposite_team_pairs = {(1, 4): [1, 2]}
        otpc = OppositeTeamPairsContainer(opposite_team_pairs)

        self.assertEqual(otpc.get_wins_loses(1, 4), (1, 2))
        self.assertEqual(otpc.get_wins_loses(4, 1), (2, 1))

        self.assertEqual(otpc.get_wins_loses(5, 7), (0, 0))

    def test_increment_win_ordered_keys(self):
        otpc = self.otpc

        otpc.increment_win(3, 5)
        otpc.increment_win(3, 5)
        otpc.increment_win(4, 5)

        self.assertEqual(otpc.team_pairs[3, 5], [2, 0])
        self.assertEqual(otpc.team_pairs[4, 5], [1, 0])

    def test_increment_win_reverse_keys(self):
        otpc = self.otpc

        otpc.increment_win(9, 6)
        otpc.increment_win(9, 6)
        otpc.increment_win(12, 9)

        self.assertEqual(otpc.team_pairs[6, 9], [0, 2])
        self.assertEqual(otpc.team_pairs[9, 12], [0, 1])

    def test_increment_win_mixture_keys(self):
        otpc = self.otpc

        otpc.increment_win(10, 12)
        otpc.increment_win(10, 12)
        otpc.increment_win(12 ,10)

        self.assertEqual(otpc.team_pairs[10, 12], [2, 1])

    def test_increment_lose_ordered_keys(self):
        otpc = self.otpc

        otpc.increment_lose(3, 5)
        otpc.increment_lose(3, 5)
        otpc.increment_lose(4, 5)

        self.assertEqual(otpc.team_pairs[3, 5], [0, 2])
        self.assertEqual(otpc.team_pairs[4, 5], [0, 1])

    def test_increment_lose_reversed_keys(self):
        otpc = self.otpc

        otpc.increment_lose(5, 3)
        otpc.increment_lose(5, 3)
        otpc.increment_lose(5, 4)

        self.assertEqual(otpc.team_pairs[3, 5], [2, 0])
        self.assertEqual(otpc.team_pairs[4, 5], [1, 0])

    def test_increment_lose_mixture(self):
        otpc = self.otpc

        otpc.increment_lose(6, 7)
        otpc.increment_lose(6, 7)
        otpc.increment_lose(7, 6)

        self.assertEqual(otpc.team_pairs[6, 7], [1, 2])

    def test_increment_mixture(self):
        otpc = self.otpc

        otpc.increment_lose(5, 7)
        otpc.increment_win(5, 7)
        otpc.increment_win(7, 5)

        self.assertEqual(otpc.team_pairs[5, 7], [1, 2])




