from unittest import TestCase
from mock import MagicMock as Mock
from termResolver import FractionTermResolver
__author__ = 'kuddai'



class TestFractionTermResolver(TestCase):

    def test_our_team_fraction(self, get_win_loses):
        stpc_mock = Mock()
        stpc_mock.get_wins_loses.return_value = (2, 3)

        frte
