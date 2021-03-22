from selenium import webdriver
from time import sleep
import datetime
import os
from config import *


driver = webdriver.Chrome(PATH)
driver.get("https://instagram.com")
log = open("log.txt", "a")
logtime = datetime.datetime.now()
timenow = logtime.strftime("%c")
sleep(3)

#Bot account
username = driver.find_element_by_name('username')
password = driver.find_element_by_name('password')
username.send_keys(usr)
password.send_keys(instagram_passowrd)
login = driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]/button/div")
login.click()
sleep(3)

trgact = "jib.lewis"
#User that wants to be scaned
userurl = "https://www.instagram.com/" + trgact + "/"

log.write("Start at " + timenow + "\n")

#returns current followers
def get_followers():
    
    driver.get(userurl)
    sleep(2)

    amtflw = int((
    (driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span").text)))

    flws = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[2]/a")
    flws.click()
    print(amtflw)

    sleep(4)



    scroll_box = driver.find_element_by_xpath("/html/body/div[5]/div/div/div[2]")
    last_ht, ht = 0, 1

    while last_ht != ht:
        last_ht = ht
        sleep(4)
        ht = driver.execute_script("""
            arguments[0].scrollTo(0, arguments[0].scrollHeight); 
            return arguments[0].scrollHeight;
            """, scroll_box)

    sleep(2)

    #Get list
    links = scroll_box.find_elements_by_tag_name('a')
    names = [name.text for name in links if name.text != '']
    followers = [names[e] for e in range(amtflw)]
    print("Having %s followers" % len(followers))
    #print(followers)
    log.write("got followers" + "\n")
    print("got followers")
    return followers


sleep(2)

#returns followers from list
def get_oldfollow():
    old_folow = []
    # open file and read the content in a list
    with open('listfile.txt', 'r') as filehandle:
        for line in filehandle:
        # remove linebreak which is the last character of the string
            currentPlace = line[:-1]

        # add item to the list
            old_folow.append(currentPlace)
        log.write("got followeing" + "\n")
        return old_folow



currentfollowers = get_followers()

oldfollowers = get_oldfollow()


unfollow = []

for item in currentfollowers:
  if item not in oldfollowers:
    unfollow.append(item)

print("done")

print(unfollow)


if currentfollowers != oldfollowers:
    with open('unfollowers.txt', 'a') as filehandle:
        for listitem in unfollow:
            filehandle.write('%s\n' % listitem)
    with open('listfile.txt', 'w') as filehandle:
        for listitem in currentfollowers:
            filehandle.write('%s\n' % listitem)
    print(unfollow)    
    for x in unfollow:
        driver.get("https://api.callmebot.com/whatsapp.php?" + whtsappnum + "&text=" + wtsmsg + "&" + whtsappapi)
        sleep(30)
else:
    log.write("no diff" + "\n")
    print("no diff")
log.write("got followers" + "\n")
print("done") 
driver.close()


