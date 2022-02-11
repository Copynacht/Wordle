import numpy as np

oWords = list()  # 元本
words = list()
nonWords = list()
data = np.zeros((26, 11), dtype=np.int16)

weightingData = np.zeros((5))

files = ["first.csv", "second.csv", "third.csv", "fourth.csv", "fifth.csv"]
weighting = np.zeros((5, 3))
weighting2 = np.zeros((5, 2))
kingN = 0
kingN2 = 0
which = 0
answer = ''
# 一つ目のweightは不明、二つ目は一致、三つ目は含まれる
weighting = [[1, 7, 1], [1, 1, 5], [7, 3, 3], [1, 1, 1], [1, 1, 1]]
weighting2 = [[11, 5], [1, 0], [1, 0], [1, 1], [1, 0]]


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
        data[a][d] = int(work[2])


# inputに対してdataを操作する関数
def ManipulateData(inp):
    global data
    # inpは辞書型の要素５個の配列、{'alphabet':'a','judgement',2}
    # 0は不明、1～5は一致、11~15は含まれている、10は含まれていない
    for i in range(len(inp)):
        if 97 <= ord(inp[i]["alphabet"]) and ord(inp[i]["alphabet"]) <= 122:
            # [5]が0の場合は不明、1の場合は含まれている、2の場合は確定、10の場合は含まれていない
            # 位置確定
            if 1 <= inp[i]["judgement"] and inp[i]["judgement"] <= 5:
                data[ord(inp[i]["alphabet"])-97][5] = 1
                data[ord(inp[i]["alphabet"])-97][5+inp[i]["judgement"]] = 1
            # 含まれている
            if 11 <= inp[i]["judgement"] and inp[i]["judgement"] <= 15:
                data[ord(inp[i]["alphabet"])-97][5] = 1
                data[ord(inp[i]["alphabet"])-97][inp[i]["judgement"]-5] = 10
            # 含まれていない(重複がない場合の可能性もある)
            if inp[i]["judgement"] == 10:
                chk = 0
                for n in range(5):
                    if data[ord(inp[i]["alphabet"])-97][6+n] != 1:
                        data[ord(inp[i]["alphabet"])-97][6+n] = 10
                    else:
                        chk = 1
                if chk == 0:
                    data[ord(inp[i]["alphabet"])-97][5] = 10
                else:
                    data[ord(inp[i]["alphabet"])-97][5] = 2


# 次のwordをdataより解析
def NextWordAnalyzer(to):
    global words, data, kingN, kingN2, which
    king = 0
    king2 = 0
    kingN = 0
    kingN2 = 0
    which = 0
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
            if data[a][5] == 1:
                if chr(a+97) not in words[w]:
                    r = 0
                    break
                for n in range(5):
                    if data[a][6+n] == 1 and words[w][n] != chr(a+97):
                        r = 0
                    if data[a][6+n] == 10 and words[w][n] == chr(a+97):
                        r = 0
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
        if r == 0:
            nonWords.append(words[w])
    for nw in range(len(nonWords)):
        count2 = 0
        for m in range(5):
            if data[ord(nonWords[nw][m])-97][5] == 0:
                count2 += data[ord(nonWords[nw][m])-97][m]*weighting[to-2][0]
            if data[ord(nonWords[nw][m])-97][5] == 1:
                count2 += data[ord(nonWords[nw][m])-97][m]*weighting[to-2][1]
            if data[ord(nonWords[nw][m])-97][5] == 2:
                count2 += data[ord(nonWords[nw][m])-97][m]*weighting[to-2][2]
        if count2 > king2:
            king2 = count2
            kingN2 = nw
    if king*weighting2[to-2][0] < king2*weighting2[to-2][1]:
        which = 1
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
                if m == n:
                    r[m] = 1+m
                else:
                    if not (1 <= r[m] and r[m] <= 5):
                        r[m] = 11+m
        if chk == 0:
            r[m] = 10
    for m in range(5):
        for n in range(5-m):
            if inp[m] == inp[m+n]:
                cnt = 0
                cnt2 = 0
                for o in range(5):
                    if answer[o] == inp[m]:
                        cnt += 1
                    if inp[o] == inp[m]:
                        if (1 <= r[o] and r[o] <= 5) or (11 <= r[o] and r[o] <= 15):
                            cnt2 += 1
                if cnt >= cnt2:
                    break
                if r[m] == m+1 and r[m+n] == m+n+1:
                    pass
                elif r[m] == m+1:
                    r[m+n] = 10
                elif r[m+n] == m+n+1:
                    r[m] = 10
    for m in range(5):
        ret.append({"alphabet": inp[m], "judgement": r[m]})
    return ret


for f in range(4):
    kingx = 0
    kingxyz = 100
    for x in range(5):
        weighting2[f][0] = 2*x+1
        count = 0
        for m in range(100):
            words = list()
            words.extend(oWords)
            nonWords = list()
            data[:, 5:11].fill(0)
            answer = oWords[2000+m]
            ans = 'arise'
            chk = 0
            print('f:' +str(f) + 'x:' + str(x) + 'm:' + str(m))
            for test in range(5):
                if len(words) == 1:
                    count+=test+1
                    chk = 1
                    break
                ManipulateData(Answer(ans))
                NextWordAnalyzer(test+2)
                if which == 0:
                    ans = words[kingN]
                else:
                    ans = nonWords[kingN2]
            if chk == 0:
                count += 10
        if (count/100) < kingxyz:
            kingxyz = count/100
            kingx = x
        weightingData[x] = (count/100)
    weighting2[f][0] = 2*kingx+1
    np.save(str(f)+'2.npy', weightingData)
print(weighting2)
