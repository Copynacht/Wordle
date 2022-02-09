f = open("wlist.txt", "r")
wList = f.readlines()

king = 0
king2 = 0
kingN=0
king2N=0

for l in range(len(wList)):
    result=0
    result2=0
    for m in range(len(wList)):
        count=0
        count2=0
        for n in range(5):
            for o in range(5):
                if  wList[m][n] == wList[l][o]:
                    count+=1
                    if n==o:
                        count2+=1
                    break
        result+=count
        result2+=count2
    result/=len(wList)
    result2/=len(wList)
    if result>king:
        king=result
        kingN=l
    if result2>king2:
        king2=result2
        king2N=l


print(wList[kingN])
print(king)
print(wList[king2N])
print(king2)