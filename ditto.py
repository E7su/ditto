import subprocess
import time

for rows in open('ditto.txt'):
    rows = rows.split(':')
    hostname = rows[0]
    time.sleep(1)
    process = subprocess.Popen(["nslookup", hostname], stdout=subprocess.PIPE)
    output = process.communicate()[0].split('\n')
    ip_arr = []
    for data in output:
        if 'Address' in data:
            ip_arr.append(data.replace('Address: ', ''))
    ip_arr.pop(0)
    for i in ip_arr:
        port = rows[1]
        port = port[:-1]
        port = str(port)
        f = i + ':' + port + '/' + rows[0]
        print f  # 127.0.0.1:8080/ditto
