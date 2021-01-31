from gi.repository import Gtk


def new_button_with_icon(freedesktop_icon: str) -> Gtk.Button:
    button = Gtk.Button()
    icon = Gtk.Image.new_from_icon_name(freedesktop_icon, Gtk.IconSize.BUTTON)
    button.props.image = icon
    return button


def get_icon(freedesktop_icon: str) -> Gtk.Image:
    icon = Gtk.Image.new_from_icon_name(freedesktop_icon, Gtk.IconSize.BUTTON)
    return icon


def new_radio_button_with_icon(freedesktop_icon: str,
                               ref_widget=None) -> Gtk.RadioButton:
    if ref_widget is None:
        button = Gtk.RadioButton()
    else:
        button = Gtk.RadioButton.new_from_widget(ref_widget)
    icon = Gtk.Image.new_from_icon_name(
        freedesktop_icon, Gtk.IconSize.LARGE_TOOLBAR)
    button.props.image = icon
    return button


def seconds_to_timestring(seconds: int) -> str:
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    return f"{hours:>02}:{minutes:>02}:{seconds:>02}"
