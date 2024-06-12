from kivy.uix.boxlayout import BoxLayout
from gui.widgets import TitleLabel,  CenteredButton


class MainMenuLayout(BoxLayout):
    def __init__(self, screen_manager, **kwargs):
        super(MainMenuLayout, self).__init__(**kwargs)
        self.screen_manager = screen_manager

        self.padding = 20
        self.spacing = 20

        self.orientation = 'vertical'

        self.add_widget(TitleLabel("BlackJack"))

        # Add "Play" button and bind to start_game
        self.play_button = CenteredButton(text="Play".upper())
        self.play_button.bind(on_press=self.start_game)
        self.add_widget(self.play_button)

        # Add "Practise" button
        self.practise_button = CenteredButton(text="Practise basic strategy".upper())
        self.practise_button.bind(on_press=self.start_quiz)
        self.add_widget(self.practise_button)

        # Add "Statistic" button
        self.statistics_button = CenteredButton(text="Player statistics".upper())
        self.statistics_button.bind(on_press=self.show_statistic)
        self.add_widget(self.statistics_button)

        # Add "Exit" button
        self.exit_button = CenteredButton(text="Exit".upper())
        self.add_widget(self.exit_button)

    def start_game(self, _):
        self.screen_manager.current = 'game'

    def show_statistic(self, _):
        self.screen_manager.current = 'stats'

    def start_quiz(self, _):
        self.screen_manager.current = 'quiz'
