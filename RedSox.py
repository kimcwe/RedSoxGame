import requests
from bs4 import BeautifulSoup as BS
import webbrowser
import datetime

def findMonthName(num):
    dict = {
        '1':'Jan', '2':'Feb', '3':'Mar',
        '4':'Apr', '5':'May', '6':'Jun',
        '7':'Jul', '8':'Aug', '9':'Sep',
        '10':'Oct', '11':'Nov', '12':'Dec'
    }
    return dict.get(str(num))

def findMatchupName(ref):
    cpy = ref[:]
    end = ref.index("href")
    beg = 0
    while(ref[end] != "<"):
        end += 1
    while(ref[beg] != ">"):
        beg += 1
    cpy = ref[beg:end]
    while(cpy[beg] != ">"):
        beg += 1
    return cpy[beg+1:end]
    
def findGameTime(ref):
    beg = ref.index(">")+1
    end = beg
    cpy = ref[beg:]
    while(cpy[beg] == " " or cpy[beg] == "\n"):
        beg += 1
    while(cpy[end] != "|"):
        end += 1
    cpy[beg:end].strip('\t')
    cpy[beg:end].strip('\n')
    return cpy[beg:end]

def findGame():
    time = datetime.datetime.now()
    print("Today's date: %s/%s/%s" % (time.month, time.day, time.year) )
    dateFormat = str(findMonthName(time.month)) + ' ' + str(time.day)

    url = "https://www.cbssports.com/mlb/teams/BOS/boston-red-sox/"
    urlInfo = requests.get(url)
    soup = BS(urlInfo.content, 'html.parser')
    nextGame = str(soup.find_all("div", "TeamMatchup-date"))
    isHome = str(soup.find_all("div", "TeamMatchup-vsInfo"))
    matchup = str(soup.find_all("span", "TeamName"))

    if(dateFormat in nextGame):
        gametime = findGameTime(nextGame)
        matchup = str(findMatchupName(matchup))
        if("@" not in isHome):
            print("\nThere is a game today! FML!:")
            print("\tRed Sox vs " + matchup)
        else:
            print("\nThere is a game, but it is away:")
            print("\tRed Sox @ " + matchup)
        print("\t" + gametime)
        webbrowser.open(url)
    else:
        print("\nNo Red Sox game today! MBTA is safe owo")

findGame()