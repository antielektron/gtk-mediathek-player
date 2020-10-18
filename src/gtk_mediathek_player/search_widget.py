from gi.repository import Gtk, GLib
import gi

gi.require_version("Gtk", "3.0")

from . import tools
from . import mediathek_request as mr

class SearchWidget(Gtk.Box):
    def __init__(self, parent: 'main_window.MainApp') -> None:
        Gtk.Box.__init__(self, orientation = Gtk.Orientation.VERTICAL)

        self._search_bar = Gtk.SearchBar()
        self._search_entry = Gtk.SearchEntry()
        self._search_bar.add(self._search_entry)
        self.pack_start(self._search_bar, False, False, 0)

        self._search_bar.show_now()
        self._search_bar.show_all()
        self._search_bar.set_search_mode(True)

        self._search_entry.connect("activate", self.on_search)

        self._main_window = parent
        self._current_search_cards = []
        self._search_card_container = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)

        self.pack_end(self._search_card_container, False, True, 10)
    
    def dialog_response(self, widget, response_id):
        # if the button clicked gives response OK (-5)
        if response_id == Gtk.ResponseType.OK:
            pass
        # if the messagedialog is destroyed (by pressing ESC)
        elif response_id == Gtk.ResponseType.DELETE_EVENT:
            pass
        widget.destroy()

    def display_warning(self, message):
        messagedialog = Gtk.MessageDialog(parent=self,
                                          flags=Gtk.DialogFlags.MODAL,
                                          type=Gtk.MessageType.WARNING,
                                          buttons=Gtk.ButtonsType.OK,
                                          message_format=message)
        # connect the response (of the button clicked) to the function
        # dialog_response()
        messagedialog.connect("response", self.dialog_response)
        # show the messagedialog
        messagedialog.show()
    
    def create_result_card(self, answer:mr.MediathekViewWebAnswer) -> Gtk.Box:

        url = answer.get_best_vid_url()
        title = answer.get_title()
        description = answer.get_description()

        if len(description) > 50:
            description = description[:50] + "..."

        play_button = tools.new_button_with_icon("media-playback-start")

        def on_click(_ = None):
            if url is not None:
                self._main_window.start_player(url)
        
        play_button.connect("clicked", on_click)

        title_label = Gtk.Label()
        title_label.set_markup(f"<b>{title}</b>")
        title_label.set_justify(Gtk.Justification.LEFT)
        title_label.set_xalign(0)
        description_label = Gtk.Label()
        description_label.set_markup(description)
        description_label.set_justify(Gtk.Justification.LEFT)
        description_label.set_xalign(0)

        text_box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)

        text_box.pack_start(title_label, True, False, 0)
        text_box.pack_start(description_label, True, False, 0)
        
        

        card_content = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
        card_content.pack_start(text_box, True, True, 0)
        card_content.pack_start(play_button, False, False, 0)

        card = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        card.pack_start(card_content, True, True, 0)
        card.pack_end(Gtk.Separator(orientation = Gtk.Orientation.HORIZONTAL), False, False, 10)
        
        

        return card
    
    def clean_results(self):
        for result in self._current_search_cards:
            self._search_card_container.remove(result)
        
        self._current_search_cards = []
    
    def on_search(self, _) -> None:
        search_text = self._search_entry.get_text()

        req = mr.MediathekViewWebRequest(query=search_text)

        answers = req.perform_request()

        if answers is None:
            self.display_warning("error while performing the search request")
            return
        
        if len(answers) == 0:
            self.display_warning("no results found")
            return
        
        self.clean_results()
        for answer in answers:
            #print(answer)
            card = self.create_result_card(answer)
            self._current_search_cards.append(card)
            self._search_card_container.pack_start(card, False, False, 0)
        
        self.show_all()
        

        


