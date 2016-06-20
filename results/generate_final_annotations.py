import csv
import warnings
from collections import defaultdict
from tabulate import tabulate # use `pip install tabulate` on the command-line
from operator import itemgetter
from collections import Counter

FILE1 = './annotations_emiel.tsv'
FILE2 = './annotations_roser.tsv'

SETTLED = './settled_disagreements.tsv'

def load_annotations(filename):
    """
    Takes a filename and returns a dictionary with k = (neg,sent), v = cat.
    """
    with open(filename) as f:
        next(f) # Skip header
        reader = csv.reader(f, delimiter='\t')
        return {(neg,sent): cat for neg, cat, sent in reader}

def load_settled(filename):
    """
    Loads the file with all the disagreements and the categories we settled on.
    """
    d = dict()
    with open(filename) as f:
        next(f) # Skip header
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            cat = row[0]
            # If the category is specified
            if cat:
                # Get the negation and the sentence
                neg, sent = row[1:3]
                # And add an entry.
                d[(neg,sent)] = cat
    return d

first = load_annotations(FILE1)
second = load_annotations(FILE2)

categories_prior_to_settling = set(first.values())

settle_dict = load_settled(SETTLED)

# Update annotations for Emiel:
first.update(settle_dict)
# Update annotations for Roser:
second.update(settle_dict)

# Sanity checks: does settling the disagreements really work?

# If this works, we haven't missed anything.
assert first == second

# If this works, then we didn't make any typos.
categories_after_settling = set(first.values())
assert categories_after_settling == categories_prior_to_settling

################################################################################
# Write the data
################################################################################

with open('final_annotations.tsv', 'w') as f:
    writer = csv.writer(f,delimiter='\t')
    writer.writerow(['Negation type','Category','Sentence'])
    for pair, cat in first.items():
        neg, sent = pair
        writer.writerow([neg, cat, sent])

################################################################################
# Category frequency
################################################################################

# Count the categories.
c = Counter(first.values())
print(tabulate(c.most_common(), tablefmt='latex_booktabs'))

################################################################################
# False positives
################################################################################

# Remove False positives to count the types of negations.
without_FP = {data:cat for data,cat in first.items() if not cat == 'False positive'}

# If this is false, there is a typo on the dict comprehension.
assert len(without_FP) < len(first)

# Get statistics and generate the table:
c = Counter(neg for neg,sent in first.keys())
print(tabulate(c.most_common(), tablefmt='latex_booktabs'))

################################################################################
# Shirts and shoes
################################################################################
with open('shirts.txt','w') as f:
    for neg,sent in without_FP.keys():
        if 'shirt' in sent:
            f.write(sent + '\n')

with open('shoes.txt','w') as f:
    for neg,sent in without_FP.keys():
        if 'shoe' in sent:
            f.write(sent + '\n')
