from unittest import TestCase
import mock
from termResolver import TermResolver
__author__ = 'kuddai'


class TestTermResolver(TestCase):

    def setUp(self):
        #set up test example
        self.stpc = mock.MagicMock()
        self.stpc.get_wins_loses.return_value = (2, 3)

        self.dtpc = mock.MagicMock()
        self.dtpc.get_wins_loses.return_value = (5, 9)

        self.shrc = { 5: (1, 6)}

        team_offset = 1000
        self.tr = TermResolver(team_offset, self.shrc, self.stpc, self.dtpc)

    def test_our_single_hero(self):
        self.assertEqual(self.tr[5], (1, 6))

    def test_opposite_single_hero(self):
        self.assertEqual(self.tr[1005], (6, 1))

    def test_our_team(self):
        self.assertEqual(self.tr[7, 8], (2, 3))
        self.stpc.get_wins_loses.assert_called_once_with(7, 8)

    def test_oppsite_team(self):
        self.assertEqual(self.tr[1008, 1007], (3, 2))
        self.stpc.get_wins_loses.assert_called_once_with(8, 7)

    def test_different_teams(self):
        self.assertEqual(self.tr[7, 1008], (5, 9))
        self.dtpc.get_wins_loses.assert_called_once_with(7, 8)


