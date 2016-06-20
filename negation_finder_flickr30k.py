import csv
import glob
import json

from collections import defaultdict

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

# Translation table to strip the annotations.
TABLE = str.maketrans("","",']')

def words_in_doc(doc):
    "Remove annotations and tokenize the line."
    with open(doc) as f:
        for line in f:
            for word in line.translate(TABLE).split():
                if not word.startswith('[/EN'):
                    yield word.lower()

def matches_for_doc(doc):
    "Checks whether the line contains a negation. Returns a set of matches."
    bag_of_words = set(words_in_doc(doc))
    matches = TO_MATCH & bag_of_words
    for word in bag_of_words:
        for verb in VERBS:
            if word.startswith(verb):
                matches.add(verb)
    return matches

def documents_containing_negation():
    "Look for documents containing negations. Returns a list of documents."
    for doc in glob.glob('Flickr30k/*.txt'):
        matches = matches_for_doc(doc)
        if matches:
            yield doc, matches

def match_length(dm):
    "Useful measure"
    return len(dm[1])

l = sorted(documents_containing_negation(), key=match_length, reverse=True)
d = defaultdict(list)

# Write everything out to a dictionary.
for doc, matches in l:
    doc_id = doc.split('/')[-1][:-4]
    for match in matches:
        d[match].append(doc_id)
with open('flickr30k.json', 'w') as fp:
    json.dump(d, fp)


def lines_in_doc(doc):
    "Remove annotations and tokenize the line."
    with open(doc) as f:
        for line in f:
            yield [word.lower() for word in line.translate(TABLE).split()
                                if not word.startswith('[/EN')]

def lines_containing_negation():
    for doc in glob.glob('Flickr30k/*.txt'):
        for line in lines_in_doc(doc):
            bag_of_words = set(line)
            if TO_MATCH & bag_of_words:
                yield ' '.join(line)
            for word in bag_of_words:
                for verb in VERBS:
                    if word.startswith(verb):
                        yield ' '.join(line)

with open('captions_flickr30k.txt','w') as f:
    negation_sents = list(lines_containing_negation())
    unique_sents = set(negation_sents)
    print("Tokens:", len(negation_sents))
    print("Types:", len(unique_sents))
    for line in unique_sents:
        f.write(line + '\n')
