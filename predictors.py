__author__ = 'kuddai'
from math import log, exp
from itertools import combinations, product

class PredictorNaiveBayesBigram(object):
    no_use_counter = 0
    def __init__(self, team_offset, term_resolver) :
        self.tr = term_resolver
        self.team_offset = team_offset

    def __calc_odds(self, our_team, opposite_team):
        tr = self.tr
        offset = self.team_offset
        our_team = our_team[:]
        opposite_team = [ hero_id + offset for hero_id in opposite_team]
        bigrams = list(combinations(our_team + opposite_team, 2))
        #bigrams = list(product(our_team, opposite_team))
        #features = bigrams + our_team + opposite_team
        #features = our_team + opposite_team
        features = bigrams
        terms = map(lambda feature: tr[feature], features)
        #threshold = 0.1
        #terms = [term for term in terms if term < 0.5 - threshold or term > 0.5 + threshold]

        #if len(terms) == 0:
        #    PredictorNaiveBayesBigram.no_use_counter += 1
        #    return 0.5

        log_prob = reduce(lambda res, term: res + log(term), terms, 0.0)
        return log_prob

    def predict(self, our_team, opposite_team):
        our_odds = self.__calc_odds(our_team, opposite_team)
        opposite_team = self.__calc_odds(opposite_team, our_team)
        if our_odds > opposite_team:
            return 1.0
        else:
            return 0.0

