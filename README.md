# Crossling-AMR-Eval

This is the code and data for the forthcoming paper:
Shira Wein, Nathan Schneider (2022). Accounting for Language Effect in the Evaluation of Cross-lingual AMR Parsers. To appear in The Proceedings of the 29th International Conference on Computational Linguistics (COLING).

You will need to have scipy (pip install scipy) installed. You will also need to have tensorflow (pip install "tensorflow>=2.0.0"), tensorflow-hub (pip install --upgrade tensorflow-hub), and tensorflow_text (pip install tensorflow_text).

# Contents:
(1) Folder to run XS2match

(2) File to run XSmatch

(3) Folder to run XSemBleu

# Running XS2match with LaBSE

Our XS2match code adpats the S2match code at https://github.com/flipz357/amr-metric-suite

To run the XS2match code:

cd s2match

chmod +x x_evaluation-fixed-s2match.sh

./x_evaluation-fixed-s2match.sh ../[output-amr].txt ../[reference-amr].txt

# Running XSmatch

Our XSmatch code is primarily adapted from https://github.com/snowblink14/smatch

To run the XSmatch code:

python xsmatch.py -f [output-amr].txt [reference-amr].txt

You will need to run this code in an environment that has EasyNMT installed.

# Running XSemBleu

To produce XSemBleu, we adapt the SemBleu code from https://github.com/freesunshine0316/sembleu/blob/master/README.md

To run the XSemBleu code:

cd sembleu-master

chmod a+x eval.sh

./eval.sh [output-amr].txt [reference-amr].txt

You should have a single AMR in each file.

# Troubleshooting LaBSE
Occasionally an error arises after using the LaBSE script with Mac for a few days. In our experience this is because the downloaded model is saved in a temporary folder that isn't being properly accessed. This error can be resovled by deleting the temporary folder. Access the temporary folder by entering "open $TMPDIR" into the command line on your machine and deleting the folder starting with "Tfhub."

# Contact

For any questions or information you can contact Shira Wein at sw1158@georgetown.edu.
