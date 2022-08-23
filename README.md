# Crossling-AMR-Eval

# Contents:
(1) Folder to run XS2match

(2) File to run XSmatch

(3) Folder to run XSemBleu

(4) Our human judgments of similarity with sentences

# Running XS2match with Labse

To run the XS2match code:

cd xs2match

./x_evaluation-fixed-s2match.sh ../[output-amr].txt ../[reference-amr].txt

# Running XSmatch

To run the XSmatch code:

python xsmatch.py -f [output-amr].txt [reference-amr].txt

You will need to run this code in an environment that has EasyNMT installed.

# Running XSemBleu

To run the XSemBleu code:

cd sembleu-master

chmod a+x eval.sh

./eval.sh [output-amr].txt [reference-amr].txt

We recommend having a single AMR in each file.

# Code references:

Smatch results: https://github.com/snowblink14/smatch

SemBleu results: https://github.com/freesunshine0316/sembleu/blob/master/README.md

S2match: https://github.com/flipz357/amr-metric-suite


# Trouble-shooting Labse
Occasionally an error arises after using the Labse script with Mac for a few days. In our experience this is because the downloaded model is saved in a temporary folder that isn't being properly accessed. This error can be resovled by deleting the temporary folder. Access the temporary folder by entering "open $TMPDIR" into the command line on your machine and deleting the folder starting with "Tfhub."
