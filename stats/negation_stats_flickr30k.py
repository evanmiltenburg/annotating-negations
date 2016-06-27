import csv
import glob

from collections import Counter
import matplotlib.pyplot as plt
import seaborn
import numpy as np
# Negations: match the word.
# ADJECTIVES = {"absent", "away", "clear", "deprived", "devoid", "free", "removed", "stripped", "vanished"}
# ADVERBS = {"barely", "hardly", "scarcely"}
FREE_NEG = {"not", "n't"}
NO_NEG = {"never", "no", "none", "nothing", "nobody", "nowhere", "nor", "neither"}
PREPOSITIONS = {"without", "sans", "minus"}#, "except", "from", "out", "off"}
# NPIS = {"any","anything"} # to make sure we don't miss anything.

# with open('./negations.csv') as f:
#     reader = csv.reader(f)
#     AFFIXED = {word for word, yes_no in reader if yes_no == 'yes'}

# Negations: special cases.
# PREFIXES = {"a", "dis", "in", "im", "non", "un"}
# SUFFIXES = {"less"}
VERBS = {"lack", "omit", "miss", "fail"}

# All.
TO_MATCH = FREE_NEG | NO_NEG | PREPOSITIONS

def lines_in_doc(doc):
    "Remove annotations and tokenize the line."
    with open(doc) as f:
        for line in f:
            yield [word.lower() for word in line.translate(None,']').split() if not word.startswith('[/EN')]

def match_in_line(line):
    "Checks whether the line contains a negation."
    bag_of_words = set(line)
    if TO_MATCH & bag_of_words:
        return True
    for word in bag_of_words:
        for verb in VERBS:
            if word.startswith(verb):
                return True
    return False

def negations_per_doc():
    "Returns a list with the number of negations for each document."
    counts = []
    for doc in glob.glob('Flickr30k/*.txt'):
        lines_with_negation = [line for line in lines_in_doc(doc)
                                    if match_in_line(line)]
        num_lines = len(lines_with_negation)
        counts.append(num_lines)
    return counts

counts = negations_per_doc()
c = Counter(counts)
del c[0]
x,y = zip(*sorted(c.items()))
print(y)

total = np.matrix(y) * np.matrix(x).T
print("Negations per image:" + str(total/float(sum(y))))

plt.bar(x, y)
plt.savefig('stats_bars.pdf')
