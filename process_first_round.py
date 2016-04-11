import csv

# Open all files
with open('annotations.tsv') as annotations, \
     open('first_round.tsv','w') as backup, \
     open('contrast.txt','w') as contrast:
    
    # Define CSV handlers:
    reader = csv.reader(annotations, delimiter='\t')
    writer = csv.writer(backup, delimiter='\t')
    
    # Processing the rows:
    for row in reader:
        writer.writerow(row)
        neg, cat, sentence = row
        if cat == 'Contrast':
            contrast.write(sentence + '\n')
