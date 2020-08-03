import os
import re
import socket
import subprocess

from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from typing import List  # noqa: F401


mod = "mod4"
my_term = "alacritty"
my_files = "pcmanfm"
my_browser = "firefox"
my_editor = "atom"
my_screenshoot = "xfce4-screenshooter" #"kazam"
my_applauncher = "rofi -show drun"


## Abstract Shape ##
#colors = [["#ffffff", "#ffffff"], # colors[0]
#          ["#202227", "#202227"], # colors[1]
#          ["#cf324e", "#cf324e"], # colors[2]
#          ["#ff627f", "#ff627f"]] # colors[3]

## Wave ##
colors = [["#ffffff", "#ffffff"], # colors[0]
          ["#262c3a", "#262c3a"], # colors[1]
          ["#cdb283", "#cdb283"], # colors[2]
          ["#5e8197", "#5e8197"]] # colors[3]


keys = [

    Key([mod], "Up", lazy.layout.grow()),
    Key([mod], "Down", lazy.layout.shrink()),
    Key([mod], "space", lazy.layout.flip()),
    Key([mod], "k", lazy.layout.down()),
    Key([mod], "j", lazy.layout.up()),
    Key([mod, "shift"], "a", lazy.layout.swap_left()),
    Key([mod, "shift"], "d", lazy.layout.swap_right()),
    Key([mod, "control"], "k", lazy.layout.shuffle_down()),
    Key([mod, "control"], "j", lazy.layout.shuffle_up()),
    Key([mod], "space", lazy.layout.next()),
    Key([mod, "shift"], "space", lazy.layout.rotate()),
    Key([mod, "shift"], "Return", lazy.layout.toggle_split()),
    Key([mod], "Return", lazy.spawn(my_term)),
    Key([mod], "f", lazy.spawn(my_browser)),
    Key([mod], "c", lazy.spawn("ferdi")),
    Key([mod], "e", lazy.spawn(my_editor)),
    Key([mod], "r", lazy.spawn(my_applauncher)),
    Key([mod], "d", lazy.spawn(my_files)),
    Key([mod], "0", lazy.spawn(my_screenshoot)),
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod], "w", lazy.window.kill()),
    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "control"], "q", lazy.shutdown()),
#    Key([mod], "r", lazy.spawncmd()),

            ]


group_names = 'WWW CHT SYS DEV ZSH ETC'.split()
groups = [Group(name, layout='monadtall') for name in group_names]
for i, name in enumerate(group_names):
    indx = str(i + 1)
    keys += [
        Key([mod], indx, lazy.group[name].toscreen()),
        Key([mod, 'shift'], indx, lazy.window.togroup(name))]


layout_theme = {"border_focus": "#5e8197",
                "border_normal": "#ffffff",
                "border_width": 1,
                "margin":8,
                "single_margin": 0,
                "single_border_width": 0
                }


layouts = [
     layout.Max(),
     layout.MonadTall(**layout_theme),
    # layout.Floating(**layout_theme),
]


widget_defaults = dict(
                       font='sans',
                       fontsize=12,
                       padding=3,
                        )
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Wallpaper(
                       directory = '~/.config/qtile/Wallpaper',
                       label = {}
                                ),

                widget.GroupBox(
                       fontsize = 12,
                       margin_y = 3,
                       margin_x = 0,
                       padding_y = 5,
                       padding_x = 3,
                       borderwidth = 3,
                       active = colors[2],
                       inactive = colors[0],
                       rounded = False,
                       highlight_color = colors[3],
                       highlight_method = "line",
                       this_current_screen_border = colors[2],
                       this_screen_border = colors[1],
                       other_current_screen_border = colors[1],
                       other_screen_border = colors[1],
                       foreground = colors[0],
                       background = colors[1]
                                ),


                widget.Spacer(
                       background = colors[1],
                             ),


                widget.Pacman(
                       update_interval = 3600,
                       foreground = colors[0],
                background = colors[1],
                       mouse_callbacks = {'Button1': lambda qtile: qtile.cmd_spawn(my_term + ' -e sudo pacman -Syu')},
                       unavailable = colors[1],
                             ),


                widget.Sep(
                       linewidth = 0,
                       padding = 8,
                       foreground = colors[0],
                       background = colors[1]
                          ),


		        widget.Battery(
                       format = '{char} {percent:2.0%}',
                       foreground = colors[0],
                       background = colors[1],
                       mouse_callbacks = {'Button1': lambda qtile: qtile.cmd_spawn(my_term + ' -e sudo reboot')},
                       charge_char = '+',
                       discharge_char = '-',
                       full_char = '=',
#                       update_interval = "5",
                       low_percentage = 0.15,
                       low_foreground = colors[2],
                       show_short_text = False
                              ),

                widget.Sep(
                       linewidth = 0,
                       padding = 8,
                       foreground = colors[0],
                       background = colors[1]
                          ),

		        widget.Clock(
                       format='%R',
                       foreground = colors[0],
                       background = colors[1],
                       padding = 0,
                       mouse_callbacks = {'Button1': lambda qtile: qtile.cmd_spawn(my_term + ' -e sudo shutdown now')},
                            ),

                widget.Sep(
                       linewidth = 0,
                       padding = 5,
                       foreground = colors[0],
                       background = colors[1]
                          ),
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


dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    border_focus = "#ffffff",
    float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
                    ])


auto_fullscreen = True
focus_on_window_activation = "smart"


@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])


wmname = "LG3D"
