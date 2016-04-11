from flask import Flask, url_for, request, render_template, redirect

import csv
from collections import defaultdict
from operator import itemgetter

app = Flask(__name__)

# General setup
with open('captions_flickr30k.txt') as f:
    lines = {line.strip() for line in f}

FREE_NEG = {"not", "n't"}
NO_NEG = {"never", "no", "none", "nothing", "nobody", "nowhere", "nor", "neither"}
PREPOSITIONS = {"without", "sans", "minus"}#, "except", "from", "out", "off"}

# Special cases:
VERBS = {"lack", "omit", "miss", "fail"}
# Others:
TO_MATCH = FREE_NEG | NO_NEG | PREPOSITIONS


#
d = defaultdict(list)

for line in lines:
    tokens = set(line.split())
    intersection = tokens & TO_MATCH
    for i in intersection:
        d[i].append(line)
    for tok in tokens:
        for verb in VERBS:
            if tok.startswith(verb):
                d[verb].append(line)

categorized = dict()
for neg, sents in d.items():
    categorized[neg] = defaultdict(list)
    categorized[neg]['uncategorized'] = sents

categories = {'Contrast',
              'Salient absence',
              'Negation of action/behavior',
              'Negation of property',
              'Negation of attitude',
              '(Preventing) future events',
              'Outside the frame',
              'Quotes and idioms',
              'Other'}

def negs():
    "Return all negations and statistics about how far we are."
    data = []
    for neg, d in categorized.items():
        uncategorized = len(d['uncategorized'])
        all_sents = sum(len(sents) for sents in d.values())
        data.append((neg, all_sents-uncategorized, all_sents))
    return sorted(data,key=itemgetter(2))

@app.route('/')
def main_page():
    "Render the main page."
    # Check whether we're done yet:
    to_do = [sentence for neg in categorized
                      for sentence in categorized[neg]['uncategorized']]
    done = len(to_do) == 0
    return render_template('index.html',
                            nav=negs(),
                            render_form= False,
                            done=done)

@app.route('/search', methods=['POST'])
def search():
    "Implements search function over uncategorized sentences."
    query = request.form['query']
    neg = request.form['neg']
    remaining_sentences = [sent for sent in categorized[neg]['uncategorized']
                                if query in sent]
    return render_template('index.html',
                            nav=negs(),
                            neg=neg,
                            render_form= True,
                            items=remaining_sentences,
                            categories=categories,
                            done=False,
                            query=query)

@app.route('/annotate/<neg>', methods=['GET','POST'])
def present_form(neg):
    """
    Processes the data in the annotation form (if POST), and returns the
    annotation page for a particular category.
    """
    if neg not in d:
        return redirect('/')
    
    if request.method == 'POST':
        category = request.form['category']
        if category == 'OTHER':
            category = request.form['other']
            categories.add(category)
        
        global categorized
        sentences = request.form.getlist('sentence')
        categorized[neg]['uncategorized'] = [sentence for sentence in categorized[neg]['uncategorized']
                                                      if not sentence in sentences]
        categorized[neg][category] += sentences
    
    remaining_sentences = categorized[neg]['uncategorized']
    return render_template('index.html',
                            nav=negs(),
                            neg=neg,
                            render_form= len(remaining_sentences) > 0,
                            items=remaining_sentences,
                            categories=categories,
                            done= len(remaining_sentences) == 0)

def generate_rows():
    "Helper function to generate the rows of the TSV file."
    for neg, d in categorized.items():
        for category, sentences in d.items():
            for sentence in sentences:
                yield [neg, category, sentence]

@app.route('/save')
def save():
    "Save the annotations in a TSV file."
    with open('annotations.tsv','w') as f:
        writer = csv.writer(f, delimiter='\t')
        rows = generate_rows()
        writer.writerow(['Negation type', 'Category', 'Sentence'])
        writer.writerows(rows)
    
    to_do = [sentence for neg in categorized
                      for sentence in categorized[neg]['uncategorized']]
    done = len(to_do) == 0
    return render_template('index.html',
                            nav=negs(),
                            render_form=False,
                            saved=True,
                            done=done)

if __name__ == '__main__':
    app.debug = True
    app.run()
