# coding: utf-8

from bluepy import btle
from switchbot import ScanDelegate
from datetime import datetime as dt

import os
import csv

CSV_HEADER = 'Date,temperature,humidity\n'

def get_sensor_data(macaddr):
    scanner = btle.Scanner().withDelegate(ScanDelegate(macaddr))
    scanner.scan(5.0)

    return scanner.delegate.value


def main():
    macaddr = os.environ.get('SWITCHBOT_MACADDR')
    csvdir = os.environ.get('SWITCHBOT_CSV_DIR')

    sensor_data = get_sensor_data(macaddr)
    if sensor_data['SensorType'] != 'SwitchBot':
        return

    now = dt.now()
    csvpath = f"{csvdir}/{now.strftime('%Y%m')}.csv"
    if not os.path.isfile(csvpath):
        with open(csvpath, mode='w') as f:
            f.write(CSV_HEADER)

    new_data = [
        now.strftime('%Y%m%d%H%M'),
        sensor_data['Temperature'],
        sensor_data['Humidity'],
    ]

    # return if got values is the same as the last data
    with open(csvpath, mode='r') as f:
        reader = csv.reader(f)
        last_data = [row for row in reader][-1]

        if last_data[1] == str(new_data[1]) and last_data[2] == str(new_data[2]):
            return

    # write to log file
    with open(csvpath, mode='a') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(new_data)


if __name__ == '__main__':
    main()
