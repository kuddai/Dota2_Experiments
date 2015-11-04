__author__ = 'kuddai'
from collections import defaultdict

class TeamPairsContainer:
    def __init__(self):
        #the keys must be two sorted heroes ID.
        #Default values - wins: 0, loses: 0
        self.team_pairs = defaultdict(lambda: [0, 0])

    def get_wins_loses(self, hero1_ID, hero2_ID):
        raise NotImplementedError()

    def increment_won(self, won_hero1_ID, hero2_ID):
        raise NotImplementedError()

    def increment_lose(self, lost_hero1_ID, hero2_ID):
        raise NotImplementedError

    def get_matches_count(self, hero1_ID, hero2_ID):
        if hero1_ID > hero2_ID:
            #the keys are not sorted -> swap keys
            hero1_ID, hero2_ID = hero2_ID, hero1_ID

        num_win, num_lose = self.team_pairs[hero1_ID, hero2_ID]
        return num_win + num_lose

class OppositeTeamPairsContainer(TeamPairsContainer):
    def __init__(self):
        super(OppositeTeamPairsContainer, self).__init__()

    def get_wins_loses(self, hero1_ID, hero2_ID):
        """
        return tuple to prevent undesired changes of opposite_team_pairs
        :return: wins/loses of hero_ID1 when hero_ID2 was in the opposite team
        """
        if hero1_ID > hero2_ID:
            #swap values
            w, l = self.team_pairs[hero2_ID, hero1_ID]
            return (l, w)

        return  tuple(self.team_pairs[hero1_ID, hero2_ID])

    def increment_win(self, won_hero1_ID, lost_hero2_ID):
        hero_ID1, hero_ID2 = won_hero1_ID, lost_hero2_ID
        win_index, lose_index = 0, 1
        if hero_ID1 > hero_ID2:
            win_index, lose_index = lose_index, win_index
            hero_ID1, hero_ID2 = hero_ID2, hero_ID1

        score = self.team_pairs[hero_ID1, hero_ID2]
        score[win_index] += 1

    def increment_lose(self, lost_hero1_ID, won_hero2_ID):
        #relying on the fact that
        #hero1_ID and hero2_ID are in the different teams.
        #So the winning of one means the loosing of other
        self.increment_win(won_hero2_ID, lost_hero1_ID)

class SameTeamPairsContainer(TeamPairsContainer):
    def __init__(self):
        super(SameTeamPairsContainer, self).__init__()

    def get_wins_loses(self, hero1_ID, hero2_ID):
        """
        return tuple to prevent undesired changes of same_team_pairs
        :return: wins/loses of hero_ID1 when hero_ID2 was in the same team
        """
        if hero1_ID > hero2_ID:
            #the keys are not sorted -> swap keys
            hero1_ID, hero2_ID = hero2_ID, hero1_ID

        return tuple(self.team_pairs[hero1_ID, hero2_ID])

    def __increment(self, hero1_ID, hero2_ID, inc_index):
        if hero1_ID > hero2_ID:
            hero1_ID, hero2_ID = hero2_ID, hero1_ID

        score = self.team_pairs[hero1_ID, hero2_ID]
        score[inc_index] += 1

    def increment_win(self, won_hero1_ID, won_hero2_ID):
        self.increment(won_hero1_ID, won_hero2_ID, 0)

    def increment_lose(self, lost_hero1_ID, lost_hero2_ID):
        self.increment(lost_hero1_ID, lost_hero2_ID, 1)
