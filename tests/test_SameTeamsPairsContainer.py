from unittest import TestCase
from PairsContainer import SameTeamsPairsContainer

__author__ = 'kuddai'


class TestSameTeamPairsContainer(TestCase):
    def setUp(self):
        self.stpc = SameTeamsPairsContainer()
    
    def test_get_wins_loses(self):
        same_teams_pairs = {(1, 4): [1, 2]}
        stpc = SameTeamsPairsContainer(same_teams_pairs)

        self.assertEqual(stpc.get_wins_loses(1, 4), (1, 2))
        self.assertEqual(stpc.get_wins_loses(4, 1), (1, 2))

        self.assertEqual(stpc.get_wins_loses(5, 7), (0, 0))

    def test_increment_win_ordered_keys(self):
        stpc = self.stpc

        stpc.increment_win(3, 5)
        stpc.increment_win(3, 5)
        stpc.increment_win(4, 5)

        self.assertEqual(stpc.teams_pairs[3, 5], [2, 0])
        self.assertEqual(stpc.teams_pairs[4, 5], [1, 0])

    def test_increment_win_reverse_keys(self):
        stpc = self.stpc

        stpc.increment_win(9, 6)
        stpc.increment_win(9, 6)
        stpc.increment_win(9, 8)

        self.assertEqual(stpc.teams_pairs[6, 9], [2, 0])
        self.assertEqual(stpc.teams_pairs[8, 9], [1, 0])

    def test_increment_win_mixture_keys(self):
        stpc = self.stpc

        stpc.increment_win(10, 12)
        stpc.increment_win(10, 12)
        stpc.increment_win(12 ,10)

        self.assertEqual(stpc.teams_pairs[10, 12], [3, 0])

    def test_increment_lose_ordered_keys(self):
        stpc = self.stpc

        stpc.increment_lose(3, 5)
        stpc.increment_lose(3, 5)
        stpc.increment_lose(4, 5)

        self.assertEqual(stpc.teams_pairs[3, 5], [0, 2])
        self.assertEqual(stpc.teams_pairs[4, 5], [0, 1])

    def test_increment_lose_reversed_keys(self):
        stpc = self.stpc

        stpc.increment_lose(5, 3)
        stpc.increment_lose(5, 3)
        stpc.increment_lose(5, 4)

        self.assertEqual(stpc.teams_pairs[3, 5], [0, 2])
        self.assertEqual(stpc.teams_pairs[4, 5], [0, 1])

    def test_increment_lose_mixture(self):
        stpc = self.stpc

        stpc.increment_lose(6, 7)
        stpc.increment_lose(6, 7)
        stpc.increment_lose(7, 6)

        self.assertEqual(stpc.teams_pairs[6, 7], [0, 3])

    def test_increment_mixture(self):
        stpc = self.stpc

        stpc.increment_lose(5, 7)
        stpc.increment_win(5, 7)
        stpc.increment_win(7, 5)

        self.assertEqual(stpc.teams_pairs[5, 7], [2, 1])



