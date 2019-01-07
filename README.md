[![Build Status](https://travis-ci.org/osstech-jp/akerun-sum.svg?branch=master)](https://travis-ci.org/osstech-jp/akerun-sum)

### 入退出集計プログラム
NFCカードのドアキー[アケルン](https://akerun.com/)の入退出記録から、勤務日数や勤務時間を集計するプログラムです。

### 以下の環境で動作確認
  * Windows 10 Home, Python 3.4.3
  * Ubuntu 16.04.2 LTS, Python 3.5.2

### 使用方法
`akerun-sum.py -i inputfile -o outputfile -d yyyymm [-f n]`  
##### 引数
    -i  入力ファイル名
    -o  出力ファイル名
    -d  集計期間 yyyymm の形式で指定
    -f  出力タイプ 初期値は0
        0  出力パターン1
        1  出力パターン2

### 実行例

    akerun-sum.py -i input-euc.csv -o output-euc.csv -d 201610
    akerun-sum.py -i input-anotherformat.csv -o output-anotherformat.csv -d 201610　-f 1

社員数やレコードの数はリストで管理しているため無制限


### 想定している入力ファイル
DATE,AKERUN,USER,LOCK,CLIENTのカラムを持つCSVファイル

##### DATE
日付データ  
`yyyy/mm/dd hh:mm`と`yyyy-mm-dd hh:mm:ss`の2パターンに対応  
昇順にソートされていることが前提
##### AKERUN
本プログラムでは使用していない
##### USER
社員名データ
##### LOCK
* 入室：オフィスに入った
* 退室：オフィスから出た
* 解錠：オフィスに入室したか退室のどちらか
* 施錠：鍵を締めた（本プログラムでは使用していない）

##### CLIENT
鍵の種類（本プログラムでは使用していない）

### 出力ファイル
出力ファイルは2パターンあり、引数によって切替可能  
文字コードは入力ファイルに合わせる

##### 出力パターン1
Excelファイルで開くことを想定

|氏名|就業日数|就業時間|yyyy/mm/dd入|yyyy/mm/dd退|yyyy/mm/dd時|…|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|山田太郎|2|13.5|8:47|10:12|1.25|…|
|山田次郎|2|20.5|8:47|20:12|11.25|…|
|:|:|:|:|:|:|:|

##### 出力パターン2
通常のCSVファイル

|||||
|:-:|:-:|:-:|:-:|
|氏名|山田太郎|||
|集計期間|yyyymm|||
|就業日数|2|||
|就業時間|13.5|||
|月日|入室時刻|退室時刻|就業時間|
|yyyy/mm/dd|8:47|10:12|1.25|
|:|:|:|:|
|||||
|氏名|山田次郎|||
|集計期間|yyyymm|||
|就業日数|2|||
|就業時間|13.5|||
|月日|入室時刻|退室時刻|就業時間|
|yyyy/mm/dd|8:47|20:12|11.25|
|:|:|:|:|
