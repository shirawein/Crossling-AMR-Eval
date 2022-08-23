# Crossling-AMR-Eval

# Contents:
(1) Folder to run S2match with Labse embeddings
(2) Folder to run Smatch with NMT/fast_align
(3) Folder to run CrossSemBleu
(4) Code to break up one large AMR file into individual AMR files
(5) Our human judgments of similarity with sentences

# Running XS2match with Labse

To run the XS2match code:

cd xs2match

./x_evaluation-fixed-s2match.sh ../output-amr.txt ../reference-amr.txt

# Running XSmatch

To run the XSmatch code:

cd xsmatch

python smatch_nmt.py -f output-amr.txt reference-amr.txt

# Running XSemBleu

To run the XSemBleu code:

cd sembleu-master

chmod a+x eval.sh

./eval.sh [output-amr].txt [reference-amr].txt

We recommend having a single AMR in each file.

# Running external scripts:
Quick pointer on where to get Smatch results: https://github.com/snowblink14/smatch
Quick pointer on where to get SemBleu results: https://github.com/freesunshine0316/sembleu/blob/master/README.md
Quick pointer on where to get multilingual BERTscore results: https://github.com/Tiiiger/bert_score

# Trouble-shooting Labse
Occasionally an error arises after using the Labse script with Mac for a few days. In our experience this is because the downloaded model is saved in a temporary folder that isn't being properly accessed. This error can be resovled by deleting the temporary folder. Access the temporary folder by entering "open $TMPDIR" into the command line on your machine and deleting the folder starting with "Tfhub."
