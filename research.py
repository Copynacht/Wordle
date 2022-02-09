wList = list()
alp = [0] * 26
first = [0] * 26
second = [0] * 26
third = [0] * 26
fourth = [0] * 26
fifth = [0] * 26
f = open("wlist.txt", "r")
wList = f.readlines()

for m in range(len(wList)):
    wList[m] = wList[m].replace('\n', '')
    for n in range(len(wList[m])):
        if 97<=ord(wList[m][n]) and ord(wList[m][n])<=122:
            alp[ord(wList[m][n])-97] = alp[ord(wList[m][n])-97] + 1
            if n==0:
                first[ord(wList[m][n])-97] = first[ord(wList[m][n])-97] + 1
            if n==1:
                second[ord(wList[m][n])-97] = second[ord(wList[m][n])-97] + 1
            if n==2:
                third[ord(wList[m][n])-97] = third[ord(wList[m][n])-97] + 1            
            if n==3:    
                fourth[ord(wList[m][n])-97] = fourth[ord(wList[m][n])-97] + 1            
            if n==4:
                fifth[ord(wList[m][n])-97] = fifth[ord(wList[m][n])-97] + 1
        
with open('all.csv', 'w') as f:
    for n in range(len(alp)):
        f.write('"alp":"' + chr(n+97) + '",sum:' + str(alp[n]) + ',\n')
with open('first.csv', 'w') as f:
    for n in range(len(alp)):
        f.write('"alp":"' + chr(n+97) + '",sum:' + str(first[n]) + ',\n')
with open('second.csv', 'w') as f:
    for n in range(len(alp)):
        f.write('"alp":"' + chr(n+97) + '",sum:' + str(second[n]) + ',\n')
with open('third.csv', 'w') as f:
    for n in range(len(alp)):
        f.write('"alp":"' + chr(n+97) + '",sum:' + str(third[n]) + ',\n')
with open('fourth.csv', 'w') as f:
    for n in range(len(alp)):
        f.write('"alp":"' + chr(n+97) + '",sum:' + str(fourth[n]) + ',\n')
with open('fifth.csv', 'w') as f:
    for n in range(len(alp)):
        f.write('"alp":"' + chr(n+97) + '",sum:' + str(fifth[n]) + ',\n')
