from libqtile import bar, layout, widget, hook
from libqtile.config import Group, Key, Match, Screen, KeyChord
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
#from typing import List
import os, subprocess, shlex, re, time, pyautogui
import pandas as pd
# pymotion requriement: pyglet rpyc argparse numpy
# status bar requries python-psutil 
# lyrics search requries playerctl
# widget.BitcoinTicker() requires proper locale setting

mod = "mod4"
alt = "mod1"
terminal = guess_terminal()
home = os.path.expanduser('~')
default_brightness='0.3'
big_movement=80
small_movement=20
tiny_movement=10
pyautogui.PAUSE=0
widget_defaults = dict(
    font='sans',
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()
# java compatibility
wmname = "LG3D"
cursor_warp = False
floating_layout = layout.Floating(float_rules=[ #xprop
    Match(wm_class='copyq'),
    Match(wm_class="{}/.config/qtile/pymotion.py".format(home)),
    Match(wm_class="/tmp/pymotion.py".format(home)),
    Match(wm_class='goldendict'),
])
focus_on_window_activation = "smart"
follow_mouse_focus = False
# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_fullscreen = False
auto_minimize = False

def set_keyboarder_layout(action):
    @lazy.function
    def f(qtile):
        if action=='switch_backspace':
            subprocess.Popen(["xmodmap",
                "-e", "keycode 66 = Escape Escape Escape",
                "-e", "keycode 78 = Caps_Lock NoSymbol Caps_Lock",
                "-e", "keycode 22 = backslash bar",
                "-e", "keycode 51 = BackSpace BackSpace",
                "-e", "clear lock"])
        elif action=='us_layout':
            subprocess.Popen("setxkbmap -layout us".split())
        pyautogui.press('esc')
    return f

def brightness_control(action):
    @lazy.function
    def f(qtile):
        output=subprocess.check_output("xrandr --verbose".split(), text=True)
        primary_output=re.search("(.*) connected primary(.|\n)*Brightness: (.*)", output)
        monitor=primary_output.group(1)
        brightness=float(primary_output.group(3))
        if action=='decrease' and brightness > 0.05:
            brightness=brightness-0.05
        elif action=='increase' and brightness < 0.95:
            brightness=brightness+0.05
        subprocess.Popen("xrandr --output {} --brightness {}".format(monitor, brightness).split())
    return f

def autogui(action, move=small_movement, scroll=5, move_x=0, move_y=0):
    @lazy.function
    def f(qtile):
        if action=='left':
            pyautogui.move(-move,0,tween=0.000001)
        elif action=='right':
            pyautogui.move(move,0,tween=0.000001)
        elif action=='up':
            pyautogui.move(0,-move,tween=0.000001)
        elif action=='down':
            pyautogui.move(0,move,tween=0.000001)

        elif action=='click':
            pyautogui.click(duration=0.1)
        elif action=='right_click':
            pyautogui.click(button='right')
        elif action=='click_at':
            pyautogui.click(move_x, move_y)
            pyautogui.press('esc')

        elif action=='scroll_up':
            pyautogui.scroll(scroll)
        elif action=='scroll_down':
            pyautogui.scroll(-scroll)
        elif action=='horizontal_scroll_up':
            pyautogui.hscroll(2*scroll)
        elif action=='horizontal_scroll_down':
            pyautogui.hscroll(2*-scroll)

        elif action=='escape':
            pyautogui.press('esc')
        elif action=='enter':
            pyautogui.press('enter')

        # drag
        elif action=='mark':
            x, y=pyautogui.position()
            df=pd.DataFrame({'Privious location':[x,y]})
            df.to_csv("/tmp/pointer_location.csv")
        elif action=='go':
            drag_x, drag_y=pyautogui.position()
            df=pd.read_csv("/tmp/pointer_location.csv".format(home))
            x,y=df['Privious location']
            pyautogui.moveTo(x, y)
            pyautogui.click()
            pyautogui.dragTo(drag_x, drag_y)
        elif action=='close':
            time.sleep(5)
            pyautogui.keyDown('ctrl')
            pyautogui.keyDown('winleft')
            pyautogui.keyDown('q')
            pyautogui.keyUp('ctrl')
            pyautogui.keyUp('winleft')
            pyautogui.keyUp('q')
    return f

def search_lyric():
    @lazy.function
    def f(qtile):
        output=subprocess.check_output("playerctl metadata xesam:title".split(), text=True)
        title=re.search("(.*)\n", output).group(1)
        output=subprocess.check_output("playerctl metadata xesam:artist".split(), text=True)
        artist=re.search("(.*)\n", output).group(1)
        search_keywords=title+' - '+artist+' lyrics'
        search_keywords=search_keywords.replace(' ', '+')
        search_url="https://www.google.com/search?q="+search_keywords
        subprocess.run("firefox --new-tab {}".format(search_url).split())
    return f

"""
Keys
"""
keys = [
    # A #

    # B #
    Key([mod, "control"], "b", lazy.spawn("firefox")),
    Key([mod, "shift"], "b", lazy.spawn("blueman-manager")),
    Key([mod, "shift", "control"], "b", lazy.hide_show_bar()),

    # C #
    Key([mod], "c", autogui('scroll_up')),
    Key([mod, "shift"], "c", autogui('horizontal_scroll_up')),

    # D #

    # E #
    Key([mod], "e", lazy.window.toggle_fullscreen()),

    # F #

    # G #
    Key([mod], "g", lazy.spawn("goldendict")),

    # H #

    # M #
    # mute
    Key([mod, "control"], "m", lazy.spawn('pactl set-sink-mute @DEFAULT_SINK@ toggle')),
    # music
    KeyChord(
        [mod, "shift"], "m", 
        #Key([], "d", autogui('click_at', move_x=2420, move_y=1358)),
        [   Key([], "p", lazy.spawn('playerctl previous'), autogui('escape')),
            Key([], "n", lazy.spawn('playerctl next'), autogui('escape')),
            Key([], "space", lazy.spawn('playerctl play-pause'), autogui('escape')),
            Key([], "t", lazy.spawn('tidal-hifi'), autogui('escape')),
         #   Key([], "s", lazy.spawn('spotify'), autogui('escape')),
            Key([], "l", search_lyric(), autogui('escape')),
            Key([], "b", lazy.spawn("bluetoothctl connect 00:02:5B:00:FF:01"), autogui('escape')),
            Key(['shift'], "b", lazy.spawn("bluetoothctl disconnect 00:02:5B:00:FF:01"), autogui('escape')),
            Key([], "h", lazy.spawn("pactl set-card-profile alsa_card.pci-0000_00_1f.3 output:hdmi-stereo-extra2+input:analog-stereo"), autogui('escape')), ],
        "music control: (d)ark, (space)play, (p)revious, (n)ext, (l)yrics, (b)luetooth, (h)dmi"
        ),

    # N #

    # O #

    # output
    KeyChord(
        [mod, "shift", "control"], "o", 
        [ Key([], "n", lazy.spawn('xrandr -o 0')),
            Key([], "i", lazy.spawn('xrandr -o 2')),
            Key([], "l", lazy.spawn('xrandr -o 3')),
            Key([], "r", lazy.spawn('xrandr -o 1')),
            Key([], "e", lazy.spawn('xrandr --output DP-2 --off'),lazy.spawn('xrandr --output eDP-1 --primary --mode 1920x1080 --rate 120 --brightness 0.35')),
            Key([], "o", lazy.spawn('xrandr --output DP-2 --primary --mode 1920x1080 --rate 120 --brightness 0.35')),
            Key([], "d", lazy.spawn('xrandr --output eDP-1 --off'),lazy.spawn('xrandr --output DP-2 --primary --mode 2560x1440 --rate 120 --brightness 0.3')),
            Key([], "m", set_keyboarder_layout(action='switch_backspace')),
            Key([], "u", set_keyboarder_layout(action='us_layout')),
            ],
        "output control: (n)ormal, (i)nverted, (l)eft, (r)ight, (e)DP, (d)P, (m)ajestouch, (u)s_layout"
        ),

    # P #
    Key([mod, "control"], "p", lazy.spawn('pavucontrol')),
    KeyChord(
        [mod, "shift", "control"], "p", 
        [Key(["shift"], "r", lazy.spawn('reboot')),
            Key([], "r", lazy.restart()),
            Key([], "l", lazy.shutdown()),
            Key([], "p", lazy.spawn('poweroff'))],
        "Power control: (S-r)start, (r)eload, (p)oweroff, (l)ogout"),

    # R #
    Key([mod], "r", lazy.spawncmd()),

    # S #
    # scrcpy
    Key([mod, "control"], "s", lazy.spawn("scrcpy --shortcut-mod=lalt,ralt --bit-rate 16M --disable-screensaver --max-fps 60 -w")),

    # T #
    # Toggle floating
    Key([mod], "t", lazy.window.toggle_floating()),

    # HJKL #
    # mod + letter: switch between windows
    Key([mod], "h", lazy.layout.left()),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod], "l", lazy.layout.right()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),


    # Q #
    Key([mod], "q", lazy.spawn('copyq toggle')),
    Key([mod, "control"], "q", lazy.window.kill()),
    Key([mod, "shift", "control"], "q", lazy.spawn("xkill")),

    # Switch window focus to other pane(s) of stack
    Key([mod, "shift"], "r", lazy.layout.rotate()),
    # Swap panes of split stack
    Key([mod, "control"], "r", lazy.spawn('sakura -e ranger')),

    # V #
    Key([mod], "v", autogui('scroll_down')),
    Key([mod, "shift"], "v", autogui('horizontal_scroll_down')),


    # W #

    # x #

    # Y #
    Key([mod], "y", lazy.next_layout()),
    Key([mod, "shift"], "y", lazy.prev_layout()),

    # Z #

    # Other #
    # toggle layouts
    Key([mod], "Tab", lazy.screen.next_group()),
    Key([mod, "shift"], "Tab", lazy.screen.prev_group()),
    Key([mod], "Return", lazy.spawn(terminal)),
    Key([mod, "shift"], "Return", lazy.layout.toggle_split()),
    # pymotion
    #Key([mod], "space", lazy.spawn("python {}/.config/qtile/pymotion.py -t".format(home))),
    Key([mod], "space", lazy.spawn("python /tmp/pymotion.py -t".format(home))),
    #Key([mod], "space", pymotion()),
    # Change window sizes
    Key([mod], "bracketleft", lazy.layout.shrink(), lazy.layout.shrink(), lazy.layout.shink_left(), lazy.layout.shink_right()),
    Key([mod], "bracketright", lazy.layout.grow(), lazy.layout.grow(), lazy.layout.grow_left(), lazy.layout.grow_right()),
    #Key([mod, "shift"], "bracketleft", lazy.layout.increase_ratio()),
    #Key([mod, "shift"], "bracketright", lazy.layout.decrease_ratio()),
    Key([mod, "shift"], "bracketleft", lazy.layout.shink_up(), lazy.layout.shink_down()),
    Key([mod, "shift"], "bracketright", lazy.layout.grow_up(), lazy.layout.grow_down()),
    # brightness and volume control
    Key([mod], "period", brightness_control(action='decrease')),
    Key([mod, "control"], "period", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -2.5%")),
    Key([mod], "slash", brightness_control(action='increase')),
    Key([mod, "control"], "slash", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +2.5%")),
    Key([mod], "semicolon", lazy.screen.next_group()),
    Key([mod], "comma", lazy.screen.prev_group()),
    Key([], "Print", lazy.spawn("scrot {}/Picture/p.png".format(home))),
    Key([mod], "Print", lazy.spawn("scrot -s -f {}/Picture/p.png".format(home))),
    Key([], "Pause", set_keyboarder_layout(action='switch_backspace')),

    # Group #
    # ASDW ZX Escape Tab#
    Key([alt], "a", autogui('left', move=big_movement)),
    Key([alt], "d", autogui('right', move=big_movement)),
    Key([alt], "w", autogui('up', move=big_movement)),
    Key([alt], "s", autogui('down', move=big_movement)),
    Key([alt, "shift"], "a", autogui('left')),
    Key([alt, "shift"], "d", autogui('right')),
    Key([alt, "shift"], "w", autogui('up')),
    Key([alt, "shift"], "s", autogui('down')),
    Key([alt, "shift", "control"], "a", autogui('left', move=tiny_movement)),
    Key([alt, "shift", "control"], "d", autogui('right', move=tiny_movement)),
    Key([alt, "shift", "control"], "w", autogui('up', move=tiny_movement)),
    Key([alt, "shift", "control"], "s", autogui('down', move=tiny_movement)),

    Key([alt, "shift"], "Caps_Lock", lazy.spawn("xte 'mouseclick 1'")),
    Key([alt, "shift"], "Escape", lazy.spawn("xte 'mouseclick 1'")),
    Key([alt, "shift"], "Tab", lazy.spawn("xte 'mouseclick 3'")),
    Key([alt], "Caps_Lock", autogui('click')),
    Key([alt], "Escape", autogui('click')),
    Key([alt], "Return", autogui('click')),
    Key([alt], "Tab", autogui('right_click')),
    Key([alt], "m", autogui("mark")),
    Key([alt], "g", autogui("go")),
]

"""
Groups
"""
groups = [Group(i) for i in "asdfuiop"]
groups[0] = Group('a', spawn=['firefox', 'sakura'])
groups[4] = Group('f', spawn=['tidal-hifi', 'easyeffects'])
for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen(),
            desc="Switch to group {}".format(i.name)),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True)),
    ])

"""
Layouts
"""
layouts = [
    layout.Bsp(),
    layout.MonadTall(),
    layout.MonadWide(),
#    layout.Zoomy(),
#    layout.Stack(num_stacks=2),
#    layout.Columns(),
#    layout.Matrix(),
#    layout.RatioTile(),
#    layout.Tile(),
#    layout.TreeTab(),
#    layout.VerticalTile(),
]

"""
Screens
"""
screens = [
    Screen(
        bottom=bar.Bar(
            [
                widget.CurrentLayout(),
                widget.GroupBox(),
                widget.Prompt(),
                widget.WindowName(),
                widget.Spacer(width=128),
                widget.Notify(),
                widget.Chord(),
                widget.Net(),
                widget.CPU(),
                widget.Memory(),
                widget.ThermalSensor(show_tag=True),
                #widget.ThermalSensor(),
                widget.BitcoinTicker(),
                widget.CheckUpdates(),
                widget.Systray(),
                widget.Clock(format='%Y-%m-%d %a %I:%M %p'),
            ],
            24,
        ),
    ),
]

"""
Hooks
"""
@hook.subscribe.startup_once
def autostart():
    subprocess.Popen(("xrandr --output DP-1-2 --primary --mode 2560x1440 --rate 120 --brightness 0.2").split())
    subprocess.Popen("python {}/.config/qtile/pymotion.py -d".format(home).split())
    subprocess.Popen("cp {}/.config/qtile/pymotion.py /tmp/pymotion.py".format(home).split())
    subprocess.Popen("jupyter-lab --no-browser".split())
    subprocess.Popen('copyq')
    subprocess.Popen("fcitx5 -d".split())
    subprocess.Popen('goldendict')
    subprocess.Popen('nm-applet')
    subprocess.Popen("blueman-applet")
    subprocess.Popen(["xmodmap",
        "-e", "keycode 66 = Escape Escape Escape",
        "-e", "keycode 78 = Caps_Lock NoSymbol Caps_Lock",
        "-e", "keycode 22 = backslash bar",
        "-e", "keycode 51 = BackSpace BackSpace",
        "-e", "clear lock"])
