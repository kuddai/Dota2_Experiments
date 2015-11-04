from abc import ABCMeta, abstractmethod
from collections import defaultdict
from PairsContainer import SameTeamsPairsContainer, DifferentTeamsPairsContainer
__author__ = 'kuddai'

class TermResolver(object):
    __metaclass__ = ABCMeta

    def __init__(self, team_offset, solo_hrs, same_teams_hrs, diff_teams_hrs):
        assert team_offset > 0

        self.team_offset = team_offset
        self.solo_hrs = solo_hrs
        self.same_teams_hrs = same_teams_hrs
        self.diff_teams_hrs = diff_teams_hrs

    def __is_our_team(self, hero1_id, hero2_id):
        return hero1_id <= self.team_offset and hero2_id <= self.team_offset

    def __is_opposite_team(self, hero1_id, hero2_id):
        return hero1_id >  self.team_offset and hero2_id >  self.team_offset

    @abstractmethod
    def __get_term(self, win_count, lose_count):
        pass

    def __get_win_odds(self, key):
        if isinstance(key, int):
            return tuple(self.solo_hrs[key])

        assert isinstance(key, tuple)
        assert len(key) == 2

        hero1_id, hero2_id = key
        offset = self.team_offset

        if self.__is_our_team(hero1_id, hero2_id):
            return self.same_teams_hrs.get_wins_loses(hero1_id, hero2_id)

        if self.__is_opposite_team(hero1_id, hero2_id):
            #normalizing
            hero1_id, hero2_id = hero1_id - offset, hero2_id - offset
            w, l = self.same_teams_hrs.get_wins_loses(hero1_id, hero2_id)
            #swaping because they are from opposite team
            #so the more opposite team lose the more our victory is likely
            return (l, w)

        #opposite teams
        our_hero_id, other_hero_id = min(hero1_id, hero2_id), max(hero1_id, hero2_id)
        #normalizing
        other_hero_id = other_hero_id - offset
        return self.diff_teams_hrs.get_wins_loses(our_hero_id, other_hero_id)

    def __getitem__(self, key):
        win_count, lose_count = self.__get_win_odds(key)
        return self.__get_term(win_count, lose_count)


