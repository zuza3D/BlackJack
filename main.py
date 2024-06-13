from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from gui.game_layout import GameLayout
from gui.main_menu_layout import MainMenuLayout
from stats.player_stats import PlayerStats
from gui.quiz_layout import QuizLayout
from gui.stats_layout import StatsLayout


class BlackJackGUI(App):
    def build(self):
        self.screen_manager = ScreenManager()
        self.player_stats = PlayerStats()

        menu_page = MainMenuLayout(screen_manager=self.screen_manager)
        game_page = GameLayout(screen_manager=self.screen_manager, player_stats=self.player_stats)
        quiz_page = QuizLayout(screen_manager=self.screen_manager)
        stats_page = StatsLayout(screen_manager=self.screen_manager, player_stats=self.player_stats)

        menu_screen = Screen(name="menu")
        menu_screen.add_widget(menu_page)
        self.screen_manager.add_widget(menu_screen)

        game_screen = Screen(name="game")
        game_screen.add_widget(game_page)
        self.screen_manager.add_widget(game_screen)

        quiz_screen = Screen(name="quiz")
        quiz_screen.add_widget(quiz_page)
        self.screen_manager.add_widget(quiz_screen)

        stats_screen = Screen(name="stats")
        stats_screen.add_widget(stats_page)
        self.screen_manager.add_widget(stats_screen)

        return self.screen_manager


if __name__ == '__main__':
    BlackJackGUI().run()
