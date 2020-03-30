#CC written by Joost Markerink http://joostmarkerink.nl
import pew
import time
pew.init()
screen = pew.Pix()
drawing = pew.Pix()
cursorx = 3
cursory = 4
prevkeys = pew.keys()
paint = 1
editing = True
willEdit = False
xbuttontime = 0
eventTime = 0
isClear = True
splash = [
0b11111111,
0b10000001,
0b10111101,
0b10100101,
0b10111101,
0b10100001,
0b10000001,
0b11111111
]

for y in range(8):
    for x in range(8):
        screen.pixel(x,y,(splash[y] >> (7 - x)) & 1)
pew.show(screen)
pew.tick(2.4)

def fill(sx,sy, fill_value):
    orig_value = drawing.pixel(sx, sy)
    stack = set(((sx, sy),))
    if fill_value == orig_value:
        return
    while stack:
        x, y = stack.pop()
        if drawing.pixel(x, y) == orig_value:
            drawing.pixel(x, y, fill_value)
            if x > 0:
                stack.add((x - 1, y))
            if x < 7:
                stack.add((x + 1, y))
            if y > 0:
                stack.add((x, y - 1))
            if y < 7:
                stack.add((x, y + 1))
while True:
    keys = pew.keys()
    tm = time.monotonic()
    needUpdate=False
    if keys != prevkeys:
        needUpdate = True
        eventTime = tm
        if keys > 0 and editing == False:
            willEdit = True
            needUpdate=True
        elif keys == 0 and willEdit:
            editing = True
            willEdit = False
        elif editing:
            if keys:
                if keys & pew.K_LEFT and (prevkeys & pew.K_LEFT) == 0:
                    cursorx -= 1
                if keys & pew.K_RIGHT and (prevkeys & pew.K_RIGHT) == 0:
                    cursorx += 1
                if keys & pew.K_UP and (prevkeys & pew.K_UP) == 0:
                    cursory -= 1
                if keys & pew.K_DOWN and (prevkeys & pew.K_DOWN) == 0:
                    cursory += 1
            cx = cursorx % 8
            cy = cursory % 8
            if keys & pew.K_O:
                if (prevkeys & pew.K_O) == 0:
                    if drawing.pixel(cx, cy) == 1:
                        paint = 0
                    else:
                        paint = 1
                        isClear = False
                drawing.pixel(cx, cy, paint)
            if keys & pew.K_X:
                if (prevkeys & pew.K_X) == 0:
                    if drawing.pixel(cx, cy) == 0:
                        fill(cx, cy, 1)
                        isClear = False
                    else:
                        fill(cx, cy, 0)
    elif keys == 0 and editing and isClear == False and (tm - eventTime) > 3:
        isClear = True
        for y in range(8):
            for x in range(8):
                if drawing.pixel(x,y) > 0:
                    isClear = False
                    break
        editing = isClear
        needUpdate = True
    prevkeys = keys
    if needUpdate:
        for y in range(8):
            for x in range(8):
                screen.pixel(x,y,drawing.pixel(x,y))
        if editing or willEdit:
            screen.pixel(cursorx % 8, cursory % 8, 3)
    pew.show(screen)