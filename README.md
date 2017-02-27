[![Build Status](https://travis-ci.org/osstech-jp/akerun-sum.svg?branch=master)](https://travis-ci.org/osstech-jp/akerun-sum)

### 入退出集計プログラム

### 以下の環境で動作確認
  - Windows 10 Home, Python 3.4.3
  - Ubuntu 16.04.2 LTS, Python 3.5.2

### 実行例

  ```
  akerun-sum.py -i input-euc.csv -o output-euc.csv -d 201610
  akerun-sum.py -i input-utf8.csv -o output-utf8.csv -d 201610
  akerun-sum.py -i input-sjis.csv -o output-sjis.csv -d 201610
  ```

社員数やレコードの数はリストで管理しているため無制限

[2017/2/14]
入力ファイルの文字コードを識別し、
出力ファイルは入力ファイルと同じ文字コードで出力するようにしました。

上記環境でUTF-8、EUC-JP、Shift_JISの文字コードで作成した入力ファイルに対し、
それぞれ対応した文字コードでの出力を確認。

改行コードはPythonの os.linesep を使用し、
実行環境に応じた改行コードを指定しています。
