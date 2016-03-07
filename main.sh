# !/bin/bash
python3 main.py contact-lenses.arff
dot -Tpdf output.dot > lenses.pdf
python3 main.py waitfortable.arff
dot -Tpdf output.dot > wait.arff
