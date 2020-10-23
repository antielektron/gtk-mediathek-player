
import gi
from . import main_window

from gi.repository import Gtk, Gio, Gst, Gdk

gi.require_version('Gtk', '3.0')
gi.require_version('Gst', '1.0')

Gst.init(None)
Gst.init_check(None)


win = main_window.MainApp()
win.run()