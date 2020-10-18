from gi.repository import Gtk, Gst

from . import gst_pipeline


class GstWidget(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self)

        self._state = Gst.State.NULL

        self.connect('realize', self._on_realize)

    def _on_realize(self, widget):
        self._build_sink_and_widget()
        widget.pack_start(self._sinkwidget, True, True, 0)
        self._create_player()
        self._bus = self._player.get_bus()
        self._bus.add_signal_watch()
        self._bus.connect("message::state-changed", self.on_state_changed)
        #self.load_from_uri("https://pdvideosdaserste-a.akamaihd.net/int/2020/05/20/412d8633-dfaf-438c-93d2-f81914d44945/960-1_679663.mp4")
        self._sinkwidget.show()
        #self.play()
        #self._pipeline.set_state(Gst.State.PLAYING)

    def _build_pipeline(self):
        self._pipeline = Gst.Pipeline()

        bin = Gst.parse_bin_from_description('videotestsrc', True)

        factory = self._pipeline.get_factory()
        gtksink = factory.make('gtksink')

        self._pipeline.add(bin)

        self._pipeline.add(gtksink)

        bin.link(gtksink)

        return gtksink
    
    def _build_sink_and_widget(self) -> None:
        gtkglsink = Gst.ElementFactory.make("gtkglsink")

        # TODO: fallback if not graphic acceleration is available

        sinkbin = Gst.ElementFactory.make("glsinkbin")
        sinkbin.set_property("sink", gtkglsink)

        self._sink = sinkbin

        self._sinkwidget = gtkglsink.get_property("widget")
    
    def _create_player(self) -> None:
        self._player = Gst.ElementFactory.make("playbin", "player")
        self._player.set_property("video-sink", self._sink)
        self._state = Gst.State.NULL
    

    def load_from_uri(self, url:str) -> None:
        self.stop()
        self._player.set_property("uri", url)
    
    def play(self):
        self._player.set_state(Gst.State.PLAYING)
    
    def pause(self):
        self._player.set_state(Gst.State.PAUSED)
    
    def stop(self):
        self._player.set_state(Gst.State.NULL)
    
    def get_state(self):
        return self._state
    
    def get_duration(self):
        return self._player.query_duration(Gst.Format.TIME)[1] / Gst.SECOND
    
    def get_position(self):
        return self._player.query_position(Gst.Format.TIME)[1] / Gst.SECOND
    
    def set_position(self, position):
        if self._state == Gst.State.PLAYING or self._state == Gst.State.PAUSED:
            self._player.seek_simple(
                Gst.Format.TIME,
                Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT,
                position * Gst.SECOND
            )

    
    def on_state_changed(self, bus, msg):
        old, new, pending = msg.parse_state_changed()
        if not msg.src == self._player:
            # not from the playbin, ignore
            return

        self._state = new
