from typing import List
from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Screen, KeyChord
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
import os
import subprocess
from libqtile import hook
import shlex
import re
import time

mod = "mod4"
terminal = guess_terminal()
home = os.path.expanduser('~')
default_brightness='0.25'

def brightness_control(action='decrease'):
    @lazy.function
    def f(qtile):
        output=subprocess.check_output("xrandr --verbose", shell=True, text=True)
        primary_output=re.search("(.*) connected primary(.|\n)*Brightness: (.*)", output)
        monitor=primary_output.group(1)
        brightness=float(primary_output.group(3))
        if action=='decrease' and brightness > 0.05:
            brightness=brightness-0.05
        elif action=='increase' and brightness < 0.95:
            brightness=brightness+0.05
        subprocess.run("xrandr --output {} --brightness {}".format(monitor, brightness), shell=True)
    return(f)

"""
Keys
"""
keys = [
    # S #
    # scrcpy
    Key([mod, "control"], "s", lazy.spawn("scrcpy --shortcut-mod=rctrl --bit-rate 10M --disable-screensaver --max-fps 60 -w")),
    #rctrl,lctrl

    # D #
    Key([mod], "g", lazy.spawn("goldendict")),

    # M #
    # mute
#    Key([mod], "m", pymotion),
    Key([mod, "control"], "m", lazy.spawn('pactl set-sink-mute @DEFAULT_SINK@ toggle')),

    # N #
    #Key([mod, "control"], "n", lazy.next_screen()),
    Key([mod], "n", lazy.layout.next()),

    # O #
    # Toggle floating
    Key([mod, "control"], "o", lazy.window.toggle_floating()),
    # output
    KeyChord(
        [mod, "shift", "control"], "o", 
        [Key([], "n", lazy.spawn('xrandr -o 0')),
            Key([], "i", lazy.spawn('xrandr -o 2')),
            Key([], "r", lazy.spawn('xrandr -o 1')),
            Key([], "l", lazy.spawn('xrandr -o 3')),
            Key([], "e", lazy.spawn('xrandr --output DP2 --off'),lazy.spawn('xrandr --output eDP1 --primary --mode 1920x1080 --rate 120 --brightness 0.35')),
            Key([], "d", lazy.spawn('xrandr --output eDP1 --off'),lazy.spawn('xrandr --output DP2 --primary --mode 2560x1440 --rate 144 --brightness 0.3'))],
        "output control: (n)ormal, (i)nverted, (l)eft, (r)ight, (e)DP, d(P)"
        ),

    # P #
    #Key([mod, "control"], "p", lazy.prev_screen()),
    Key([mod, "control"], "p", lazy.spawn('pavucontrol')),
    KeyChord(
        [mod, "shift", "control"], "p", 
        [Key(["shift"], "r", lazy.spawn('reboot')),
            Key([], "r", lazy.restart()),
            Key([], "l", lazy.shutdown()),
            Key([], "p", lazy.spawn('poweroff'))],
        "Power control: (S-r)start, (r)eload, (p)oweroff, (l)ogout"),

    # HJKL #
    # mod + letter: switch between windows in current stack pane
    # mod + control+letter: move windows up or down in current stack
    Key([mod], "h", lazy.layout.left()),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod], "l", lazy.layout.right()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),

    # B #
    Key([mod, "control"], "b", lazy.spawn("firefox")),
    Key([mod, "shift"], "b", lazy.spawn("blueman-manager")),
    Key([mod, "shift", "control"], "b", lazy.spawn("qtile-cmd -o cmd -f hide_show_bar")),

    # F #
    Key([mod, "control"], "f", lazy.window.toggle_fullscreen()),


    # Q #
    Key([mod], "q", lazy.spawn('copyq toggle')),
    Key([mod, "control"], "q", lazy.window.kill()),
    Key([mod, "shift", "control"], "q", lazy.spawn("xkill")),

    # R #
    Key([mod], "r", lazy.spawncmd()),
    # Switch window focus to other pane(s) of stack
    Key([mod, "shift"], "r", lazy.layout.rotate()),
    # Swap panes of split stack
    Key([mod, "control"], "r", lazy.spawn('terminator -e ranger')),

    # Other #
    # toggle layouts
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod, "shift"], "Return", lazy.layout.toggle_split()),
    # pymotion
    Key([mod], "space", lazy.spawn("python {}/.config/qtile/pymotion.py".format(home))),
    # Change window sizes
    Key([mod], "bracketleft", lazy.layout.shrink()),
    Key([mod], "bracketright", lazy.layout.grow()),
    # brightness and volume control
    Key([mod], "period", brightness_control(action='decrease')),
    Key([mod, "control"], "period", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -5%")),
    Key([mod], "slash", brightness_control(action='increase')),
    Key([mod, "control"], "slash", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +5%")),
]

"""
Groups
"""
groups = [Group(i) for i in "asdfuiop"]
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
#    layout.Max(),
#    layout.Stack(num_stacks=2),
    layout.Bsp(),
    # layout.Columns(),
#    layout.Matrix(),
    layout.MonadTall(),
    layout.MonadWide(),
    layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font='sans',
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

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
                widget.Chord(),
                widget.Net(),
                widget.CPU(),
                widget.Memory(),
                widget.Battery(),
                widget.CheckUpdates(),
                widget.Systray(),
                widget.Clock(format='%Y-%m-%d %a %I:%M %p'),
            ],
            24,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

follow_mouse_focus = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    {'wmclass': 'copyq'},  # gitk
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
])

"""
Hooks
"""
#@hook.subscribe.startup
#def autostart():

@hook.subscribe.startup_once
def autostart():
    subprocess.Popen('blueman-applet')
    #subprocess.Popen(shlex.split("xrandr --output eDP-1 --off"))
    #subprocess.Popen(shlex.split("xrandr --output DP-2 --primary --mode 2560x1440 --rate 144 --brightness "+default_brightness))
    subprocess.Popen(shlex.split("xrandr --output eDP1 --off"))
    subprocess.Popen(shlex.split("xrandr --output DP2 --primary --mode 2560x1440 --rate 144 --brightness "+default_brightness))
    #subprocess.Popen(shlex.split("xrandr --output eDP-1-1 --off"))
    #subprocess.Popen(shlex.split("xrandr --output DP-1-2 --primary --mode 2560x1440 --rate 144 --brightness "+default_brightness))
    subprocess.Popen('goldendict')
    subprocess.Popen('fcitx')
    subprocess.Popen('nm-applet')
    subprocess.Popen('copyq')
    subprocess.Popen(shlex.split("jupyter-lab --no-browser"))
    subprocess.Popen(shlex.split("python {}/.config/qtile/pymotion_daemon.py".format(home)))

@hook.subscribe.screen_change
def restart_on_randr(ev):
    subprocess.Popen(shlex.split("qtile-cmd -o cmd -f restart"))
