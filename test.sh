#! /bin/bash

# test tool

VENV=testenv
PYTHON3=python3
SCRIPT=./${VENV}/bin/akerun-sum

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
    echo "$inputfile Success"
    rm log
    rm ${outfile}
  fi
}

empty_outputfile() {
  outfile=$1
  inputfile=$2
  errmasage="err when used [${inputfile}]"
  if [ -e ${outfile} ]; then
    echo ${errmessage}
    exit 1
  else
    echo "$inputfile Success"
  fi
}

init() {
  python3 -m venv ${VENV}
  ./${VENV}/bin/python -m pip install -U pip setuptools wheel
  ./${VENV}/bin/python -m pip install .
}

init

${SCRIPT} -i test/input-utf8.csv -o output.csv -d 201610 -f 1 || exit $?
diff_outputfile output.csv test/output-utf8.csv test/input-utf8.csv

${SCRIPT} -i test/input-sjis.csv -o output.csv -d 201610 -f 1 || exit $?
diff_outputfile output.csv test/output-sjis.csv test/input-sjis.csv

${SCRIPT} -i test/input-euc.csv -o output.csv -d 201610 -f 1 || exit $?
diff_outputfile output.csv test/output-euc.csv test/input-euc.csv

${SCRIPT} -i test/input-anotherdate.csv -o output.csv -d 201702 -f 1 || exit $?
diff_outputfile output.csv test/output-anotherdate.csv test/input-anotherdate.csv

${SCRIPT} -i test/input-anotherdate.csv -o output-empty.csv -d 201703 -f 1 || exit $?
empty_outputfile output.csv test/input-anotherdate.csv

${SCRIPT} -i test/input-anotherformat.csv -o output.csv -d 201610 -f 0 || exit $?
diff_outputfile output.csv test/output-anotherformat.csv test/input-anotherformat.csv

${SCRIPT} -i test/input-anotherformat.csv -o output.csv -d 201610 || exit $?
diff_outputfile output.csv test/output-anotherformat.csv test/input-anotherformat.csv

rm -f output.csv
rm -r ${VENV}
