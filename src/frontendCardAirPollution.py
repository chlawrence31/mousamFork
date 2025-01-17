import gi
import time

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk

from .frontendUiDrawPollutionBar import PollutionBar


class CardAirPollution:
    def __init__(self):
        from .weatherData import air_apllution_data, classify_aqi

        self.air_apllution_data = air_apllution_data
        self.classify_aqi = classify_aqi
        self.card = None
        self.create_card()

    def _get_nearest_time_index(self):

        for i in range(len(self.air_apllution_data["hourly"]["time"])):
            if (
                abs(time.time() - self.air_apllution_data["hourly"]["time"][i]) // 60
            ) < 30:
                nearest_current_time_idx = i
                break

        return nearest_current_time_idx

    def create_card(self):
        idx = self._get_nearest_time_index()

        card = Gtk.Grid(margin_top=10, margin_start=5)
        self.card = card
        card.halign = Gtk.Align.FILL
        card.set_row_spacing(5)
        card.set_css_classes(["view", "card", "custom_card"])

        # Main title of the card
        title = Gtk.Label(label="Air Pollution")
        title.set_hexpand(True)
        title.set_halign(Gtk.Align.START)
        title.set_css_classes(["text-4", "light-3", "bold"])
        card.attach(title, 0, 0, 4, 2)

        # Main value (like windspeed = 32km/h)
        info_box = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL, hexpand=True, halign=Gtk.Align.START
        )
        card.attach(info_box, 0, 2, 4, 2)
        info_box.set_margin_start(10)
        info_box.set_margin_top(30)

        main_val = Gtk.Label(label=self.air_apllution_data["hourly"]["us_aqi"][idx])
        main_val.set_css_classes(["text-l3", "bold"])
        main_val.set_halign(Gtk.Align.START)
        main_val.set_margin_end(10)
        info_box.append(main_val)

        desc = Gtk.Label(
            label=self.classify_aqi(self.air_apllution_data["hourly"]["us_aqi"][idx])
        )
        desc.set_css_classes(["text-3", "light-2", "bold-2"])
        desc.set_margin_bottom(10)
        desc.set_valign(Gtk.Align.END)
        desc.set_halign(Gtk.Align.START)
        info_box.append(desc)

        # Pollution bar
        aqi = self.air_apllution_data["hourly"]["us_aqi"][idx]
        bar_level = aqi / 600

        pollution_bar = PollutionBar(bar_level)
        # pollution_bar.set_margin_top()
        card.attach(pollution_bar, 0, 4, 4, 1)
