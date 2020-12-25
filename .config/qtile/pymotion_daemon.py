from Pyro5.api import expose, behavior, serve
import pyglet
import os
import subprocess
import shlex
import pyautogui
import numpy as np
pyautogui.FAILSAFE=False

window_width=pyautogui.size()[0]
window_height=pyautogui.size()[1]

chars='ZXCVM<>?ASDFJKL:QWERUIOP'
cell_width=window_width//8
cell_height=window_height//3

label_xs=[]
label_ys=[]
labels=[]

line_xs=[]
line_ys=[]
lines=[]

for i, char in enumerate(chars):
    label_xs.append(cell_width*(i%8)+cell_width//2)
    label_ys.append(cell_height*(i//8)+cell_height//2)
    labels.append(
        pyglet.text.Label(
            char, font_size=48,
            x=label_xs[i], y=label_ys[i],
            anchor_x='center', anchor_y='center')
    )
    line_xs.append(cell_width*(i%8))
    line_ys.append(cell_height*(i//8))
    lines.append(
        pyglet.shapes.Line(line_xs[i], 0, line_xs[i], window_height)
    )
    lines.append(
        pyglet.shapes.Line(0, line_ys[i], window_width, line_ys[i])
    )

keys=[122,120,99,118,109,44,46,47, 97,115,100,102,106,107,108,59, 113,119,101,114,117,105,111,112]
pyautogui_label_ys=window_height-np.array(label_ys)

@expose
@behavior(instance_mode="single")
class Pymotion(object):
    def move(self):
        # take screenshot
        subprocess.run(shlex.split("scrot /tmp/screenshot.png -o"))
        with open('/tmp/screenshot.png', 'rb') as stream:
            image = pyglet.image.load('/tmp/screenshot.png', file=stream)
        window = pyglet.window.Window(fullscreen=True, visible=True)

        @window.event
        def on_draw():
            image.blit(0, 0)
            for label in labels:
                label.draw()
            for line in lines:
                line.draw()
             
        event_loop = pyglet.app.EventLoop()

        @window.event
        def on_key_press(symbol, modifiers):
            if symbol in keys:
                i=keys.index(symbol)
                pyautogui.moveTo(label_xs[i], pyautogui_label_ys[i], duration=0) 
            window.close()
            event_loop.exit()

        event_loop.run()

serve(
    {Pymotion: "pymotion"},
    use_ns=False,
    port=9090)
