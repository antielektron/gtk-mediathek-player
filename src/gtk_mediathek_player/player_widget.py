from . import tools
from . import gst_widget
from gi.repository import Gtk, GLib, Gst
import gi

gi.require_version("Gtk", "3.0")
gi.require_version('Gst', '1.0')


class PlayerWidget(Gtk.Overlay):
    @staticmethod
    def create_player_for_uri(uri:str):
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

        GLib.timeout_add_seconds(1, self.update_controls)

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

        self._controls = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        self._controls.pack_start(self._play_button,
                                  expand=False,
                                  fill=False,
                                  padding=0)

        self._controls.pack_start(self._stop_button,
                                  expand=False,
                                  fill=False,
                                  padding=0)

        self._controls.pack_end(self._slider,
                                expand=True,
                                fill=True,
                                padding=0)

        self._controls.set_valign(Gtk.Align.END)

        self._play_button.connect("clicked", self.play)
        self._stop_button.connect("clicked", self.pause)

    def play_from_uri(self, uri: str):
        self._videoarea.load_from_uri(uri)

    def play(self, _=None):
        if self.get_state() != Gst.State.PLAYING:
            self._videoarea.play()

    def stop(self, _=None):
        state = self.get_state()
        if state == Gst.State.PLAYING or state == Gst.State.PAUSED:
            self._videoarea.stop()
            self._duration = None

    def pause(self, _=None):
        if self.get_state() == Gst.State.PLAYING:
            self._videoarea.pause()

    def get_state(self):
        return self._videoarea.get_state()
