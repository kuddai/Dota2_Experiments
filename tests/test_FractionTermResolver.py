from unittest import TestCase
import mock
from termResolver import FractionTermResolver
__author__ = 'kuddai'



class TestFractionTermResolver(TestCase):

    def setUp(self):
        #set up test example
        self.stpc = mock.MagicMock()
        self.stpc.get_wins_loses.return_value = (1, 2)

        self.dtpc = mock.MagicMock()
        self.dtpc.get_wins_loses.return_value = (4, 6)

        self.shrc = { 5: (2, 3)}

        self.delta = 0.00001
        self.team_offset = 1000

    def test_with_default_smoothing(self):
        tr = FractionTermResolver(self.team_offset, self.shrc, self.stpc, self.dtpc)

        #test our single hero
        self.assertAlmostEqual(tr[5], 2.0/5, delta=self.delta)

        #test opposite single hero
        self.assertAlmostEqual(tr[1005], 3.0/5, delta=self.delta)

        #test our team
        self.assertAlmostEqual(tr[4, 5], 1.0/3, delta=self.delta)
        self.stpc.get_wins_loses.assert_called_with(4, 5)

        #test opposite team
        self.assertAlmostEqual(tr[1004, 1005], 2.0/3, delta=self.delta)
        self.stpc.get_wins_loses.assert_called_with(4, 5)

        #test different teams
        self.assertAlmostEqual(tr[4, 1008], 4.0/10, delta=self.delta)
        self.dtpc.get_wins_loses.assert_called_with(4, 8)

    def test_win_custom_smoothing(self):
        eps = 0.5
        tr = FractionTermResolver(self.team_offset, self.shrc, self.stpc, self.dtpc, eps)

        #test our single hero
        self.assertAlmostEqual(tr[5], (2.0 + eps)/(5 + 2 * eps), delta=self.delta)

        #test opposite single hero
        self.assertAlmostEqual(tr[1005], (3.0 + eps)/(5 + 2 * eps), delta=self.delta)

        #test our team
        self.assertAlmostEqual(tr[4, 5], (1.0 + eps)/(3 + 2 * eps), delta=self.delta)
        self.stpc.get_wins_loses.assert_called_with(4, 5)

        #test opposite team
        self.assertAlmostEqual(tr[1004, 1005], (2.0 + eps)/(3 + 2 * eps), delta=self.delta)
        self.stpc.get_wins_loses.assert_called_with(4, 5)

        #test different teams
        self.assertAlmostEqual(tr[4, 1008], (4.0 + eps)/(10 + 2 * eps), delta=self.delta)
        self.dtpc.get_wins_loses.assert_called_with(4, 8)
