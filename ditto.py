#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import subprocess
import time

str_counter = 0
uniq_host_info = set()
source = ('ditto_data.csv',
          'ditto_data2.csv')

# Circle for reading all files
for element in source:
    file = pd.read_csv(element, sep=';')

    # Circle for reading all rows in our files
    for row in file.iterrows():

        # Circle for reading data without columns
        for element in row:

            if type(element) is pd.core.series.Series:  # not numpy.int64
                data_row = str(element.tolist())

                # Circle for reading words
                for word in data_row.split(','):
                    if 'http' in word:  # parsing
                        # print word  # http://ditto:80/service
                        word = word.split('/')

                        try:
                            word = word[2]  # ditto:80
                        except IndexError:
                            continue

                        if ':' in word:  # if we have hostport
                            uniq_host_info.add(word)

uniq_host_info = list(uniq_host_info)

# Circle for determine ip
for host_info in uniq_host_info:
    host_info = host_info.split(':')
    hostname = host_info[0]  # take hostname
    time.sleep(1)  # sleep for reduce network load
    process = subprocess.Popen(["nslookup", hostname], stdout=subprocess.PIPE)
    output = process.communicate()[0].split('\n')
    ip_arr = []
          
    for data in output:
        if 'Address' in data:
            ip_arr.append(data.replace('Address: ', ''))   # 127.0.0.1
    ip_arr.pop(0)

    for ip in ip_arr:
        str_counter += 1
        port = str(host_info[1])
        ip_port_host = ip + ':' + port + '/' + hostname
        print ip_port_host  # 127.0.0.1:8080/totoro

print str_counter
