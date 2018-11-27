


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
notesset = {"quartA.png","quartE.png", "halfG.png", "quartC.png", "halfA.png", "quartD.png", "quartB.png", "quartG.png", "halfD.png"}
img = cv2.imread("bigtwinkle.png")
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
listy = []

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

    elif "half" in note:
        loc = np.where(result >= 0.90)
        for pt in zip(*loc[::-1]):
            if pt[0] not in points and pt[0] - 1 not in points and pt[0] - 2 not in points:
                points.add(pt[0])
                listy.append(pt)











print(listy)
print(len(listy))


cv2.imshow("img", img)


cv2.waitKey(0)
cv2.destroyAllWindows()
