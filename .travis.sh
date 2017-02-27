#! /bin/sh

# test tool

python3 akerun-sum.py -i test/input-utf8.csv -o output.csv -d 201610
diff output.csv test/output-utf8.csv > log.csv
if [ $? -ne 0 ]; then
  echo err when use input-utf8.csv
  exit $?;
else
  rm log.csv
fi
  
python3 akerun-sum.py -i test/input-sjis.csv -o output.csv -d 201610
diff output.csv test/output-sjis.csv > log.csv
if [ $? -ne 0 ]; then
  echo err when use input-sjis.csv
  exit $?;
else
  rm log.csv
fi

python3 akerun-sum.py -i test/input-euc.csv -o output.csv -d 201610
diff output.csv test/output-euc.csv > log.csv
if [ $? -ne 0 ]; then
  echo err when use input-euc.csv
  exit $?;
else
  rm log.csv
fi
