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
import cv2
import numpy as np

listy = ["A","A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
#quarter notes: only turns red for every other quarter note
#green only works for side with half notes
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
    notelist = []
    while True and len(notelist) < 10:

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
            notelist.append("D")
        elif 425 < pitch < 445 or 216 < pitch < 225 :
            notelist.append("A")
        elif 259 < pitch < 264:
            notelist.append("C")
        elif 275 < pitch < 279:
            notelist.append("C#")
        elif 305 < pitch < 315:
            notelist.append("D#")

        elif 320 < pitch < 335:
            notelist.append("E")

        elif 345 < pitch < 351:
            notelist.append("F")

        elif 365 < pitch < 373:
            notelist.append("F#")

        elif 390 < pitch < 396 or 190 < pitch < 200:
            notelist.append("G")

        elif 410 < pitch < 420:
            notelist.append("G#")

        elif 460 < pitch < 470:
            notelist.append("A#")

        elif 490 < pitch < 495 or 240 < pitch < 253:
            notelist.append("B")

        elif pitch == 0.00:
            notelist.append("Q")
    return notelist

# print(tester())
#only gives me points when it registers note correctly
#how tester works: if any note is played other than note being checked, it stops
#have to get it to re-record for every falling note if something is played, and make sure the correct note is played only in that instant





#it's not reading the last half G for some reason????

def noteparser():
    notesset = {"Aquart.png","Equart.png", "Ghalf.png", "Cquart.png", "Ahalf.png", "Dquart.png", "Bquart.png", "Gquart.png", "Dhalf.png"}
    img = cv2.imread("bigtwinkle.png")
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    listy = []
    listyletter = []

    for note in notesset:
        template = cv2.imread(note, cv2.IMREAD_GRAYSCALE)
        w, h = template.shape[::-1]
        result = cv2.matchTemplate(gray_img, template, cv2.TM_CCOEFF_NORMED)
        points = set()
        if "quart" in note:
            loc = np.where(result >= 0.93)
            for pt in zip(*loc[::-1]):
                if pt[0] not in points and pt[0] - 1 not in points and pt[0] - 2 not in points:
                    points.add(pt[0])
                    listy.append(pt)
                    listyletter.append(pt)
                    listyletter.append(note)


        elif "half" in note:
            loc = np.where(result >= 0.90)
            for pt in zip(*loc[::-1]):
                if pt[0] not in points and pt[0] - 1 not in points and pt[0] - 2 not in points:
                    points.add(pt[0])
                    listy.append(pt)
                    listyletter.append(pt)
                    listyletter.append(note)

    hundred = []
    twohundred = []
    threehundred = []
    fourhundred = []
    fivehundred = []
    ycoordslist = []
    yset = set()
    for coord in listy:
        yset.add(coord[1])
    ylst = sorted(yset)
    for y in ylst:
        if 0 < y <= 100:
            hundred.append(y)
        elif 100 < y <= 200:
            twohundred.append(y)
        elif 200 < y <= 300:
            threehundred.append(y)
        elif 300 < y <= 400:
            fourhundred.append(y)
        elif 400 < y <= 500:
            fivehundred.append(y)

    hundredcoords = []
    twohundredcoords = []
    threehundredcoords = []
    fourhundredcoords = []
    fivehundredcoords = []

    for i in listy:
        if i[1] in hundred:
            hundredcoords.append(i)
        elif i[1] in twohundred:
            twohundredcoords.append(i)
        elif i[1] in threehundred:
            threehundredcoords.append(i)
        elif i[1] in fourhundred:
            fourhundredcoords.append(i)
        elif i[1] in fivehundred:
            fivehundredcoords.append(i)


    ycoordslist.append(sorted(hundredcoords, key=lambda k: [k[0]]))
    ycoordslist.append(sorted(twohundredcoords, key=lambda k: [k[0]]))
    ycoordslist.append(sorted(threehundredcoords, key=lambda k: [k[0]]))
    ycoordslist.append(sorted(fourhundredcoords, key=lambda k: [k[0]]))
    ycoordslist.append(sorted(fivehundredcoords, key=lambda k: [k[0]]))

    newlist = []
    for coo in ycoordslist:
        if len(coo) > 0:
            for val in coo:
                newlist.append(val)


    alphabet = [] #this is all the notes of the song in order
    for lettercoord in newlist:
        if lettercoord in listyletter:
            c = listyletter.index(lettercoord)
            alphabet.append(listyletter[c+1])
    alphabet.append("Ghalf.png")
    quartlist = []
    halflist = []
    mainlist = []
    for i in range(len(alphabet)):
        if "quart" in alphabet[i]:
            quartlist.append(alphabet[i][0])
            if i % 2 == 1:
                halflist.append("")

        elif "half" in alphabet[i]:
            quartlist.append("")
            quartlist.append("")
            halflist.append(alphabet[i][0])
    mainlist.append(quartlist)
    mainlist.append(halflist)
    return mainlist
    # print(mainlist)
    # return alphabet

def init(data):
    note = noteparser()
    data.song = ["A", "A#", "B", "B#", "C", "C#", "D", "D#", "E"] #A string
    data.song2 = ["D", "D#", "E", "F", "F#", "G", "G#"] #D string
    data.song3 = note[1] #half notes
    data.song4 = note[0] #quarter notes
    data.timerDelay = 100
    data.counter = 0
    #these are the notes that will be checked off against what pyaudio hears
    data.play = [] #A string
    data.play2 = [] #D string
    data.play3 = [] #G string
    data.play4 = [] #C string
    #color of circle
    data.colorlist = []
    data.end = 0

    data.points = 0


def timerFired(data):

    xcoord = 80 #C string
    ycoord = 0
    x2coord = 160 #G string
    x3coord = 240 #D string
    x4coord = 320 #A string


    if data.counter % 5 == 0 and len(data.song4) > 0:
        data.play4.append([xcoord, ycoord, data.song4[0]])
        data.song4.pop(0)
    if data.counter % 10 == 0 and len(data.song3) > 0:
        data.play3.append([x2coord, ycoord, data.song3[0]])
        data.song3.pop(0)
    # elif data.counter % 48 == 0 and len(data.song2) > 0:
    #     data.play2.append([x3coord, ycoord, data.song2[0]])
    #     data.song2.pop(0)
    # elif data.counter % 26 == 0 and len(data.song) > 0:
    #     data.play.append([x4coord, ycoord, data.song[0]])
    #     data.song.pop(0)

    for item3 in data.play3:
         # have letter move progressively down screen

        if item3[1] >= 169 and item3[2] != "":
            if item3[2] in set(tester()):
                data.colorlist.append("green")
                data.points += 1
            else:
                data.colorlist.append("red")


            data.play3.remove(item3)


        else:
            data.colorlist.append("purple")
            item3[1] += 5


    for item4 in data.play4:
         # have letter move progressively down screen

        if item4[1] >= 169 and item4[2] != "":
            if item4[2] in set(tester()):
                data.colorlist.append("green")
                data.points += 1
            else:
                data.colorlist.append("red")


            data.play4.remove(item4)


        else:
            data.colorlist.append("purple")
            item4[1] += 5

    # for item2 in data.play2:
    #      # have letter move progressively down screen
    #
    #     if item2[1] >= 169:
    #         if item2[2] in set(tester()):
    #             data.color = "green"
    #             data.points += 1
    #             print("hi")
    #         else:
    #             data.color = "red"
    #
    #
    #         data.play2.remove(item2)
    #
    #
    #     else:
    #         data.color = "purple"
    #         item2[1] += 5
    #
    # for item in data.play:
    #      # have letter move progressively down screen
    #
    #     if item[1] >= 169:
    #         if item[2] in set(tester()):
    #             data.color = "green"
    #             data.points += 1
    #             print("hi")
    #         else:
    #             data.color = "red"
    #
    #
    #         data.play.remove(item)
    #
    #
    #     else:
    #         data.color = "purple"
    #         item[1] += 5

    data.counter += 1
def redrawAll(canvas, data):
    #creating the four circles

    if "green" in data.colorlist:
        canvas.create_rectangle(0, 170, 400, 200, fill = "green")
    elif "red" in data.colorlist:
        canvas.create_rectangle(0, 170, 400, 200, fill = "red")
    else:
        canvas.create_rectangle(0, 170, 400, 200, fill = "purple")
    data.colorlist = []
    canvas.create_text(40, 50, text = "Points:" + str(data.points))
    #creating the letters....
    for item4 in data.play4:
        canvas.create_text(item4[0], item4[1], text = item4[2])
    for item3 in data.play3:
        canvas.create_text(item3[0], item3[1], text = item3[2])
    for item2 in data.play2:
        canvas.create_text(item2[0], item2[1], text = item2[2])
    for item in data.play:
        canvas.create_text(item[0], item[1], text = item[2])
    print(len(data.play4))
    print(len(data.play3))
    if data.play4 == [] and data.play3 == []:
        print("good job")
        canvas.create_text(data.width/2, data.height/2, text = "Great job!")


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
    # t1 = threading.Thread(target = tester)
    # t1.start()

    new = run(400, 200)
    new.mainloop()
    # wait until thread 1 is completely executed
    # t1.join()

    # both threads completely executed
    print("Done!")
