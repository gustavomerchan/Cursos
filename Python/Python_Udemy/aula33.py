from time import sleep
count = 0
while count < 10:
    count += 1
    
    if count == 3:
        print('3 e um numero especial')
        continue

    if count == 6:
        print('6 tambem e especial')
        continue

    if count == 9:
        print('9 e o mais especial de todos')
        continue
    print(count)
    sleep(0.5)