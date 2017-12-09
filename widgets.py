import urwid


class LineBoxColor(urwid.WidgetDecoration, urwid.WidgetWrap):
    def __init__(self, widget):
        hline = urwid.Divider('─')
        self._lvline = urwid.AttrMap(urwid.SolidFill('│'), 'lightbar')
        self._rvline = urwid.AttrMap(urwid.SolidFill('│'), 'darkbar')
        self._topline = urwid.AttrMap(
            urwid.Columns([
                ('fixed', 1, urwid.AttrMap(urwid.Text('┌'), 'lightbar')),
                urwid.AttrMap(hline, 'lightbar'),
                ('fixed', 1, urwid.AttrMap(urwid.Text('┐'), 'darkbar')),
            ]),
            'whiteonblue')
        self._bottomline = urwid.AttrMap(
            urwid.Columns([
                ('fixed', 1, urwid.AttrMap(urwid.Text('└'), 'lightbar')),
                urwid.AttrMap(hline, 'darkbar'),
                ('fixed', 1, urwid.AttrMap(urwid.Text('┘'), 'darkbar'))
            ]),
            'whiteonblue')

        self._middle = urwid.Columns(
            [('fixed', 1, self._lvline), widget, ('fixed', 1, self._rvline)],
            focus_column=1,
        )
        self._all = urwid.Pile(
            [('flow', self._topline), self._middle, ('flow', self._bottomline)],
            focus_item=1,
        )

        urwid.WidgetWrap.__init__(self, self._all)
        urwid.WidgetDecoration.__init__(self, widget)
