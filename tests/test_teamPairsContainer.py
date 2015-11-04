from unittest import TestCase
from PairsContainer import  TeamPairsContainer
__author__ = 'kuddai'


class TestTeamPairsContainer(TestCase):
    def test_init(self):
        tpc = TeamPairsContainer()

        self.assertEqual(len(tpc.team_pairs), 0)

    def test_get_matches_count(self):
        team_pairs = {(1, 2): [2, 3], (4, 6): [0, 2]}
        tpc = TeamPairsContainer(team_pairs)

        self.assertEqual(tpc.get_matches_count(6, 8), 0)
        self.assertEqual(tpc.get_matches_count(4, 6), 2)
        self.assertEqual(tpc.get_matches_count(1, 2), 5)
