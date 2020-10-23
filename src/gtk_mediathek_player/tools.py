from gi.repository import Gtk


def new_button_with_icon(freedesktop_icon: str) -> Gtk.Button:
    button = Gtk.Button()
    icon = Gtk.Image.new_from_icon_name(freedesktop_icon, Gtk.IconSize.BUTTON)
    button.props.image = icon
    return button


def new_radio_button_with_icon(freedesktop_icon: str,
                               ref_widget=None) -> Gtk.RadioButton:
    if ref_widget is None:
        button = Gtk.RadioButton()
    else:
        button = Gtk.RadioButton.new_from_widget(ref_widget)
    icon = Gtk.Image.new_from_icon_name(freedesktop_icon, Gtk.IconSize.LARGE_TOOLBAR)
    button.props.image = icon
    return button