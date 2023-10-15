import pywhatkit
import datetime
from gtts import gTTS
import os

def sendmsg(address,msg):
    
    current_time = datetime.datetime.now()
    time = current_time.strftime("%H:%M:%S")
    time = time.split(":")
    hour = int(time[0])
    min = int(time[1])
    sec = int(time[2])

    if sec < 45:
        if min + 1 >= 60 and hour + 1 < 24:
            hour += 1
            min = 0
        elif min + 1 >= 60 and hour + 1 > 24:
            hour = 0
            min = 1
        else:
            min += 1

    elif sec > 45:
        if min + 2 >= 60 and hour + 1 < 24:
            hour += 1
            min = min + 2 - 60
        elif min + 1 >= 60 and hour + 1 > 24:
            hour = 0
            min = min + 2 - 60
        else:
            min += 2
        
    print(hour)
    print(min)
    pywhatkit.sendwhatmsg(address, msg, hour, min, 15, True, 10)
    
def texttovoice(text):
    myobj = gTTS(text=text, lang='en', slow = False)
    myobj.save("test.mp3")
    os.system(r'"C:\Program Files\VideoLAN\VLC\vlc.exe" test.mp3')

def main():
    #sendmsg("+601126699816" , "Test")
    texttovoice("Test")
    
main()