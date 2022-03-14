import numpy as np

oWords = list() #元本
words = list()
data = np.zeros((26, 11), dtype=np.int16)

weightingData = np.zeros((5, 5, 5))

files = ["first.csv", "second.csv", "third.csv", "fourth.csv", "fifth.csv"]
weighting = np.zeros((5, 3))
kingN = 0
answer = ''
# 一つ目のweightは不明、二つ目は一致、三つ目は含まれる
weighting = [[5, 5, 5], [5, 5, 5], [5, 5, 5], [5, 5, 5], [5, 5, 5]]

# wordsの初期化
f = open("wlist.txt", "r")
wList = f.readlines()
for w in range(len(wList)):
    oWords.append(wList[w].replace('\n', ''))


# dataの初期化
for d in range(5):
    f = open(files[d], "r")
    read = f.readlines()
    for a in range(26):
        work = read[a].split(',')
        data[a][d] = int(work[1])
        

# inputに対してdataを操作する関数
def ManipulateData(inp):
    global data
    # inpは辞書型の要素５個の配列、{'alphabet':'a','judgement',2}
    for gob in range(2):
        for i in range(len(inp)):
            # 0は不明、1～5は一致、11~15は含まれている、10は含まれていない
            # [5]が0の場合は不明、1の場合は含まれている、2の場合は確定、10の場合は含まれていない
            if gob == 0:  # goのみ検索
                # 場所特定
                if 1 <= inp[i]["judgement"] and inp[i]["judgement"] <= 5:
                    data[ord(inp[i]["alphabet"])-97][5] = 1
                    data[ord(inp[i]["alphabet"])-97][5+inp[i]["judgement"]] = 1
                # 含まれている
                if 11 <= inp[i]["judgement"] and inp[i]["judgement"] <= 15:
                    data[ord(inp[i]["alphabet"])-97][5] = 1
                    data[ord(inp[i]["alphabet"])-97][inp[i]
                                                     ["judgement"]-5] = 10
            if gob == 1:
                # 含まれていない(重複がない場合の可能性もある)
                if inp[i]["judgement"] == 10:
                    chk = 0
                    if data[ord(inp[i]["alphabet"])-97][5] == 1:
                        for n in range(5):
                            if data[ord(inp[i]["alphabet"])-97][6+n] == 1:
                                chk = 1
                        if chk == 1:
                            data[ord(inp[i]["alphabet"])-97][5] = 2
                        else:
                            data[ord(inp[i]["alphabet"])-97][6+i] = 10
                    elif data[ord(inp[i]["alphabet"])-97][5] == 0:
                        data[ord(inp[i]["alphabet"])-97][5] = 10


# 次のwordをdataより解析
def NextWordAnalyzer(to):
    global words, data, kingN
    king = 0
    kingN = 0
    newWords = list()
    for w in range(len(words)):
        r = 1
        for n in range(5):
            if 97 <= ord(words[w][n]) and ord(words[w][n]) <= 122:
                # wordにまだ可能性があるか判定
                if data[ord(words[w][n])-97][5] == 10:
                    r = 0
                    break
            else:
                r = 0
        for a in range(26):
            if data[a][5]==1:
                if chr(a+97) not in words[w]:
                    r=0
                    break
                for n in range(5):
                    if data[a][6+n]==1 and words[w][n]!=chr(a+97):
                            r=0
                    if data[a][6+n]==10 and words[w][n]==chr(a+97):
                            r=0
        if r == 1:
            newWords.append(words[w])
            count = 0
            for m in range(5):
                if data[ord(words[w][m])-97][5] == 0:
                    count += data[ord(words[w][m])-97][m]*weighting[to-2][0]
                if data[ord(words[w][m])-97][5] == 1:
                    count += data[ord(words[w][m])-97][m]*weighting[to-2][1]
                if data[ord(words[w][m])-97][5] == 2:
                    count += data[ord(words[w][m])-97][m]*weighting[to-2][2]
            if count > king:
                king = count
                kingN = len(newWords)-1
    words = list()
    words.extend(newWords)


# 返答を作成
def Answer(inp):
    global answer
    r = [0]*5
    ret = list()
    for m in range(5):
        chk = 0
        for n in range(5):
            if inp[m] == answer[n]:
                chk = 1
                if m==n:
                    r[m]=1+m
                else:
                    if not (1<=r[m] and r[m]<=5):
                        r[m]=11+m
        if chk==0:
            r[m]=10
    for m in range(5):
        for n in range(5-m):
            if inp[m] == inp[m+n]:
                cnt=0
                cnt2=0
                for o in range(5):
                    if answer[o]==inp[m]:
                        cnt+=1
                    if inp[o]==inp[m]:
                        if (1<=r[o] and r[o]<=5) or (11<=r[o] and r[o]<=15):
                            cnt2+=1
                if cnt>=cnt2:
                    break
                if r[m] == m+1 and r[m+n] == m+n+1:
                    pass
                elif r[m] == m+1:
                    r[m+n]=10
                elif r[m+n] == m+n+1:
                    r[m]=10
    for m in range(5):
        ret.append({"alphabet":inp[m], "judgement": r[m]})
    return ret

for f in range(5):
    kingx = 0
    kingy = 0
    kingz = 0
    kingxyz=100
    for x in range(5):
        for y in range(5):
            for z in range(5):
                weighting[f][0]=2*x+1
                weighting[f][1]=2*y+1
                weighting[f][2]=2*z+1
                count=0
                for m in range(200):
                    words = list()
                    words.extend(oWords)
                    data[:,5:11].fill(0)
                    answer = oWords[1000+m]
                    print(answer)
                    ans='later'
                    chk=0
                    print('f:' + str(f) + 'x:' + str(x) +'y:' + str(y) +'z:' + str(z) +'m:' + str(m))
                    for test in range(5):
                        if len(words)==1:
                            count+=test+1
                            chk=1
                            break
                        ManipulateData(Answer(ans))
                        NextWordAnalyzer(test+2)
                        ans=words[kingN]
                    if chk==0:
                        count+=10
                if (count/100)<kingxyz:
                    kingxyz=count/100
                    kingx = x
                    kingy = y
                    kingz = z
                weightingData[x][y][z]=(count/200)
    weighting[f][0]=2*kingx+1
    weighting[f][1]=2*kingy+1
    weighting[f][2]=2*kingz+1
    np.save(str(f) +'.npy', weightingData)
print(weighting)