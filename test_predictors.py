
from pairsContainer import SameTeamsPairsContainer, DifferentTeamsPairsContainer
from termResolver import *
from itertools import combinations, product
from predictors import *
from collections import defaultdict
import cPickle as pickle
__author__ = 'kuddai'

STAT_FILE_NAME = "stat_data.p"
TEST_DATA_FILE_NAME = "test_data16451.p"
TEAM_OFFSET = 1000

print "load stat data from {0}".format(STAT_FILE_NAME)
stat_data = pickle.load(open(STAT_FILE_NAME, 'rb'))
print "load complete"

print "load test data from {0}".format(TEST_DATA_FILE_NAME)
test_data = pickle.load(open(TEST_DATA_FILE_NAME, 'rb'))
print "load complete"

solo_hr, stpc, dtpc = stat_data
solo_hr = defaultdict(lambda: [0, 0], solo_hr)
stpc = SameTeamsPairsContainer(stpc)
dtpc = DifferentTeamsPairsContainer(dtpc)

tr = FractionTermResolver(TEAM_OFFSET, solo_hr, stpc, dtpc, smoothing=0.5)
#tr = OddsTermResolver(TEAM_OFFSET, solo_hr, stpc, dtpc)
predictor = PredictorNaiveBayesBigram(TEAM_OFFSET, tr)

num_correct = 0.0
num_matches = len(test_data)
for record in test_data:
    radiant_win, radiant, dire = record

    probability = predictor.predict(radiant, dire)

    if probability > 0.5001 and radiant_win or probability < 0.4999 and not radiant_win:
        num_correct += 1.0


print "num matches: {0}".format(num_matches)
print "accuracy: {0}".format(num_correct / num_matches)
