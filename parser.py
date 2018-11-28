


# import cv2
# import numpy as np
# #it's not reading the last half G for some reason????
# notesset = {"quartE.png", "halfG.png", "quartC.png", "halfA.png", "quartD.png", "quartB.png", "quartG.png", "halfD.png"}
# img = cv2.imread("bigtwinkle.png")
# gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# songnotes = []
#
# template = cv2.imread("quartC.png", cv2.IMREAD_GRAYSCALE)
# w, h = template.shape[::-1]
#
# result = cv2.matchTemplate(gray_img, template, cv2.TM_CCOEFF_NORMED)
# loc = np.where(result >= 0.9)
# # print(loc)
# #if loc = (array([], dtype=int64), array([], dtype=int64)) you know there's nothing
# pointset = set()
# for pt in zip(*loc[::-1]):
#     if pt[0] - 10 not in pointset:
#         cv2.rectangle(img, (pt[0]-10, pt[1] - 20), (pt[0] + w + 20, pt[1] + h + 60), (0, 255, 0), 3)
#         pointset.add(pt[0] - 10)
#
#
#
#
# cv2.imshow("img", img)
#
#
# cv2.waitKey(0)
# cv2.destroyAllWindows()


#get pt of each note, so note, pt, note, pt
# produce a sublist for every unique y pt coordinate,
#quarters need 93
#halves need 90
#

import cv2
import numpy as np

#it's not reading the last half G for some reason????
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
        alphabet.append(listyletter[c+1][0])
alphabet.append("G")
print(alphabet)




cv2.waitKey(0)
cv2.destroyAllWindows()
