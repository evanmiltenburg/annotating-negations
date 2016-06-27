import json
import itertools
from collections import defaultdict, Counter
import numpy as np
from nltk.tokenize import word_tokenize

with open('MSCOCO/captions_train2014.json') as f1,\
     open('MSCOCO/captions_val2014.json') as f2:
     d1 = json.load(f1)
     d2 = json.load(f2)

image_captions_dict = defaultdict(list)
for d in itertools.chain(d1['annotations'], d2['annotations']):
    image_captions_dict[d['image_id']].append(d['caption'])

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

def words_in_doc(doc):
    "Tokenize captions using split, return list of words."
    return [w for caption in doc for w in caption.split()]

def line_contains_negation(line):
    "Checks whether the line contains a negation. Returns a set of matches."
    tokenized = word_tokenize(line)
    bag_of_words = set(tokenized)
    if TO_MATCH & bag_of_words:
        return True
    for word in bag_of_words:
        for verb in VERBS:
            if word.startswith(verb):
                return True
    return False

all_negations = []
counts = []
for image_id, doc in image_captions_dict.items():
    lines_with_negations = [line for line in doc if line_contains_negation(line)]
    all_negations.extend(lines_with_negations)
    counts.append(len(lines_with_negations))

print('Sentence tokens:', len(all_negations))
print('Sentence types:', len(set(all_negations)))

print("Percentage:", (len(all_negations)/float(len(image_captions_dict.items()))) * 100)

print('Number of descriptions with negations per image:')
c = Counter(counts)
del c[0]
x,y = zip(*sorted(c.items()))
print(x)
print(y)

total = np.matrix(y) * np.matrix(x).T
print("Negations per image:" + str(total/float(sum(y))))
