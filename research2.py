first = list()
second = list()
third = list()
fourth = list()
fifth = list()
king = 0
kingN=0

files = ["first.csv","second.csv","third.csv","fourth.csv","fifth.csv"]

for d in range(5):
    f = open(files[d], "r")
    read = f.readlines()
    for a in range(26):
        work = read[a].split(',')
        if d==0:
            first.append({'alp' : work[0], 'rank': int(work[2].replace('\n', ''))})
        if d==1:
            second.append({'alp' : work[0], 'rank': int(work[2].replace('\n', ''))})
        if d==2:
            third.append({'alp' : work[0], 'rank': int(work[2].replace('\n', ''))})
        if d==3:
            fourth.append({'alp' : work[0], 'rank': int(work[2].replace('\n', ''))})
        if d==4:
            fifth.append({'alp' : work[0], 'rank': int(work[2].replace('\n', ''))})

f = open("wlist.txt", "r")
wList = f.readlines()

for m in range(len(wList)):
    score = 0
    for n in range(5):
        if 97<=ord(wList[m][n]) and ord(wList[m][n])<=122:
            if n==0:
                score+=26-first[ord(wList[m][n])-97]["rank"]
            if n==1:
                score+=26-second[ord(wList[m][n])-97]["rank"]
            if n==2:
                score+=26-third[ord(wList[m][n])-97]["rank"]
            if n==3:
                score+=26-fourth[ord(wList[m][n])-97]["rank"]
            if n==4:
                score+=26-fifth[ord(wList[m][n])-97]["rank"]
    if score>king:
        king=score
        kingN = m
    if score==122:
        print(wList[m])
print(king)
print(wList[kingN])
