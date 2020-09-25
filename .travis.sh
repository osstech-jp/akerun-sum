#! /bin/bash

# test tool

diff_outputfile() {
  outfile=$1
  orgfile=$2
  inputfile=$3
  errmasage="err when used [$3] and [$2]"
  diff $outfile $orgfile > log
  if [ $? -ne 0 ]; then
    echo $errmasage
    exit $?;
  else
    rm log
  fi
}

init() {
  python3 -m venv ${VENV}
  ./${VENV}/bin/python -m pip install -U pip setuptools wheel
  ./${VENV}/bin/python -m pip install .
}

init

python3 akerun_sum.py -i test/input-utf8.csv -o output.csv -d 201610 -f 1 || exit $?
diff_outputfile output.csv test/output-utf8.csv test/input-utf8.csv

python3 akerun_sum.py -i test/input-sjis.csv -o output.csv -d 201610 -f 1 || exit $?
diff_outputfile output.csv test/output-sjis.csv test/input-sjis.csv

python3 akerun_sum.py -i test/input-euc.csv -o output.csv -d 201610 -f 1 || exit $?
diff_outputfile output.csv test/output-euc.csv test/input-euc.csv

python3 akerun_sum.py -i test/input-anotherdate.csv -o output.csv -d 201702 -f 1 || exit $?
diff_outputfile output.csv test/output-anotherdate.csv test/input-anotherdate.csv

python3 akerun_sum.py -i test/input-anotherdate.csv -o output.csv -d 201703 -f 1 || exit $?
diff_outputfile output.csv test/output-empty.csv test/input-anotherdate.csv

python3 akerun_sum.py -i test/input-anotherformat.csv -o output.csv -d 201610 -f 0 || exit $?
diff_outputfile output.csv test/output-anotherformat.csv test/input-anotherformat.csv

python3 akerun_sum.py -i test/input-anotherformat.csv -o output.csv -d 201610 || exit $?
diff_outputfile output.csv test/output-anotherformat.csv test/input-anotherformat.csv

echo "Success!!"
