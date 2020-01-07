def wheel(pos):
    pos %= 255
    if pos < 0:
        while pos < 0:
            pos += 256
    if pos < 85:
        return int(255 - pos * 3), int(pos * 3), 0
    if pos < 170:
        pos -= 85
        return 0, int(255 - pos * 3), int(pos * 3)
    pos -= 170
    return int(pos * 3), 0, int(255 - (pos * 3))
def fillTrellisRainbow_AtPoint(press):
    pixel = (press[1] * 8) + press[0]
    pixel_index = (pixel * 256 // 32)
    trellis.pixels.fill(wheel(pixel_index & 255))
def fillTrellisRainbow():
    for x in range(trellis.pixels.width):
        for y in range(trellis.pixels.height):
            pixel_index = (((y * 8) + x) * 256 // 32)
            trellis.pixels[x, y] = wheel(pixel_index & 255)
def trellis_effect_fadeFromTo(colorFrom,colorTo,steps,delay):
    print("fade")
    # fade UP
    rDelta = colorTo[0]-colorFrom[0]
    gDelta = colorTo[1]-colorFrom[1]
    bDelta = colorTo[2]-colorFrom[2]

    for step in range(steps):
        
        r = int(rDelta/steps) * step
        g = int(gDelta/steps) * step
        b = int(bDelta/steps) * step
        color = (r,g,b)
        print(color)
        trellis.pixels.fill(color)
        trellis.pixels.show()
        time.sleep(delay)        
def effect_stepToColor(targetColor,perStep):
    for pixel in trellis.pixels:
        if pixel != targetColor:
            newColor = []
            for channelID in range(len(pixel)):
                if abs(pixel[channelID] + perStep) - targetColor[channelID] < 0:
                    #less than one step away
                    newColor.append(targetColor[channelID])
                else:
                    newColor.append(pixel[channelID] + perStep)
            trellis.pixels.fill(newColor) 