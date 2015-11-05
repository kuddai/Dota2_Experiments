__author__ = 'kuddai'
#it is expected that local database is working here
import cPickle as pickle
import random
from progressbar import ProgressBar, Bar, Percentage, FormatLabel, ETA
from pymongo import MongoClient

#based on https://github.com/kevincon/dotaml/blob/master/k_nearest_neighbors/preprocess.py
# and https://wiki.teamfortress.com/wiki/WebAPI/GetMatchDetails#Player_Slot

client = MongoClient()
db = client['dotabot']
matches = db['matches']

NUM_MATCHES = matches.count()
compressed_matches = []

widgets = [FormatLabel('Processed: %(value)d/%(max)d matches. '), ETA(), Percentage(), ' ', Bar()]
pbar = ProgressBar(widgets=widgets, maxval=NUM_MATCHES).start()

for i, match in enumerate(matches.find()):
    radiant_win = match['radiant_win']
    radiant, dire = [], []

    for player in match['players']:
        is_radiant = player['player_slot'] &(1 << 7) == 0
        hero_id = player['hero_id']
        if is_radiant:
            radiant.append(hero_id)
        else:
            dire.append(hero_id)

    if len(radiant) != 5 or len(dire) != 5:
        print "match {0} doesn't have enough players".format(i)

    compressed_matches.append((radiant_win, radiant, dire))
    pbar.update(i)

pbar.finish()

print "shuffling matches"
random.shuffle(compressed_matches)

train_data = compressed_matches[NUM_MATCHES/10:NUM_MATCHES]
test_data = compressed_matches[0:NUM_MATCHES/10]

train_name = "train_data{0}.p".format(len(train_data))
test_name = "test_data{0}.p".format(len(test_data))



pickle.dump(train_data, open(train_name, 'wb'))
pickle.dump(test_data, open(test_name, 'wb'))