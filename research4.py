import numpy as np

words = list()
data = np.zeros((26, 6), dtype=np.int16)

files = ["first.csv", "second.csv", "third.csv", "fourth.csv", "fifth.csv"]
weighting = np.zeros((5, 3))
kingN = 0
# 一つ目のweightは不明、二つ目は一致、三つ目は含まれる
weighting = [[50, 50, 50], [50, 50, 50], [50, 50, 50], [50, 50, 50], [50, 50, 50]]
answer = 'skill'

# wordsの初期化
f = open("wlist.txt", "r")
wList = f.readlines()
for w in range(len(wList)):
    words.append(wList[w].replace('\n', ''))


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
    # 0は不明、1～5は一致、11~15は含まれている、25～35重複なし確定、10は含まれていない
    for i in range(len(inp)):
        if 97 <= ord(inp[i]["alphabet"]) and ord(inp[i]["alphabet"]) <= 122:
            if (1 <= data[ord(inp[i]["alphabet"])-97][5] and data[ord(inp[i]["alphabet"])-97][5] <= 5) and inp[i]["judgement"] == 10:
                data[ord(inp[i]["alphabet"])-97][5] += 20
            elif (11 <= data[ord(inp[i]["alphabet"])-97][5] and data[ord(inp[i]["alphabet"])-97][5] <= 15) and inp[i]["judgement"] == 10:
                data[ord(inp[i]["alphabet"])-97][5] += 10
            elif 21 <= data[ord(inp[i]["alphabet"])-97][5] and data[ord(inp[i]["alphabet"])-97][5] <= 25:
                pass
            elif (21 <= data[ord(inp[i]["alphabet"])-97][5] and data[ord(inp[i]["alphabet"])-97][5] <= 25) and inp[i]["judgement"] == 10:
                pass
            else:
                data[ord(inp[i]["alphabet"])-97][5] = inp[i]["judgement"]


# 可能性の残っているwordをdataより解析
def RemainingWords():
    global words, data
    newWords = list()
    for w in range(len(words)):
        r = 1
        for n in range(5):
            if 97 <= ord(words[w][n]) and ord(words[w][n]) <= 122:
                # wordにまだ可能性があるか判定
                if data[ord(words[w][n])-97][5] == 10 or ((21 <= data[ord(words[w][n])-97][5] and data[ord(words[w][n])-97][5] <= 25) and data[ord(words[w][n])-97][5]-20 != n+1):
                    r = 0
                    break
            else:
                r = 0
        for a in range(26):
            # wordにまだ可能性があるか判定
            if 1 <= data[a][5] and data[a][5] <= 5:
                if chr(a+97) != words[w][data[a][5]-1]:
                    r = 0
                    break
            if 11 <= data[a][5] and data[a][5] <= 15:
                if chr(a+97) == words[w][data[a][5]-11]:
                    r = 0
                    break
                s = 0
                for n in range(5):
                    if words[w][n] == chr(a+97):
                        s = 1
                if s == 0:
                    r = 0
            if 21 <= data[a][5] and data[a][5] <= 25:
                if chr(a+97) != words[w][data[a][5]-21]:
                    r = 0
                    break
        if r == 1:
            newWords.append(words[w])
    words = list()
    words.extend(newWords)


# 次に入力すべき単語の解析
def NextWordAnalyzer(n):  # n個目の入力単語解析
    global kingN, words, data
    king = 0
    kingN = 0
    for w in range(len(words)):
        count = 0
        for m in range(5):
            if data[ord(words[w][m])-97][5] == 0:
                count += data[ord(words[w][m])-97][m]*weighting[n-2][0]
            if 1 <= data[ord(words[w][m])-97][5] and data[ord(words[w][m])-97][5] <= 5:
                count += data[ord(words[w][m])-97][m]*weighting[n-2][1]
            if 11 <= data[ord(words[w][m])-97][5] and data[ord(words[w][m])-97][5] <= 15:
                count += data[ord(words[w][m])-97][m]*weighting[n-2][2]
        if count > king:
            king = count
            kingN = w

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
                if r[m] == m+1 and r[m+n] == m+n+1:
                    pass
                elif r[m] == m+1:
                    r[m+n]=10
                elif r[m+n] == m+n+1:
                    r[m]=10
    for m in range(5):
        ret.append({"alphabet":inp[m], "judgement": r[m]})
    return ret

ans='arise'
for test in range(5):
    print(ans)
    ManipulateData(Answer(ans))
    RemainingWords()
    NextWordAnalyzer(test+2)
    ans=words[kingN]
    print(len(words))
print(ans)