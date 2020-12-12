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
cell_width=window_width//8
cell_height=window_height//3
chars='ZXCVM<>?ASDFJKL:QWERUIOP'
xs=[]
ys=[]
labels=[]
for i, char in enumerate(chars):
    xs.append(cell_width*(i%8)+cell_width//2)
    ys.append(cell_height*(i//8)+cell_height//2)
    labels.append(
        pyglet.text.Label(
            char, font_size=48,
            x=xs[i], y=ys[i],
            anchor_x='center', anchor_y='center')
    )
keys=[122,120,99,118,109,44,46,47, 97,115,100,102,106,107,108,59, 113,119,101,114,117,105,111,112]
pyautogui_ys=window_height-np.array(ys)

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
             
        event_loop = pyglet.app.EventLoop()

        @window.event
        def on_key_press(symbol, modifiers):
            if symbol in keys:
                i=keys.index(symbol)
                pyautogui.moveTo(xs[i], pyautogui_ys[i], duration=0) 
            window.close()
            event_loop.exit()

        event_loop.run()

serve(
    {Pymotion: "pymotion"},
    use_ns=False,
    port=9090)
