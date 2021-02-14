from time import sleep

times = 0
while True:
    times += 1
    print('this is stdout', times)
    sleep(1)

input('this is stdin')