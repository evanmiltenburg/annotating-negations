# Computing the statistics

This folder contains two files: `negation_stats_coco.py` and `negation_stats_flickr30k.py`.
These files compute relevant statistics for our paper "Pragmatic factors in image description: the case of negations".
To run them, please

* Download the Flickr30K Entities dataset, and put the files with image descriptions in a folder called `Flickr30k`.
* Download the MS COCO training and validation JSON files and put them in a folder called `MSCOCO`.

And then just execute the scripts from the command line using `python negation_stats_coco.py` and `python negation_stats_flickr30k.py`.
