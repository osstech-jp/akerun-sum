#! /bin/bash

# test tool

diff_outputfile() {
  outfile = $1
  orgfile = $2
  errmasage = "err when use $1"
  diff $outfile $orgfile > log.csv
  if [ $? -ne 0 ]; then
    echo $errmasage
    exit $?;
  else
    rm log.csv
  fi
}
python3 akerun-sum.py -i test/input-utf8.csv -o output.csv -d 201610
diff_outputfile output.csv test/output-utf8.csv

python3 akerun-sum.py -i test/input-sjis.csv -o output.csv -d 201610
diff_outputfile output.csv test/output-sjis.csv

python3 akerun-sum.py -i test/input-euc.csv -o output.csv -d 201610
diff_outputfile output.csv test/output-euc.csv

