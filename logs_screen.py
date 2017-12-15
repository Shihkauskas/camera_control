import time
import os

while True:
    with open('Full_log.log', 'r') as file:
        print('\n')
        for line in file:
            print(line)
    time.sleep(600)
    os.system('clear')
