# Annotating negations

This repository contains the necessary tools and data to annotate sentences
containing negation in the Flickr30k corpus. The annotation script is written in
Python, and makes use of Flask (a web framework) so that you can annotate the data
in your own browser. If you use our annotation tool, or any of the annotated data,
please cite our paper:

```
@inproceedings{miltenburg2016pragmatic,
	Author = {Emiel van Miltenburg and Roser Morante and Desmond Elliott},
	Booktitle = {Proceedings of the 5$^{th}$ Workshop on Vision and Language},
	Title = {Pragmatic factors in image description: the case of negations},
	Year = {2016}}
```

## The raw data
We annotated image descriptions from the Flickr30K dataset. The relevant files can
be found in the Flickr30k folder. The relevant citations for this data are:

* [Flickr30K] Peter Young, Alice Lai, Micah Hodosh and Julia Hockenmaier. From image descriptions to visual denotations: New similarity metrics for semantic inference over event descriptions, Transactions of the Association for Computational Linguistics, 2(Feb):67-78, 2014.
* [Flickr30K Entities] Bryan A. Plummer, Liwei Wang, Chris M. Cervantes, Juan C. Caicedo, Julia Hockenmaier, and Svetlana Lazebnik, Flickr30k Entities: Collecting Region-to-Phrase Correspondences for Richer Image-to-Sentence Models, ICCV, 2015.

## Processing the data
We processed the data using `negation_finder_flickr30k.py`, which creates the `captions_flickr30k.txt` file.
If you want to do any annotation on the same sentences, but require the document IDs,
please see `flickr30K_negations.tsv`, which is produced using `./negation_tsv_maker.py`.

## Annotation tool requirements
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
