from examples import animate
import os
import visionapi
from picamera import PiCamera
from time import sleep
from pynput import keyboard
import random

"""for i in range(10):    
    sleep(2)
    stri = '/home/pi/Desktop/HackathonProject/pics/image{}.jpg'.format(i)
    camera.capture(stri)
"""


def perform_capture():
    global count, camera
    #Capturing the file
    print('Entered the method')
    stri = '/home/pi/Desktop/HackathonProject/pics/image{}.png'.format(count)
    count += 1
    print('Images taken so far is {}'.format(count))
    sleep(5)
    camera.capture(stri)
    camera.stop_preview()
    #Process the file
    #walking = os.walk('./pics')
    files = os.listdir('./pics')
    files.sort()
    curr_photo = files[-1]
    result = visionapi.detect_face(str('/home/pi/Desktop/HackathonProject/pics/' + curr_photo))
    play_song = "No Emotion Detected"
    emotion = ''
    print(result)
    for i in range(4):
        if result[i] == 'VERY_LIKELY':
            if i == 0:
                emotion = 'Angry: '
                print('Angry')
                songs = ["Sh*t Luck, Modest Mouse","Smells Like Teen Spirit, Nirvana","You Know How I Do, Taking Back Sunday","Basket Case, Green Day"]
            elif i == 1:
                emotion = 'Joy: '
                print('Joy')
                songs = ['Happy by Pharell Williams', 'Uptown Funk by Bruno Mars', 'Walking On Sunshine by Katrina and the Waves', 'I gotta feeling by Black Eyed Peas']
            elif i == 2:
                emotion = 'Surprised: '
                print('Surprised')
                songs = ['Random by G-Eazy', 'Wow by Post Malone', 'Sicko Mode by Travis Scott', 'Despacito by Daddy Yankee and Louis Fonsi', 'Never gonna give you up by Rick Astley']
            else:
                emotion = 'Sorrow: '
                print('Sorrow')
                songs = ['Sun and Moon by Above and Beyond','I remember by Kaskade and Deadmau5','Concrete Angel by Gareth Emery','On hold by the xx','Raise your weapon by Deadmau5']
            # choose song at index and print to lcd
            play_song = songs[random.randint(0,3)]
            break
    animate.run_display(play_song, emotion)
    #sleep(15)
    #print(result)
    
    


if __name__ == '__main__':
    #camera.rotation = 180
    #run_count = 0
    #while run_count != 10:
    animate.countdown(5)
    print('Starting camera')
    camera = PiCamera()
    camera.start_preview()
    count = 0
    print('Entering perform capture')
    perform_capture()
    print('Song Created')
        #run_count += 1
    #lis = keyboard.Listener(on_press = perform_capture)
    #lis.start()
    #lis.join()
        
        
