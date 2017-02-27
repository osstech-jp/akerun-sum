#! /bin/sh

python3 ../akerun-sum.py -i input-utf8.csv -o output.csv -d 201610
python3 ../akerun-sum.py -i input-sjis.csv -o output.csv -d 201610
python3 ../akerun-sum.py -i input-euc.csv -o output.csv -d 201610

