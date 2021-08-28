import rpyc
from rpyc.utils.server import ThreadedServer
import pyglet, subprocess, pyautogui, argparse
import numpy as np

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
            anchor_x='center', anchor_y='center', bold=True)
    )
    labels.append(
        pyglet.text.Label(
            char, font_size=42,
            x=label_xs[i], y=label_ys[i],
            anchor_x='center', anchor_y='center', color=(0,0,0,255))
    )
    line_xs.append(cell_width*(i%8))
    line_ys.append(cell_height*(i//8))
    lines.append(
        pyglet.shapes.Line(line_xs[i], 0, line_xs[i], window_height, width=4)
    )
    lines.append(
        pyglet.shapes.Line(0, line_ys[i], window_width, line_ys[i], width=4)
    )
    lines.append(
        pyglet.shapes.Line(line_xs[i], 0, line_xs[i], window_height, color=(0,0,0), width=2)
    )
    lines.append(
        pyglet.shapes.Line(0, line_ys[i], window_width, line_ys[i], color=(0,0,0), width=2)
    )

keys=[122,120,99,118,109,44,46,47, 97,115,100,102,106,107,108,59, 113,119,101,114,117,105,111,112]
pyautogui_label_ys=window_height-np.array(label_ys)


class MyService(rpyc.Service):
    def exposed_get_grid(self):
        # take screenshot
        subprocess.run("scrot -o /tmp/pymotion.png".split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # use stream to speedup
        with open('/tmp/pymotion.png', 'rb') as screenshot_stream:
            image = pyglet.image.load('/tmp/pymotion.png', file=screenshot_stream)
            
        window = pyglet.window.Window(fullscreen=True)
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Pymotion")
    parser.add_argument('-d', '--daemon', help="run as a daemon", action="store_true")
    parser.add_argument('-t', '--toggle', help="toggle to show grid", action="store_true")
    args = parser.parse_args()
    if args.daemon:
        t = ThreadedServer(MyService, port=18861)
        t.start()
    elif args.toggle:
        conn = rpyc.connect("localhost", port=18861)
        conn.root.get_grid()
