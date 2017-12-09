import urwid
import urwid.curses_display
import widgets
import re
import json
import GridItem
import time
from openhab import openHAB



palette = [
    ('titlebar', 'white, bold', 'light blue'),
    ('refresh button', 'dark green,bold', 'dark blue'),
    ('quit button', 'dark red', 'dark blue'),
    ('headers', 'white,bold', 'dark blue'),
    ('body', 'white', 'dark blue'),
    ('on', 'yellow,bold', 'dark blue'),
    ('off', 'light gray', 'dark blue'),
    ('lightbar', 'light blue', 'dark blue'),
    ('darkbar', 'black', 'dark blue')]


def refresh(_loop, _data):
    main_loop.draw_screen()
    lightbox.base_widget.set_text(get_update())
    main_loop.set_alarm_in(10, refresh)


def handle_input(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()
    elif key in ('r', 'R'):
        refresh(main_loop, '')
        return
    for keyitem in itemlist:
        if keyitem.key != '':
            if key == keyitem.key:
                if keyitem.ztype == GridItem.Type.SWITCH.value:
                    flip_state(openhab.get_item(keyitem.name))


def append_text(l, s, tabsize=10, color='body', type=GridItem.Type.SWITCH):
    if type == GridItem.Type.DOOR.value:
        if 'ON' in s:
            l.append((color, 'OPEN'.expandtabs(tabsize)))
        else:
            l.append((color, 'CLOSED'.expandtabs(tabsize)))
    else:
        if 'ON' in s:
            l.append(('on', s.expandtabs(tabsize)))
        elif 'OFF' in s:
            l.append(('off', s.expandtabs(tabsize)))
        elif is_number(s):
            if float(re.search(r'\d+', s).group()) == 0:
                l.append(('off', s.expandtabs(tabsize)))
            elif float(re.search(r'\d+', s).group()) > 0:
                l.append(('on', s.expandtabs(tabsize)))
        else:
            l.append((color, s.expandtabs(tabsize)))

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False


def flip_dimmer(item):
    if item.state is 0:
        item.update(100)
    else:
        item.update(0)


def flip_state(item):
    if item.state in 'ON':
        item.off()
    else:
        item.on()


def get_update():
    updates = [
        ('headers', u'Key\t'.expandtabs(6)),
        ('headers', u'Device \t '.expandtabs(25)),
        ('headers', u'Status \n'.expandtabs(5))]

    for item in itemlist:
        if item.key != '':
            append_text(updates, '({}) \t '.format(item.key), tabsize=6)
        else:
            append_text(updates, '{} \t '.format(''), tabsize=6)
        append_text(updates, '{} \t '.format(item.label), tabsize=25)
        append_text(updates, '{} \t '.format(openhab.get_item(item.name).state), tabsize=4, type=item.ztype)
        append_text(updates, '\n')
    append_text(updates, '\n')
    append_text(updates, 'Last update: ')
    append_text(updates, time.asctime(time.localtime(time.time())))

    return updates


with open('griditems.json', 'r') as f:
    data = json.load(f)
items = data.get('Griditems')
itemlist = []
for item in items:
    itemlist.append(GridItem.GridItem(item.get('name'), item.get('label'), item.get('type'), item.get('key')))

base_url = 'http://openhab:8080/rest'
openhab = openHAB(base_url)

header_text = urwid.Text(u' Crosscreek Control Grid', align='center')
header = urwid.AttrMap(header_text, 'titlebar')
menu = urwid.AttrMap(urwid.Text([
    u'Press (', ('refresh button', u'R'), u') to manually refresh. ',
    u'Press (', ('quit button', u'Q'), u') to quit. ',
    u'Last refresh: ', time.asctime( time.localtime(time.time()))
], align='center'), 'body')
quote_text = urwid.AttrMap(urwid.Text(u'Cross Creek Control Grid Initializing'), 'body')
quote_filler = urwid.AttrMap(urwid.Filler(quote_text, valign='middle', top=1, bottom=1), 'body')
v_padding = urwid.AttrMap(urwid.Padding(quote_filler, left=1, right=1), 'body')
lightbox = widgets.LineBoxColor(v_padding)
layout = urwid.Frame(header=header, body=lightbox, footer=menu)
main_loop = urwid.MainLoop(layout, palette, unhandled_input=handle_input)
main_loop.set_alarm_in(0, refresh)
main_loop.run()
