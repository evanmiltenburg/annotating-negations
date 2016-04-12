# Annotating negations

This repository contains the necessary tools and data to annotate sentences
containing negation in the Flickr30k corpus. The annotation script is written in
Python, and makes use of Flask (a web framework) so that you can annotate the data
in your own browser.

## Requirements
* Python 2.7 or 3.5 (I haven't tested on any others, but they should work)
* Flask (use `pip install flask` or `conda install flask` to install)

## Annotation steps

1. `cd` to the environment containing `annotator.py`
2. Use `python annotator.py` to start the script. By default this will start hosting
the annotation page on `http://127.0.0.1:5000/`. If this is an issue, change `app.run()`
to `app.run(port=5555)` or whichever port you prefer.
3. Annotate!
    * Click on one of the items in the sidebar to start annotating.
    * Use the search box to narrow down the list. Typing 'shirt' and pressing ENTER
    will give you all the sentences with 'shirt' in it.
    * Select a category from the list.
    * Either select all sentences that belong to the category, or select all and
    deselect the sentences that do not belong to the category.
    * Submit your selection.
    * Continue untill all sentences have been annotated.
    * Move on to the next item from the side bar.
    * Save your annotations by clicking the SAVE button.

**WARNING** all annotation should be done in one Terminal session.
(Don't worry, you can just leave the server running in the background if you get bored or something.
You can even close your browser and reopen it.
Just don't shut down the Terminal or reboot your computer.
Hibernation should be OK.)

## Second annotation round

Once all the sentences have been annotated, the ones marked as displaying **contrast**
should be annotated once more (to say *what kind of contrast* there is). Here is how:

* Use `python process_first_round.py` to copy the annotated data to `first_round.tsv` and
the contrast sentences to `contrast.txt`.
* Modify line 10 in `annotator.py` by replacing `captions_flickr30k.txt` with `contrast.txt`.
The line should now look like this: `with open('contrast.txt') as f:`.
* Annotate the sentences again, but this time ignoring the Contrast category.

**WARNING** Once you save, the `annotations.tsv` file will get overwritten. Make sure that the script successfully copied your old data to `first_round.tsv` or that you have backed up the TSV file some other way.
