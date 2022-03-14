from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome import service
from selenium.webdriver.common.by import By
import numpy as np, time

words = list()
nonWords = list()
data = np.zeros((26, 11), dtype=np.int16)

files = ["first.csv", "second.csv", "third.csv", "fourth.csv", "fifth.csv"]
weighting = np.zeros((5, 3))
weighting2 = np.zeros((5, 2))
kingN, kingN2, which = 0, 0, 0
# 一つ目のweightは不明、二つ目は一致、三つ目は含まれる
weighting = [[9, 7, 1], [5, 7, 3], [3, 9, 1], [1, 1, 1], [1, 1, 1]]
weighting2 = [[7, 5], [9, 5], [7, 5], [1, 5], [1, 0]]
ans = 'later'


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
        data[a][d] = int(work[1])


# wordleに入力
def keyboard_input(b, word):
    for n in range(5):
        time.sleep(0.1)
        if keyboard.index(word[n])>=19:
            b[keyboard.index(word[n])+1].click()
        else:
            b[keyboard.index(word[n])].click()
    b[19].click()


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


# 可能性の残っているwordをdataより解析
def NextWordAnalyzer(to):
    global words, data, kingN, kingN2, which
    king, king2, kingN, kingN2, which = 0, 0, 0, 0, 0
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


def inputManip():
    ret = list()
    inp = ''
    # bgoob  #bはblack,gはgreen,oはorange
    for n in range(5):
        if gt[n].get_attribute('evaluation') == 'absent': #b
            inp+='b'
        if gt[n].get_attribute('evaluation') == 'present': #o
            inp+='o'
        if gt[n].get_attribute('evaluation') == 'correct': #g
            inp+='g'
    for n in range(5):
        if inp[n] == 'g':
            ret.append({"alphabet": ans[n], "judgement": n+1})
        elif inp[n] == 'o':
            ret.append({"alphabet": ans[n], "judgement": n+11})
        elif inp[n] == 'b':
            ret.append({"alphabet": ans[n], "judgement": 10})
    return ret


CHROMEDRIVER = "C:/chromedriver_win32/chromedriver.exe"
keyboard = 'qwertyuiopasdfghjklzxcvbnm'
 
# ドライバー指定でChromeブラウザを開く
chrome_service = service.Service(executable_path=CHROMEDRIVER)
driver = webdriver.Chrome(service=chrome_service)
actions = ActionChains(driver)

#driver.get("https://web.archive.org/web/20211227150528/https://www.powerlanguage.co.uk/wordle/")
#driver.get("https://web.archive.org/web/20220101000801/https://www.powerlanguage.co.uk/wordle/")
#driver.get("https://web.archive.org/web/20211230172040/https://www.powerlanguage.co.uk/wordle/")
driver.get("https://www.nytimes.com/games/wordle/index.html")
ga = driver.find_element(By.TAG_NAME, 'game-app').shadow_root
gm = ga.find_element(By.TAG_NAME, 'game-modal').shadow_root
gm.find_element(By.TAG_NAME, 'game-icon').click()

gk = ga.find_element(By.TAG_NAME, 'game-keyboard').shadow_root
b = gk.find_elements(By.TAG_NAME, 'button')

gr = ga.find_elements(By.TAG_NAME, 'game-row')

# 実行
for n in range(6):    
    print(ans)
    keyboard_input(b, ans)
    time.sleep(1.5)
    gt = gr[n].shadow_root.find_elements(By.TAG_NAME, 'game-tile')
    ManipulateData(inputManip())
    NextWordAnalyzer(n+2)
    ans = words[kingN]
    if which == 0:
        ans = words[kingN]
    else:
        ans = nonWords[kingN2]
    