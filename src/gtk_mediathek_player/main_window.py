from . import mediathek_request as mr
from . import tools
from . import search_widget
from . import player_widget
from gi.repository import Gtk, GLib, Gdk
import gi

gi.require_version("Gtk", "3.0")

WINDOW_TITLE = "Gtk Mediathek Player"

class MainApp(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title=WINDOW_TITLE)

        self._current_mediathek_item = None

        self.set_default_icon_name("gtkmediathekplayer")

        self.set_role("GtkMediathekPlayer")
        self.set_wmclass("GtkMediathekPlayer", "GtkMediathekPlayer")

        self.set_default_size(800, 600)

        self._main_container = Gtk.Overlay()

        self._main_stack = Gtk.Stack()

        self._fullscreen = False

        self._player_widget = self._create_player_widget()
        self._search_widget = self._create_search_widget()

        self._main_stack.add_named(self._player_widget, "player")
        self._main_stack.add_named(self._search_widget, "search")

        self._main_stack.show_all()

        self._main_container.add(self._main_stack)

        self._headerbar = self._create_headerbar(True)

        # TODO: standardize widget creation methods
        self._fullscreen_bar = self._create_headerbar(False)
        self._fullscreen_bar.set_title(WINDOW_TITLE)
        self._create_fullscreen_bar()

        self._main_container.add_overlay(self._revealer)
        self.add(self._main_container)

        self.connect('motion-notify-event', self.on_mouse_move)

        self._seconds_after_mouse_move = 0

        self.set_active_pane("search")

        self.connect("key-press-event", self._on_keypress)

        GLib.timeout_add_seconds(1, self.update)

    def on_mouse_move(self, _, __):
        self._player_widget.show_controls()
        self._seconds_after_mouse_move = 0
        if self._fullscreen:
            self._revealer.set_reveal_child(True)

    def _on_keypress(self, widget, event):
        if event.keyval == Gdk.KEY_space:
            if self.get_active_pane() == "player":
                self._player_widget.toogle_play()
        if event.keyval == Gdk.KEY_F11:
            self.toggle_fullscreen()

    def update(self):
        if self._seconds_after_mouse_move > 1:
            self._revealer.set_reveal_child(False)

        self._seconds_after_mouse_move += 1
        self._player_widget.update_controls()

        return True

    def on_search(self, _=None):
        self.set_active_pane("search")

    def on_player(self, _=None):
        self.set_active_pane("player")

    def _create_context_switch(self, container):

        bbox = Gtk.ButtonBox(orientation=Gtk.Orientation.HORIZONTAL)
        bbox.set_layout(Gtk.ButtonBoxStyle.EXPAND)

        search_radio = tools.new_button_with_icon("edit-find")
        search_radio.connect("clicked", self.on_search)

        player_radio = tools.new_button_with_icon("tv-symbolic")
        player_radio.connect("clicked", self.on_player)

        bbox.pack_start(player_radio,
                        expand=False,
                        fill=False,
                        padding=0)

        bbox.pack_start(search_radio,
                        expand=False,
                        fill=False,
                        padding=0)

        container.pack_start(bbox)

    def _create_headerbar(self, main_bar=True):
        headerbar = Gtk.HeaderBar()

        fullscreen = tools.new_button_with_icon("view-fullscreen")

        fullscreen.connect("clicked", self.toggle_fullscreen)

        headerbar.pack_end(fullscreen)

        self._create_context_switch(headerbar)

        if main_bar:

            self._fullscreen_button = fullscreen

            headerbar.set_show_close_button(True)
            headerbar.props.title = "Gtk Mediathek Player"
            self.set_titlebar(headerbar)

        return headerbar

    def _create_fullscreen_bar(self):
        self._revealer = Gtk.Revealer()
        self._revealer.add(self._fullscreen_bar)
        self._revealer.set_valign(Gtk.Align.START)
        self._revealer.set_vexpand(False)
        self._revealer.set_transition_type(
            Gtk.RevealerTransitionType.SLIDE_DOWN)
        return self._revealer

    def _create_player_widget(self):
        return player_widget.PlayerWidget()

    def _create_search_widget(self):
        return search_widget.SearchWidget(self)

    def run(self):
        self.connect("destroy", Gtk.main_quit)
        self.show_all()
        Gtk.main()

    def set_active_pane(self, name: str):
        active_pane = self.get_active_pane()

        self._main_stack.set_visible_child_name(name)
        if name != "player":
            self._player_widget.pause()
            self.set_title(WINDOW_TITLE)
            self._fullscreen_bar.set_title(WINDOW_TITLE)
        else:
            if active_pane != "player":
                if self._player_widget.is_paused():
                    self._player_widget.play()
                
                if self._current_mediathek_item is not None:
                    title = self._current_mediathek_item.get_title()
                    if title is not None:
                        self.set_title(title)

    def get_active_pane(self):
        return self._main_stack.get_visible_child_name()

    def start_player(self,
                     uri: str,
                     mediathek_item:mr.MediathekViewWebAnswer = None):
        if self.get_active_pane() != "player":
            self.set_active_pane("player")
        
        self._current_mediathek_item = mediathek_item

        if mediathek_item is not None:
            title = mediathek_item.get_title()
            if title is not None:
                self.set_title(title)
                self._fullscreen_bar.set_title(title)
                #self._headerbar.set_title(title)

        self._player_widget.stop()
        self._player_widget.play_from_uri(uri)
        self._player_widget.play()

    def go_fullscreen(self):
        if self._fullscreen:
            return

        self._fullscreen = True

        self.fullscreen()
        self._revealer.set_reveal_child(True)

    def go_unfullscreen(self):
        if not self._fullscreen:
            return

        self._fullscreen = False

        self.unfullscreen()
        self._revealer.set_reveal_child(False)

    def toggle_fullscreen(self, _=None):
        if self._fullscreen:
            self.go_unfullscreen()
        else:
            self.go_fullscreen()
