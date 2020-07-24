import os
import subprocess

from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.lazy import lazy
from libqtile import layout, bar, widget, hook

from typing import List  # noqa: F401


mod = "mod4"
my_term = "tilix"
my_browser = "firefox"
my_editor = "atom"


keys = [
    # Switch between windows in current stack pane
    Key([mod], "k", lazy.layout.down()),
    Key([mod], "j", lazy.layout.up()),

    # Move windows up or down in current stack
    Key([mod, "control"], "k", lazy.layout.shuffle_down()),
    Key([mod, "control"], "j", lazy.layout.shuffle_up()),

    # Switch window focus to other pane(s) of stack
    Key([mod], "space", lazy.layout.next()),

    # Swap panes of split stack
    Key([mod, "shift"], "space", lazy.layout.rotate()),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split()),
    Key([mod], "Return", lazy.spawn(my_term)),
    Key([mod], "f", lazy.spawn(my_browser)),
    Key([mod], "c", lazy.spawn("ferdi")),
    Key([mod], "e", lazy.spawn(my_editor)),
    Key([mod], "a", lazy.spawn("xfce4-appfinder")),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod], "w", lazy.window.kill()),

    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "control"], "q", lazy.shutdown()),
    Key([mod], "r", lazy.spawncmd()),
]

group_names = 'WWW CHT SYS DEV ZSH ETC'.split()
groups = [Group(name, layout='columns') for name in group_names]
for i, name in enumerate(group_names):
    indx = str(i + 1)
    keys += [
        Key([mod], indx, lazy.group[name].toscreen()),
        Key([mod, 'shift'], indx, lazy.window.togroup(name))]

layouts = [
    layout.Max(),
    # layout.Stack(num_stacks=2),
    # Try more layouts by unleashing below layouts.
    # layout.Bsp(),
     layout.Columns(border_focus = '#ee237d'),
     layout.Matrix(border_focus = '#ee237d'),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
     layout.Tile(border_focus = '#ee237d'),
    # layout.TreeTab(),
    # layout.VerticalTile(),
     layout.Zoomy(),
]


## Vader ##
colors = [["#001334", "#001334"], # color 0
          ["#A2487B", "#A2487B"], # color 1
          ["#c7d5d9", "#c7d5d9"], # color 2
          ["#376692", "#376692"], # color 3
          ["#ee237d", "#ee237d"], # color 4
          ["#43A8C3", "#43A8C3"], # color 5
          ["#8b9597", "#8b9597"]] # color 6


## Fairy Floss ##
#colors = [["#42395D", "#42395D"], # color 0
#          ["#716799", "#716799"], # color 1
#          ["#ffffff", "#ffffff"], # color 2
#          ["#AE81FF", "#AE81FF"], # color 3
#          ["#C5A3FF", "#C5A3FF"], # color 4
#          ["#C2FFDF", "#C2FFDF"], # color 5
#          ["#F1568E", "#F1568E"]] # color 6


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
                       inactive = colors[3],
                       rounded = False,
                       highlight_color = colors[4],
                       highlight_method = "line",
                       this_current_screen_border = colors[3],
                       this_screen_border = colors[4],
                       other_current_screen_border = colors[0],
                       other_screen_border = colors[0],
                       foreground = colors[2],
                       background = colors[0]
                                ),

                widget.Sep(
                       linewidth = 0,
                       padding = 10,
                       foreground = colors[2],
                       background = colors[0]
                          ),

                widget.Prompt(
                       #padding = 10,
                       foreground = colors[2],
                       background = colors[4]
                             ),

                widget.Sep(
                       linewidth = 0,
                       padding = 10,
                       foreground = colors[2],
                       background = colors[0]
                                                       ),

                widget.WindowName(
                       foreground = colors[2],
                       background = colors[0],
                       padding = 0,
                       margin_y = 3,
                                 ),

                widget.Pacman(
                       update_interval = 1800,
                       foreground = colors[2],
                       mouse_callbacks = {'Button1': lambda qtile: qtile.cmd_spawn(myTerm + ' -e sudo pacman -Syu')},
                       background = colors[0]
                             ),

               widget.Sep(
                      linewidth = 0,
                      padding = 3,
                      foreground = colors[2],
                      background = colors[0]
                         ),

		        widget.Battery(
                        format = '{char} {percent:2.0%}',
                        foreground = colors[2],
                        background = colors[0],
                        mouse_callbacks = {'Button1': lambda qtile: qtile.cmd_spawn(myTerm + ' -e sudo shutdown now')},
                    #    padding = 0
                              ),

               widget.Sep(
                        linewidth = 0,
                        padding = 3,
                        foreground = colors[2],
                        background = colors[0]
                         ),

                widget.QuickExit(
                        default_text = '[X]',
                        countdown_format = '{}',
                        foreground = colors[2],
                        background = colors[0],
                    #    padding = 0
                                ),

                widget.Sep(
                       linewidth = 0,
                       padding = 3,
                       foreground = colors[2],
                       background = colors[0]
                          ),

		        widget.Clock(
                        format='%R',
                        foreground = colors[2],
                        background = colors[0],
                        padding = 0,
                        mouse_callbacks = {'Button1': lambda qtile: qtile.cmd_spawn('dmenu_run')}
                            ),

                widget.Sep(
                       linewidth = 0,
                       padding = 5,
                       foreground = colors[2],
                       background = colors[0]
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
    border_focus = '#376692',
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


@hook.subscribe.startup
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([home])


wmname = "LG3D"