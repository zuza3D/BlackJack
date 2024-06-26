from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.stacklayout import StackLayout
from kivy.uix.widget import Widget

from gui.plot_generator import PlotGenerator
from gui.widgets import CustomButton, CustomLabel


class StatsLayout(GridLayout):
    def __init__(self, screen_manager, player_stats, **kwargs):
        super(StatsLayout, self).__init__(**kwargs)
        self.screen_manager = screen_manager
        self.player_stats = player_stats
        self.plot_generator = PlotGenerator(player_stats.stats)
        self.pie_chart_image = Image(source=self.plot_generator.pie_chart_path)
        self.histogram_image = Image(source=self.plot_generator.histogram_path)

        self.cols = 1

        self.navigation_bar = StackLayout(size_hint=(1, 0.2))

        self.back_button = CustomButton(text="menu".upper(), size_hint=(0.2, 1))
        self.back_button.bind(on_press=self.back_to_menu)
        self.navigation_bar.add_widget(self.back_button)

        self.refresh_button = CustomButton(text="refresh".upper(), size_hint=(0.2, 1))
        self.refresh_button.bind(on_press=self.refresh_plots)
        self.navigation_bar.add_widget(self.refresh_button)

        self.navigation_bar.add_widget(Widget(size_hint=(0.2, 1)))
        self.navigation_bar.add_widget(CustomLabel(text="Statistics".upper(), size_hint=(0.2, 1)))
        self.add_widget(self.navigation_bar)

        self.plot_panel = self.create_plot_panel()
        self.add_plots()

    def refresh_plots(self, _):
        Clock.schedule_once(lambda dt: self.update_plots())

    def back_to_menu(self, _):
        self.screen_manager.current = 'menu'

    def create_plot_panel(self):
        plot_panel = BoxLayout()
        plot_panel.orientation = 'horizontal'
        plot_panel.padding = 20
        plot_panel.spacing = 20
        return plot_panel

    def update_plots(self):
        self.plot_generator.generate_game_result_histogram()
        self.plot_generator.generate_game_result_pie_graph()
        self.pie_chart_image.reload()
        self.histogram_image.reload()

    def add_plots(self):
        self.update_plots()

        self.plot_panel.add_widget(self.pie_chart_image)
        self.plot_panel.add_widget(self.histogram_image)

        if self.plot_panel not in self.children:
            self.add_widget(self.plot_panel)
