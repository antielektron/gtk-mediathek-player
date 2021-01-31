from . import tools
from . import gst_widget
from gi.repository import Gtk, GLib, Gst, Gdk
import gi

gi.require_version("Gtk", "3.0")
gi.require_version('Gst', '1.0')


class PlayerWidget(Gtk.Overlay):
    @staticmethod
    def create_player_for_uri(uri: str):
        widget = PlayerWidget()
        widget.play_from_uri(uri)
        return widget

    def __init__(self) -> None:
        Gtk.Overlay.__init__(self)
        self._videoarea = gst_widget.GstWidget()

        self._create_controls()

        self.add(self._videoarea)

        self.add_overlay(self._controls)

        self._duration = None

        self._is_update = False

        self._seconds_after_mouse_move = 0

        self._slider.connect("value-changed", self._on_user_slider_change)

    def update_controls(self):

        self._is_update = True

        state = self.get_state()

        if state == Gst.State.PLAYING or state == Gst.State.PAUSED:
            self._duration = self._videoarea.get_duration()

            self._slider.set_range(0, self._duration)

        if self._duration is not None:

            self._slider.set_value(self._videoarea.get_position())

        self._is_update = False

        if self._seconds_after_mouse_move > 3:
            self._controls.set_reveal_child(False)

        self._seconds_after_mouse_move += 1

        return True

    def _on_user_slider_change(self, range):
        if self._is_update:
            return
        value = self._slider.get_value()
        self._videoarea.set_position(value)

    def _create_controls(self) -> Gtk.Box:

        self._slider = Gtk.Scale.new_with_range(orientation=Gtk.Orientation.HORIZONTAL,
                                                min=0,
                                                max=100,
                                                step=1)

        self._slider.props.draw_value = False

        self._play_button = tools.new_button_with_icon('media-playback-start')

        self._stop_button = tools.new_button_with_icon('media-playback-stop')

        self._play_pause_button = tools.new_button_with_icon(
            'media-playback-pause')

        bbox = Gtk.ButtonBox(orientation=Gtk.Orientation.HORIZONTAL)
        bbox.set_layout(Gtk.ButtonBoxStyle.EXPAND)
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self._controls = Gtk.Revealer()

        # bbox.pack_start(self._play_button,
        #               expand=False,
        #               fill=False,
        #               padding=0)

        # bbox.pack_start(self._stop_button,
        #               expand=False,
        #               fill=False,
        #               padding=0)

        bbox.pack_start(self._play_pause_button,
                        expand=False,
                        fill=False,
                        padding=0)

        box.pack_start(bbox,
                       expand=False,
                       fill=False,
                       padding=0)

        box.pack_end(self._slider,
                     expand=True,
                     fill=True,
                     padding=0)

        self._controls.add(box)

        self._controls.set_valign(Gtk.Align.END)
        self._controls.set_transition_type(Gtk.RevealerTransitionType.SLIDE_UP)
        self._controls.set_reveal_child(True)

        style_context = self._controls.get_style_context()
        style_context.add_class(Gtk.STYLE_CLASS_TITLEBAR)

        #self._play_button.connect("clicked", self.play)
        #self._stop_button.connect("clicked", self.pause)

        self._play_pause_button.connect("clicked", self.toogle_play)

    def play_from_uri(self, uri: str):
        self._videoarea.load_from_uri(uri)

    def play(self, _=None):
        if self.get_state() != Gst.State.PLAYING:
            new_icon = tools.get_icon("media-playback-pause")
            self._play_pause_button.props.image = new_icon
            self._videoarea.play()

    def stop(self, _=None):
        state = self.get_state()
        if state == Gst.State.PLAYING or state == Gst.State.PAUSED:
            new_icon = tools.get_icon("media-playback-start")
            self._play_pause_button.props.image = new_icon
            self._videoarea.stop()
            self._duration = None

    def toogle_play(self, _=None):
        state = self.get_state()

        if state == Gst.State.PLAYING:
            self.pause()

        elif state == Gst.State.PAUSED:
            self.play()

    def pause(self, _=None):
        if self.get_state() == Gst.State.PLAYING:
            new_icon = tools.get_icon("media-playback-start")
            self._play_pause_button.props.image = new_icon
            self._videoarea.pause()

    def get_state(self):
        return self._videoarea.get_state()

    def show_controls(self):
        self._controls.set_reveal_child(True)
        self._seconds_after_mouse_move = 0
