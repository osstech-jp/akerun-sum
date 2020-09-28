#!/usr/bin/env python3
# -*- coding: utf-8 -*- vim:shiftwidth=4:expandtab:

import click
import math
import calendar
import datetime
import codecs
import csv
import sys
import os

DAYSTART = '0300'
ROUNDDOWNTIME = 15

KEYS = {'date': '日時', 'user': 'ユーザー名', 'lock': 'アクション'}


def input_data(filename):
    lookup = ('utf_8', 'euc_jp', 'euc_jis_2004', 'euc_jisx0213',
              'shift_jis', 'shift_jis_2004', 'shift_jisx0213',
              'iso2022jp', 'iso2022_jp_1', 'iso2022_jp_2', 'iso2022_jp_3',
              'iso2022_jp_ext', 'latin_1', 'ascii')
    encode = None

    for encoding in lookup:
        try:
            f = codecs.open(filename, 'r', encoding)
            encode = encoding
            reader = csv.DictReader(f)
            data_list = [d for d in reader]
            return data_list, encode
        except:
            continue
    raise LookupError


def data_shaping(data_list, period):
    # 2:00 -> 23:00
    date_format_list = ['%Y/%m/%d %H:%M', '%Y-%m-%d %H:%M:%S']
    day_start = datetime.datetime.strptime(DAYSTART, '%H%M')
    for data in data_list:
        for date_format in date_format_list:
            try:
                data[KEYS['date']] = datetime.datetime.strptime(data[KEYS['date']], date_format)
                data[KEYS['date']] -= datetime.timedelta(hours=day_start.hour)
                data[KEYS['date']] -= datetime.timedelta(minutes=day_start.minute)
                break
            except:
                pass
    # data mining
    period_start = period
    period_str = period.strftime('%Y%m')
    day_range = calendar.monthrange(period_start.year, period_start.month)[1]
    period_end = period_start + datetime.timedelta(days=day_range)

    mining_data = []
    user_list = []
    shaped_data = []
    for data in data_list:
        if isinstance(data[KEYS['date']], str):
            continue
        if period_start <= data[KEYS['date']] and data[KEYS['date']] < period_end\
                and data[KEYS['lock']] in ['入室', '退室', '解錠']\
                and data[KEYS['user']] != '':
            mining_data.append(data)
            if data[KEYS['user']] not in user_list:
                user_list.append(data[KEYS['user']])
                shaped_data.append({
                    'name': data[KEYS['user']], 'timecard_data': [],
                    'writed_days': [], 'period': period_str})

    # data reconstruction
    for data in mining_data:
        index = user_list.index(data[KEYS['user']])

        if data[KEYS['date']].day not in shaped_data[index]['writed_days']:
            shaped_data[index]['timecard_data'].append({'day': data[KEYS['date']].day})
            shaped_data[index]['writed_days'].append(data[KEYS['date']].day)

        timecard_data_index = shaped_data[index]['writed_days'].index(data[KEYS['date']].day)

        if data[KEYS['lock']] == '入室':
            if 'in_time' not in shaped_data[index]['timecard_data'][timecard_data_index]:
                shaped_data[index]['timecard_data'][timecard_data_index]['in_time'] = data[KEYS['date']]

        elif data[KEYS['lock']] == '退室':
            shaped_data[index]['timecard_data'][timecard_data_index]['out_time'] = data[KEYS['date']]

        elif data[KEYS['lock']] == '解錠':
            if 'in_time' not in shaped_data[index]['timecard_data'][timecard_data_index]:
                shaped_data[index]['timecard_data'][timecard_data_index]['in_time'] = data[KEYS['date']]
            else:
                shaped_data[index]['timecard_data'][timecard_data_index]['out_time'] = data[KEYS['date']]

    # data totalization
    for data in shaped_data:
        total_working_hours = 0
        total_working_days = 0

        for timecard_data in data['timecard_data']:
            if 'in_time' in timecard_data\
                    and 'out_time' in timecard_data:
                diff = timecard_data['out_time'] - timecard_data['in_time']
                if diff.days < 0:
                    timecard_data['working_hours'] = 0
                else:
                    diff_sec = diff.seconds
                    diff_min = diff_sec / 60
                    diff_min = math.floor(diff_min / ROUNDDOWNTIME) * ROUNDDOWNTIME
                    diff_hour = diff_min / 60

                    timecard_data['working_hours'] = diff_hour
                total_working_hours += diff_hour

            else:
                timecard_data['working_hours'] = 0

            total_working_days += 1

        data['total_working_hours'] = total_working_hours
        data['total_working_days'] = total_working_days

    return shaped_data


def output_data0(filename, encode, shaped_data):
    # make datelist
    day_list = []
    for data in shaped_data:
        for timecard in data['timecard_data']:
            if timecard['day'] not in day_list:
                day_list.append(timecard['day'])
    day_list.sort()

    if len(shaped_data) == 0:
        click.echo("output data is empty")
        return

    period = shaped_data[0]['period']

    header = ['氏名', '就業日数', '就業時間']
    for day in day_list:
        day_str = period[0:4] + '/'\
            + str(int(period[4:6])) + '/'\
            + str(day)
        header.append(day_str + '入')
        header.append(day_str + '退')
        header.append(day_str + '時')

    with codecs.open(filename, 'w', encode) as f:
        writer = csv.writer(f, lineterminator=os.linesep)
        writer.writerow(header)
        for data in shaped_data:
            row = [data['name'], data['total_working_days'], data['total_working_hours']]
            curr_index = 0
            writedata_index = 0
            while curr_index < len(day_list):
                if writedata_index < len(data['timecard_data'])\
                        and data['timecard_data'][writedata_index]['day'] == day_list[curr_index]:
                    timecard = data['timecard_data'][writedata_index]
                    day_start = datetime.datetime.strptime(DAYSTART, '%H%M')
                    if 'in_time' in timecard:
                        # 23:00 -> 26:00
                        timecard['in_time'] += datetime.timedelta(minutes=day_start.minute)
                        timecard['in_time'] += datetime.timedelta(hours=day_start.hour)
                        hour = timecard['in_time'].hour
                        if hour < day_start.hour:
                            hour += 24

                        in_time_str = str(hour) + ':'\
                            + timecard['in_time'].strftime('%M')
                    else:
                        in_time_str = ''

                    if 'out_time' in timecard:
                        # 23:00 -> 26:00
                        timecard['out_time'] += datetime.timedelta(minutes=day_start.minute)
                        timecard['out_time'] += datetime.timedelta(hours=day_start.hour)
                        hour = timecard['out_time'].hour
                        if hour < day_start.hour:
                            hour += 24
                        out_time_str = str(hour) + ':'\
                            + timecard['out_time'].strftime('%M')
                    else:
                        out_time_str = ''

                    row.append(in_time_str)
                    row.append(out_time_str)
                    row.append(timecard['working_hours'])
                    writedata_index += 1
                else:
                    row.append('')
                    row.append('')
                    row.append('')
                curr_index += 1

            writer.writerow(row)
            row.clear()


def output_data1(filename, encode, shaped_data):
    if len(shaped_data) == 0:
        click.echo("output data is empty")
        return

    with codecs.open(filename, 'w', encode) as f:
        writer = csv.writer(f, lineterminator=os.linesep)
        for data in shaped_data:
            writer.writerow(['氏名', data['name'], '', '', '', ''])
            writer.writerow(['集計期間', data['period'], '', '', '', ''])
            writer.writerow(['就業日数', data['total_working_days'], '', '', '', ''])
            writer.writerow(['就業時間', data['total_working_hours'], '', '', '', ''])
            writer.writerow(['月日', '入室時刻', '退出時刻', '就業時間', '', ''])
            for timecard in data['timecard_data']:
                date_str = data['period'][0:4] + '/'\
                    + str(int(data['period'][4:6])) + '/'\
                    + str(timecard['day'])

                day_start = datetime.datetime.strptime(DAYSTART, '%H%M')
                if 'in_time' in timecard:
                    # 23:00 -> 26:00
                    timecard['in_time'] += datetime.timedelta(minutes=day_start.minute)
                    timecard['in_time'] += datetime.timedelta(hours=day_start.hour)
                    hour = timecard['in_time'].hour
                    if hour < day_start.hour:
                        hour += 24

                    in_time_str = str(hour) + ':'\
                        + timecard['in_time'].strftime('%M')
                else:
                    in_time_str = ''

                if 'out_time' in timecard:
                    # 23:00 -> 26:00
                    timecard['out_time'] += datetime.timedelta(minutes=day_start.minute)
                    timecard['out_time'] += datetime.timedelta(hours=day_start.hour)
                    hour = timecard['out_time'].hour
                    if hour < day_start.hour:
                        hour += 24
                    out_time_str = str(hour) + ':'\
                        + timecard['out_time'].strftime('%M')
                else:
                    out_time_str = ''

                writer.writerow([
                    date_str, in_time_str, out_time_str, str(timecard['working_hours']), '', ''])

            writer.writerow(['', '', '', '', '', ''])


@click.command()
@click.option('-i', '--input-filename', required=True, type=click.Path(exists=True))
@click.option('-o', '--output-filename', required=True, type=click.Path())
@click.option('-d', '--period', required=True, type=click.DateTime(['%Y%m']))
@click.option('-f', '--format', default='0', show_default=True, type=click.Choice(['0', '1']))
def main(input_filename, output_filename, period, format):
    commandline_vars = {
            'input_filename': input_filename,
            'output_filename': output_filename,
            'period': period,
            'format_num': int(format),
            }
    data_list, encode = input_data(commandline_vars['input_filename'])
    shaped_data = data_shaping(data_list, commandline_vars['period'])
    if commandline_vars['format_num'] == 0:
        output_data0(commandline_vars['output_filename'], encode, shaped_data)
    elif commandline_vars['format_num'] == 1:
        output_data1(commandline_vars['output_filename'], encode, shaped_data)
