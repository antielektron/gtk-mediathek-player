import gi
gi.require_version('Gst', '1.0')

from gi.repository import Gst

def init_gst() -> None:
    if not init_gst.gst_initialized:
        Gst.init(None)
        Gst.init_check(None)
        init_gst.gst_initialized = True

init_gst.gst_initialized = False


def create_pipeline():
    init_gst()

    pipeline = Gst.Pipeline()
    
    return pipeline

