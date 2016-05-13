import csv
import warnings
from collections import defaultdict
from tabulate import tabulate # use `pip install tabulate` on the command-line

FILE1 = './annotations_emiel.tsv'
FILE2 = './annotations_roser.tsv'

def generate_annotation_dict(filename):
    """
    Takes a filename and returns a dictionary cat: {(neg,sent), (neg,sent), ...}
    
    The combination (neg, sent) is necessary because some sentences contain
    multiple negations.
    """
    with open(filename) as f:
        reader = csv.reader(f, delimiter='\t')
        d = defaultdict(set)
        for neg, cat, sent in reader:
            d[cat].add((neg,sent))
        return d

def get_table(d1,d2):
    "Take the annotations, and return a list of categories, along with the table."
    
    # Get the set of categories
    d1_cats = set(d1.keys())
    d2_cats = set(d2.keys())
    
    # See whether both annotators used the same categories. If not, warn the user.
    try:
        assert d1_cats == d2_cats
    except AssertionError:
        warnings.warn("Category sets are not equal.", Warning)
    
    # Create a list of all the categories in sorted order.
    categories = sorted(d1_cats | d2_cats)
    
    # Create the table.
    table = []
    for row in categories:
        table.append([len(d1[col] & d2[row]) for col in categories])
    return categories, table

def agreement_and_kappa(table):
    "Compute agreement score and the kappa score"
    total_agreement = float(sum(table[i][i] for i in range(len(categories))))
    total_examples = float(sum(len(v) for v in d1.values()))
    
    # Compute agreement score:
    agreement_score = total_agreement/total_examples
    
    # How many items are agreed upon by chance?
    all_by_chance = []
    for i in range(len(categories)):
        total_horizontal = float(sum(table[i][j] for j in range(len(table[0]))))
        total_vertical   = float(sum(table[j][i] for j in range(len(table[0]))))
        by_chance = ((total_horizontal/total_examples) * (total_vertical/total_examples)) * total_examples
        all_by_chance.append(by_chance)
    
    # Compute kappa score:
    kappa = (total_agreement - sum(all_by_chance)) / (total_examples- sum(all_by_chance))
    return agreement_score, kappa

def write_disagreements(filename='disagreements.txt'):
    "Write all the lines where "
    with open(filename,'w') as f:
        for cat1, s1 in d1.items():
            for cat2, s2 in d2.items():
                if s1 & s2 and not cat1 == cat2:
                    f.write('-----------------------------------------------------\n')
                    f.write('Roser: ' + cat2 + '\n')
                    f.write('Emiel: ' + cat1 + '\n\n')
                    f.writelines(''.join([str(i), '. ', sent, '\n'])
                                 for i, (neg,sent) in enumerate(s1 & s2, start=1))
                    f.write('\n')

def write_disagreement_csv(filename="disagreements_to_settle.tsv"):
    "Write disagreement data to a CSV file so as to harmonize the data."
    with open(filename,'w') as f:
        writer = csv.writer(f,delimiter='\t')
        writer.writerow(['Category', 'Neg', 'Sent'])
        for cat1, s1 in d1.items():
            for cat2, s2 in d2.items():
                if s1 & s2 and not cat1 == cat2:
                    writer.writerow(['', 'Roser', cat2])
                    writer.writerow(['', 'Emiel', cat1])
                    writer.writerow([])
                    for neg, sent in s1 & s2:
                        writer.writerow(['', neg, sent])
                    writer.writerow([])

# Load the annotation files.
d1 = generate_annotation_dict(FILE1)
d2 = generate_annotation_dict(FILE2)

# get the categories and the table, and print them.
categories, table = get_table(d1,d2)
print(categories)
print(tabulate(table))

# Compute and print the agreement scores.
agreement_score, kappa = agreement_and_kappa(table)
print('Agreement score:', agreement_score)
print('Kappa: ', kappa)

# Write disagreements to a file.
write_disagreements()
write_disagreement_csv()
