from pairsContainer import SameTeamsPairsContainer, DifferentTeamsPairsContainer
from itertools import combinations, product
from collections import defaultdict
import codecs
import sys
import cPickle as pickle
__author__ = 'kuddai'

# radiant_win, radiant, dire
TRAIN_FILE_NAME = "train_data148064.p"
DEBUG_LAUNCH = False
DEBUG_STOP = 1


print "load train data from {0}".format(TRAIN_FILE_NAME)
train_data = pickle.load(open(TRAIN_FILE_NAME, 'rb'))
print "load complete"
team_offset = 1000

def get_hero_id_to_name():
    import json
    HEROES_NAMES_FILE_NAME = "heroes.json"
    heroes_names_raw = json.load(open(HEROES_NAMES_FILE_NAME, 'rb'))
    hero_id_to_name = {}
    for hero in heroes_names_raw:
        name = hero["localized_name"]
        id = hero["id"]
        hero_id_to_name[id + team_offset] = "*" + name
        hero_id_to_name[id] = name

    return  hero_id_to_name

hero_id_to_name = get_hero_id_to_name()

def show_win_loses(heroes, hr_id_to_nm):
    if isinstance(heroes, dict):
        heroes = heroes.items()

    for key, value in heroes:
        if isinstance(key, int):
            key = (key, )
        names = ["{0:20}".format(hero_id_to_name[id]) for id in key]
        name = "| ".join(names)
        print "{0} {1:0>5} {2:0>5}".format(name, *value)

solo_hr = defaultdict(lambda: [0, 0])
stpc = SameTeamsPairsContainer()
dtpc = DifferentTeamsPairsContainer()
WIN_INDEX, LOSE_INDEX = 0, 1

same_triple = defaultdict(lambda: [0, 0])

for i, record in enumerate(train_data):
    radiant_win, radiant, dire = record
    winners, losers = (radiant, dire) if radiant_win else (dire, radiant)
    #solo heroes
    for hero_id in winners:
        solo_hr[hero_id][WIN_INDEX] += 1

    for hero_id in losers:
        solo_hr[hero_id][LOSE_INDEX] += 1

    for hero1_id, hero2_id in combinations(winners, 2):
        stpc.increment_win(hero1_id, hero2_id)

    for key in combinations(winners, 3):
        same_triple[frozenset(key)][WIN_INDEX] += 1

    for key in combinations(losers, 3):
        same_triple[frozenset(key)][LOSE_INDEX] += 1

    for hero1_id, hero2_id in combinations(losers, 2):
        stpc.increment_lose(hero1_id, hero2_id)

    #decart product
    for won_hero_id, lost_hero_id in product(winners, losers):
        dtpc.increment_win(won_hero_id, lost_hero_id)

    if DEBUG_LAUNCH:
        print "radiant win %s" % radiant_win
        print "winners: %s" % ", ".join(map(lambda x: hero_id_to_name[x],winners))
        print "losers: %s" % ", ".join(map(lambda x: hero_id_to_name[x],losers))
        print " "
        print "#####SOLO HEROES######"
        show_win_loses(solo_hr, hero_id_to_name)
        print " "
        print "#####SAME TEAMS#######"
        show_win_loses(stpc.teams_pairs, hero_id_to_name)
        print stpc.teams_pairs
        print len(stpc.teams_pairs)
        print " "
        print "#####DIFFERENT TEAMS##"
        show_win_loses(dtpc.teams_pairs, hero_id_to_name)
        print len(dtpc.teams_pairs)

    if DEBUG_LAUNCH and i == DEBUG_STOP:
        sys.exit(0)

solo_hr = dict(solo_hr)
stpc = dict(stpc.teams_pairs)
dtpc = dict(dtpc.teams_pairs)

best_win_rate  = lambda x: float(x[1][0])/(x[1][1] + x[1][0])
worst_win_rate = lambda x: float(x[1][1])/(x[1][1] + x[1][0])

print " "
print "#####BEST COMBOS##"
print len(stpc)
best_combo = sorted(stpc.items(), key=best_win_rate, reverse=True)
best_combo = best_combo[:100]
show_win_loses(best_combo, hero_id_to_name)

print " "
print "#####WORST COMBOS##"
print len(stpc)
worst_combo = sorted(stpc.items(), key=worst_win_rate, reverse=False)
worst_combo = worst_combo[:100]
show_win_loses(worst_combo, hero_id_to_name)

def against_key(record):
    w, l = record[1]
    return max(float(w)/(w + l), float(l)/(w + l))

print " "
print "#####BEST AGAINST##"
print len(dtpc)
best_against = sorted(dtpc.items(), key=against_key, reverse=True)
best_against = best_against[:100]
show_win_loses(best_against, hero_id_to_name)

print " "
print "#####BEST TRIPLES##"
sorted_triple = sorted(same_triple.items(), key=worst_win_rate, reverse=True)
print "total triples:", len(sorted_triple)
best_triple = sorted_triple[:100]
show_win_loses(best_triple, hero_id_to_name)

print " "
print "#####BEST SOLO######"
best_solo = sorted(solo_hr.items(), key=lambda record: float(record[1][0])/record[1][1], reverse=True)
show_win_loses(best_solo, hero_id_to_name)



stat_data = (solo_hr, stpc, dtpc)
print "saving on stat_data.p"
pickle.dump(stat_data, open("stat_data.p", 'wb'))
print "saving complete"






