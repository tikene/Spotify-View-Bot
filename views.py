# Imports
import os
import json
import requests
import re
from sys import exit
import sys
from random import uniform
from random import randint
from time import sleep
from time import time
from colorama import Fore, Style, init
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys  # and Krates
from webdriver_manager.chrome import ChromeDriverManager
from multiprocessing import Process

# Color shortcuts
bright = Style.BRIGHT
red = Fore.RED + bright
green = Fore.GREEN + bright
cyan = Fore.CYAN + bright
yellow = Fore.LIGHTYELLOW_EX + bright

# Color defines
init(convert=True)
init(autoreset=True)

# Making sure the program only works in windows cuz autism
os.system("cls")
os.system("title Spotify views bot - Created by Tikene")


configPath = "SavedAccounts.json"
pauseStrings = ["Pausa", "Pause"]
loopStrings = ["Disable repeat", "Desactivar repetir"]

chromeoptions = Options()
chromeoptions.add_argument("--log-level=3")
chromeoptions.add_experimental_option('excludeSwitches', ['enable-logging'])


asciiArt = """\
   ,______________________________________
  |_________________,----------._ [____]  ""-,__  __....-----=====
                 (_(||||||||||||)___________/   ""                |   Spotify views bot
                    `----------'       [ ))"-,                    |   Created by Tikene
                                         ""    `,  _,--....___    |
                                                 `/           \"\"\"\"
"""


def loadConfig():

    with open(configPath) as f:
        data = json.load(f)

    return data


def saveAccount(username, password):

    with open(configPath) as f:
        data = json.load(f)

    lastElement = len(data["accounts"])

    data["accounts"].update({
        lastElement: {
            "username": username,
            "password": password
        }
    })

    try:

        with open(configPath, 'w') as f:
            result = json.dump(data, f)
        return True

    except:

        return False

def saveTrack(tracklink):

    with open(configPath) as f:
        data = json.load(f)

    lastElement = len(data["tracklinks"])

    data["tracklinks"].update({
        lastElement: {
            "link": tracklink,
        }
    })

    try:

        with open(configPath, 'w') as f:
            result = json.dump(data, f)

        return True

    except:

        return False


def startViewLoop(driver, usr):

    tracks = loadConfig()["tracklinks"]

    for i in tracks:
        tracklink = tracks[i]["link"]
        driver.get(tracklink)

        while True:
            try:
                repeat = driver.find_element_by_xpath("//*[@id=\"main\"]/div/div[2]/div[2]/footer/div/div[2]/div/div[1]/div[2]/button[2]")
                play = driver.find_element_by_xpath("//*[@id=\"main\"]/div/div[2]/div[3]/main/div[2]/div[2]/div/div/div[2]/section/div[3]/div/button[1]")

                print(yellow + " "+usr+": Website fully loaded, found elements!")
                break
            except Exception as e:
                print(e)
                print(red + " Website not fully loaded yet")
                sleep(1.5)

        sleep(1)
        while True:
            title = play.get_attribute("aria-label")
            print(title, pauseStrings)
            if not title in pauseStrings:
                ActionChains(driver).click(play).perform()
                print(yellow + " "+usr+": Clicked play button")
                sleep(3)
            else:
                print(yellow + " INFO: Song being played")
                break

        while True:
            title = repeat.get_attribute("aria-label")
            if not title in loopStrings:
                ActionChains(driver).click(repeat).perform()
                print(yellow + " "+usr+": Clicked loop button")
                sleep(3)
            else:
                #print(yellow + " INFO: Song being looped")
                break

        oldtime = time()
        maxPlayTime = randint(1100, 1800)

        while True:
            # Loop button
            title = repeat.get_attribute("aria-label")
            if not title in loopStrings:
                ActionChains(driver).click(repeat).perform()
                print(yellow + " "+usr+": Clicked loop button")
                sleep(3)

            # Reload website after x time
            if time() - oldtime >= maxPlayTime:
                print(yellow + " "+usr+": "+str(maxPlayTime)+" seconds passed, reloading page")
                sleep(1)
                startViewLoop(driver, usr)
                break

            sleep(3)


def doLogin(usr, pss):
    try:
        driver = webdriver.Chrome(options=chromeoptions)
    except:
        print(red + "\n Error opening chromedriver, reinstalling...")
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=chromeoptions)

    #print(yellow + " "+usr+": Creating browser session")

    driver.get("https://accounts.spotify.com/en/login/")

    while True:
        try:
            usrObject = driver.find_element_by_name("username")
            pssObject = driver.find_element_by_name("password")
            logObject = driver.find_element_by_id("login-button")
            #print(yellow + " "+usr+": Website fully loaded!\n")
            break
        except:
            #print(yellow + " INFO: *Waiting for website to fully load*")
            sleep(1)


    uniform(0.5, 1)
    ActionChains(driver).click(usrObject).perform()
    uniform(0.2, 0.4)

    for i in usr:
        ActionChains(driver).send_keys(i).perform()
        sleep(uniform(0.05, 0.1))

    ActionChains(driver).click(pssObject).perform()
    uniform(0.2, 0.4)

    for i in pss:
        ActionChains(driver).send_keys(i).perform()
        sleep(uniform(0.05, 0.1))

    ActionChains(driver).click(logObject).perform()
    sleep(uniform(1, 1.5))

    count = 0
    maxtries = 4
    while True:
        currurl = driver.current_url
        count += 1

        if count >= maxtries:
            print(red + " \n\n ERROR: Couldn't log into '"+usr+"'")
            driver.quit()
            return False

        if currurl == "https://accounts.spotify.com/en/login/":
            #print(red + " ERROR: Not logged in ("+str(count)+"/"+str(maxtries-1)+")")
            pass
        elif currurl == "https://accounts.spotify.com/en/status":
            print(green + " Successfully logged into '"+usr+"'!\n")
            break

        sleep(1.5)


    #Process(target=startViewLoop, args=(driver)).start()
    startViewLoop(driver, usr)



def inicio():

    print(cyan + "\n\n\n\n" + asciiArt)
    print(cyan + "\n\n\n INFO: Starting service...\n\n")

    if not os.path.exists(configPath):

        with open(configPath, "w+") as f:
            json.dump({"accounts": {}, "tracklinks": {}}, f)

        print(yellow + "\n INFO: Created config file '"+configPath+"'")


    try:
        data = loadConfig()
        print(yellow + " INFO: '"+configPath+"' file loaded successfully\n")

    except Exception as error:
        print(red + " ERROR: Couldn't load file '"+configPath+"'")
        print(error)
        exit()


    # Spotify accounts
    numberAccounts = len(data["accounts"])

    if numberAccounts == 0:
        selectedAcc = input(" You currently have "+str(numberAccounts)+" Spotify accounts. Add more? (Y/n): ")
        if selectedAcc == "":
            selectedAcc = True
    else:
        selectedAcc = input(" You currently have "+str(numberAccounts)+" Spotify accounts. Add more? (y/N): ")
        if selectedAcc == "":
            selectedAcc = False

    if selectedAcc == "no" or selectedAcc == "n":
        selected = False
    elif selectedAcc == "yes" or selectedAcc == "y":
        selectedAcc = True

    if selectedAcc:

        print(yellow + "\n Type 'stop' anytime to continue\n")

        while True:

            usr = input(" > Spotify email: ")
            if usr == "stop":
                print("\n")
                break

            pss = input(" > Spotify password: ")
            if pss == "stop":
                print("\n")
                break

            if usr == "" or pss == "":
                print(red + "\n You cannot leave any field empty!")
                continue

            result = saveAccount(usr, pss)
            if result:
                print(green + "\n Account saved!\n")
            else:
                print(red + "\n Couldn't save account\n")


    # Spotify tracks
    numberTracks = len(data["tracklinks"])

    if numberTracks == 0:
        selected = input(" You currently have "+str(numberTracks)+" Spotify tracks. Add more? (Y/n): ")
        if selected == "":
            selected = True
    else:
        selected = input(" You currently have "+str(numberTracks)+" Spotify tracks. Add more? (y/N): ")
        if selected == "":
            selected = False

    if selected == "no" or selected == "n":
        selected = False
    elif selected == "yes" or selected == "y":
        selected = True


    if selected:

        print(yellow + "\n Type 'stop' anytime to continue\n")

        while True:

            track = input(" > Spotify track: ")

            if track == "stop":
                print("\n")
                break
            elif track == "":
                print(red + "\n You cannot add an empty track!")
                continue

            result = saveTrack(track)
            if result:
                print(green + "\n Track saved!\n")
            else:
                print(red + "\n Couldn't save track\n")


    """\
    # Browser visible
    selected = input(" Do you want the browser to be visible (y/N): ")

    if selected == "":
        selected = False
    elif selected == "no" or selected == "n":
        selected = False
    elif selected == "yes" or selected == "y":
        selected = True

    if not selected:
        print(yellow + "\n INFO: Silent mode ON")
        chromeoptions.silent = True
        chromeoptions.headless = True
    else:
        print(yellow + "\n INFO: Silent mode OFF")
    """

    try:
        data = loadConfig()

    except Exception as error:
        print(red + "\n ERROR: Couldn't load file '"+configPath+"'")
        print(error)
        exit()

    print(yellow + "\n\n INFO: Starting accounts loop")

    count = 0
    lenAcc = len(data["accounts"])

    sleep(1)

    for i in data["accounts"]:

        count = count + 1

        usr = data["accounts"][i]["username"]
        pss = data["accounts"][i]["password"]

        if not usr:
            print(red + " ERROR: Skipping account, missing username")
            pass
        elif not pss:
            print(red + " ERROR: Skipping account '"+usr+"', missing username")
            pass

        #print(cyan + " [Logging into account '"+usr+"' - ("+str(count)+"/"+str(lenAcc)+")]")


        #doLogin(usr, pss)
        try:
            Process(target=doLogin, args=(usr, pss)).start()
        except Exception as error:
            print(red + "\n An error occurred: "+error)

        sleep(1)

    print(green + "\n\n Finished starting sessions\n\n")


if __name__ == "__main__":
    inicio()
