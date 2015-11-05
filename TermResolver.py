from collections import defaultdict
from abc import ABCMeta, abstractmethod
__author__ = 'kuddai'

class TermResolver(object):
    __metaclass__ = ABCMeta

    def __init__(self, team_offset, solo_hrs, same_teams_hrs, diff_teams_hrs):
        assert team_offset > 0

        self.team_offset = team_offset
        if solo_hrs is None:
            solo_hrs = {}
        self.solo_hrs = defaultdict(lambda: [0, 0], solo_hrs)
        self.same_teams_hrs = same_teams_hrs
        self.diff_teams_hrs = diff_teams_hrs

    def __normalize(self, *hero_ids):
        #that all ids correspond to the heroes ids of DOTA 2
        return [hero_id % self.team_offset for hero_id in hero_ids]

    def __get_our_win_odds_our_team_case(self, *hero_ids):
        getter = self.same_teams_hrs.get_wins_loses if len(hero_ids) > 1 else self.solo_hrs.get
        w, l = getter(*hero_ids)
        return w, l

    def __get_our_win_odds_opposite_team_case(self, *hero_ids):
        getter = self.same_teams_hrs.get_wins_loses if len(hero_ids) > 1 else self.solo_hrs.get
        w, l = getter(*self.__normalize(*hero_ids))
        #swaping because they are from opposite team
        #so the more opposite team lose the more our victory is likely
        return l, w

    def __get_our_win_odds_different_teams_case(self, hero1_id, hero2_id):
        #our hero < team_offset and opposite here >= team_offset
        our_hero_id, opposite_hero_id = min(hero1_id, hero2_id), max(hero1_id, hero2_id)
        opposite_hero_id = self.__normalize(opposite_hero_id)[0]
        return self.diff_teams_hrs.get_wins_loses(our_hero_id, opposite_hero_id)

    def __is_our_team(self, *hero_ids):
        return all(hero_id <  self.team_offset for hero_id in hero_ids)

    def __is_opposite_team(self, *hero_ids):
        return all(hero_id >= self.team_offset for hero_id in hero_ids)

    @abstractmethod
    def get_term(self, positive_odds, negative_odds):
        pass

    def __get_our_win_odds(self, *hero_ids):
        if self.__is_our_team(*hero_ids):
            return self.__get_our_win_odds_our_team_case(*hero_ids)
        if self.__is_opposite_team(*hero_ids):
            return self.__get_our_win_odds_opposite_team_case(*hero_ids)
        return self.__get_our_win_odds_different_teams_case(*hero_ids)

    def __getitem__(self, key):
        #pack in case of singular value
        key = (key,) if isinstance(key, int) else key
        assert len(key) == 1 or len(key) == 2
        win_count, lose_count = self.__get_our_win_odds(*key)
        return self.get_term(win_count, lose_count)

class FractionTermResolver(TermResolver):

    def __init__(self, team_offset, solo_hrs, same_teams_hrs, diff_teams_hrs, smoothing = 0.0):
        super(FractionTermResolver, self).__init__(team_offset, solo_hrs, same_teams_hrs, diff_teams_hrs)
        self.eps = smoothing

    def get_term(self, positive_odds, negative_odds):
        if positive_odds == 0 and negative_odds == 0:
            return 1
        return (positive_odds + 1.0 * self.eps) / (positive_odds + negative_odds + 2.0 * self.eps)

class OddsTermResolver(TermResolver):
    def __init__(self, team_offset, solo_hrs, same_teams_hrs, diff_teams_hrs):
        super(OddsTermResolver, self).__init__(team_offset, solo_hrs, same_teams_hrs, diff_teams_hrs)

    def get_term(self, positive_odds, negative_odds):
        #smoothing in case of zero frequencies
        return  positive_odds + 1.0

