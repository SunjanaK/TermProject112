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
        # print(pitch)
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
        elif 490 < pitch < 500:
            return "B"


def init(data):
    data.song = ["A", "A#", "B", "B#", "C", "C#", "D", "D#", "E"] #A string
    data.song2 = ["D", "D#", "E", "F", "F#", "G", "G#"] #D string
    data.song3 = ["G", "G#", "A", "A#", "B", "C", "C#"] #G string
    data.song4 = ['C', "C#", "D", "D#", "E", "F", "F#"] #C string
    data.timerDelay = 1000
    #these are the notes that will be checked off against what pyaudio hears
    data.play = [] #A string
    data.play2 = [] #D string
    data.play3 = [] #G string
    data.play4 = [] #C string
    #color of circle
    data.color = "purple"
    data.points = 0
    #speed of various notes
    data.speed = 20 #A string
    data.speed2 = 20 #D string
    data.speed3 = 20 #G string
    data.speed4 = 40 #C string

def timerFired(data):
    xcoord = 80 #C string
    ycoord = 20
    x2coord = 160 #G string
    x3coord = 240 #D string
    x4coord = 320 #A string

    if len(data.song4) > 0:
        data.play4.append([xcoord, ycoord, data.song4[0]])
        data.song4.pop(0)

    if len(data.song3) > 0:
        data.play3.append([x2coord, ycoord, data.song3[0]])
        data.song3.pop(0)
    if len(data.song2) > 0:
        data.play2.append([x3coord, ycoord, data.song2[0]])
        data.song2.pop(0)
    if len(data.song) > 0:
        data.play.append([x4coord, ycoord, data.song[0]])
        data.song.pop(0)

    for item4 in data.play4:
        item4[1] += data.speed4 #have letter move progressively down screen

        if item4[1] >= 170:
            if item4[2] == tester():
                data.points += 1
                data.color = "green"
        if item4[1] > 190:
            data.color = "purple"

    for item3 in data.play3:
        item3[1] += data.speed3 #have letter move progressively down screen

    for item2 in data.play2:
        item2[1] += data.speed2 #have letter move progressively down screen

    for item in data.play:
        item[1] += data.speed #have letter move progressively down screen

        if item[1] >= 170:
            if item[2] == tester(): #testing to see if correct note is played
            #when note hits purple circle
                data.points += 1 #adds a point if correct note was played
                data.color = "green" #circle turns green
        if item[1] > 190:
            data.color = "purple" #circle becomes purple after correct move


def redrawAll(canvas, data):
    #creating the four circles
    canvas.create_oval(70, 170, 90, 190, fill = data.color)
    canvas.create_oval(150, 170, 170, 190, fill = data.color)
    canvas.create_oval(230, 170, 250, 190, fill = data.color)
    canvas.create_oval(310, 170, 330, 190, fill = data.color)

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
