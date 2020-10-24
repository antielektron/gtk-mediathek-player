
import gi

gi.require_version('Gtk', '3.0')
gi.require_version('Gst', '1.0')

from gi.repository import Gtk, Gst

from . import gst_pipeline
from . import main_window


gst_pipeline.init_gst()


win = main_window.MainApp()
win.run()