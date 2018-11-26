import aubio
import random
#https://docs.python.org/2/library/warnings.html
import warnings
warnings.simplefilter("ignore", DeprecationWarning)
import numpy as num
import pyaudio
import wave
import threading
from tkinter import *
from multiprocessing import Process

listy = ["A","A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]

#questions for TA's: how to make sure background noise doesn't influence machine, get rid of laggy moments
#how to keep 2 notes from meeting bc currently, they could meet at a specific time, right?
# PyAudio object.
# got some pyaudio/aubio merge code from here:
# https://github.com/aubio/aubio/issues/78
def tester(): #turn on microphone
    print("recording.....")
    p = pyaudio.PyAudio()

    # Open stream.
    stream = p.open(format=pyaudio.paFloat32,
        channels=1, rate=44100, input=True,
        frames_per_buffer=1024)

    # Aubio's pitch detection.
    pDetection = aubio.pitch("default", 2048,
        2048//2, 44100)
    # Set unit.
    pDetection.set_unit("Hz")
    pDetection.set_silence(-40)

    while True:

        data = stream.read(1024)
        samples = num.fromstring(data,
            dtype=aubio.float_type)
        pitch = pDetection(samples)[0] #getting pitch of note using Aubio
        # Compute the energy (volume) of the
        # current frame.
        volume = num.sum(samples**2)/len(samples)
        # Format the volume output so that at most
        # it has six decimal numbers.
        volume = "{:.6f}".format(volume)
        print(pitch)
        if 290 < pitch < 300:
            return "D"
        elif 425 < pitch < 445 or int(pitch) == 219 :
            return "A"
        elif 259 < pitch < 264:
            return "C"
        elif 275 < pitch < 279:
            return "C#"
        elif 305 < pitch < 315:
            return "D#"
        elif 328 < pitch < 332:
            return "E"
        elif 345 < pitch < 351:
            return "F"
        elif 365 < pitch < 373:
            return "F#"
        elif 390 < pitch < 396:
            return "G"
        elif 410 < pitch < 420:
            return "G#"
        elif 460 < pitch < 470:
            return "A#"
        elif 490 < pitch < 495:
            return "B"
        elif pitch == 0.00:
            return "Q"

#only gives me points when it registers note correctly
#how tester works: if any note is played other than note being checked, it stops
#have to get it to re-record for every falling note if something is played, and make sure the correct note is played only in that instant
def init(data):
    data.song = ["A", "A#", "B", "B#", "C", "C#", "D", "D#", "E"] #A string
    data.song2 = ["D", "D#", "E", "F", "F#", "G", "G#"] #D string
    data.song3 = ["G", "G#", "A", "A#", "B", "C", "C#"] #G string
    data.song4 = ['C', "C#", "D", "D#", "E", "F", "F#"] #C string
    data.timerDelay = 100
    data.counter = 0
    #these are the notes that will be checked off against what pyaudio hears
    data.play = [] #A string
    data.play2 = [] #D string
    data.play3 = [] #G string
    data.play4 = [] #C string
    #color of circle
    data.color = "purple"
    data.points = 0


def timerFired(data):

    xcoord = 80 #C string
    ycoord = 0
    x2coord = 160 #G string
    x3coord = 240 #D string
    x4coord = 320 #A string

    data.counter += 1
    if data.counter % 20 == 0 and len(data.song4) > 0:
        data.play4.append([xcoord, ycoord, data.song4[0]])
        data.song4.pop(0)
    elif data.counter % 68 == 0 and len(data.song3) > 0:
        data.play3.append([x2coord, ycoord, data.song3[0]])
        data.song3.pop(0)
    elif data.counter % 85 == 0 and len(data.song2) > 0:
        data.play2.append([x3coord, ycoord, data.song2[0]])
        data.song2.pop(0)
    elif data.counter % 100 == 0 and len(data.song) > 0:
        data.play.append([x4coord, ycoord, data.song[0]])
        data.song.pop(0)

    for item4 in data.play4:
         # have letter move progressively down screen

        if item4[1] >= 169:
            sound4 = tester()
            if sound4 == "Q" or sound4 != item4[2]:
                data.color = "red"
                print("hi")
            elif sound4 == item4[2]:
                data.color = "green"
                data.points += 1

            data.play4.remove(item4)


        else:
            data.color = "purple"
            item4[1] += 5

    for item3 in data.play3:
             # have letter move progressively down screen

        if item3[1] >= 169:
            sound3 = tester()
            if sound3 == "Q" or sound3 != item3[2]:
                data.color = "red"
                print("hello")
            elif sound3 == item3[2]:
                data.color = "green"
                data.points += 1

            data.play3.remove(item3)


        else:
            data.color = "purple"
            item3[1] += 5
    for item2 in data.play2:
                 # have letter move progressively down screen

        if item2[1] >= 169:
            sound2 = tester()
            if sound2 == "Q":
                data.color = "red"
            elif sound2 == item2[2]:
                data.color = "green"
                data.points += 1

            else:
                data.color = "red"
            data.play2.remove(item2)


        else:
            data.color = "purple"
            item2[1] += 5


    for item in data.play:
         #have letter move progressively down screen

        if item[1] >= 169:
            sound = tester()
            if sound == "Q":
                data.color = "red"
            elif sound == item[2]: #testing to see if correct note is played
            #when note hits purple circle
                data.color = "green" #circle turns green
                data.points += 1 #adds a point if correct note was played
            else:
                data.color = "red"
            data.play.remove(item)

        else:
            data.color = "purple"
            item[1] += 10

def redrawAll(canvas, data):
    #creating the four circles
    canvas.create_rectangle(0, 170, 400, 200, fill = data.color)
    canvas.create_text(50, 50, text = data.points)
    #creating the letters....
    for item4 in data.play4:
        canvas.create_text(item4[0], item4[1], text = item4[2])
    for item3 in data.play3:
        canvas.create_text(item3[0], item3[1], text = item3[2])
    for item2 in data.play2:
        canvas.create_text(item2[0], item2[1], text = item2[2])
    for item in data.play:
        canvas.create_text(item[0], item[1], text = item[2])



def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

#threading Pyaudio/Aubio and Tkinter
if __name__ == "__main__":
    t1 = threading.Thread(target = tester)
    t1.start()

    new = run(400, 200)
    new.mainloop()
    # wait until thread 1 is completely executed
    t1.join()

    # both threads completely executed
    print("Done!")
