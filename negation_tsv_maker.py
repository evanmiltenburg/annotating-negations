import csv
import glob
import json

from collections import defaultdict

FREE_NEG = {"not", "n't"}
NO_NEG = {"never", "no", "none", "nothing", "nobody", "nowhere", "nor", "neither"}
PREPOSITIONS = {"without", "sans", "minus"}#, "except", "from", "out", "off"}
VERBS = {"lack", "omit", "miss", "fail"}

TO_MATCH = FREE_NEG | NO_NEG | PREPOSITIONS

# Translation table to strip the annotations.
TABLE = str.maketrans("","",']')

def lines_in_doc(doc):
    "Remove annotations and tokenize the line."
    with open(doc) as f:
        for line in f:
            yield [word.lower() for word in line.translate(TABLE).split()
                                if not word.startswith('[/EN')]

def doc_to_id(doc):
    return doc.split('/')[-1].split('.')[0]

def lines_containing_negation():
    for doc in glob.glob('Flickr30k/*.txt'):
        ident = doc_to_id(doc)
        for line in lines_in_doc(doc):
            bag_of_words = set(line)
            if TO_MATCH & bag_of_words:
                yield (ident, ' '.join(line))
            for word in bag_of_words:
                for verb in VERBS:
                    if word.startswith(verb):
                        yield (ident, ' '.join(line))

with open('flickr30K_negations.tsv','w') as f:
    unique_sents = set(lines_containing_negation())
    writer = csv.writer(f, delimiter='\t')
    writer.writerows(unique_sents)
