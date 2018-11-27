
import cv2
import numpy as np
#it's not reading the last half G for some reason????
notesset = {"quartE.png", "halfG.png", "quartC.png", "halfA.png", "quartD.png", "quartB.png", "quartG.png", "halfD.png"}
img = cv2.imread("bigtwinkle.png")
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)



template = cv2.imread("quartA.png", cv2.IMREAD_GRAYSCALE)
w, h = template.shape[::-1]

result = cv2.matchTemplate(gray_img, template, cv2.TM_CCOEFF_NORMED)
loc = np.where(result >= 0.9)
print(loc)
#if loc = (array([], dtype=int64), array([], dtype=int64)) you know there's nothing

for pt in zip(*loc[::-1]):
    cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 3)


cv2.imshow("img", img)


cv2.waitKey(0)
cv2.destroyAllWindows()
