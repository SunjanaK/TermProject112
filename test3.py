import aubio
import random
import warnings
warnings.simplefilter("ignore", DeprecationWarning)
import numpy as num
import pyaudio
import wave
import threading
from tkinter import *
from multiprocessing import Process

# PyAudio object.
def tester():
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
        pitch = pDetection(samples)[0]
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
    data.song = ["A", "D", "E", "F#", "G"]
    # data.x = 200
    # data.y = 20
    data.timerDelay = 1000
    data.play = []
    data.color = "purple"
    data.points = 0

#need to make the spaces between the notes bigger

def timerFired(data):
    xcoord = 200
    ycoord = 20
    if len(data.song) > 0:
        data.play.append([xcoord, ycoord, data.song[0]])
        data.song.pop(0)

    # data.play.append([xcoord, ycoord, random.choice(data.notes)])
    for item in data.play:
        item[1] += 20

        if item[1] >= 170:
            if item[2] == tester():
                data.points += 1
                data.color = "green"


def redrawAll(canvas, data):
    # canvas.create_text(200, 100, text = detect("music.wav"))
    canvas.create_oval(188, 165, 210, 185, fill = data.color)
    canvas.create_text(50, 50, text = data.points)
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


if __name__ == "__main__":
    t1 = threading.Thread(target = tester)
    t1.start()

    new = run(400, 200)
    new.mainloop()


    # wait until thread 1 is completely executed
    t1.join()
    # wait until thread 2 is completely executed



    # both threads completely executed
    print("Done!")
