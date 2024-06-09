from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from blackjack_gui import MainMenuLayout, GameLayout


class BlackJackGUI(App):
    def build(self):
        self.screen_manager = ScreenManager()

        menu_page = MainMenuLayout(screen_manager=self.screen_manager)
        game_page = GameLayout(screen_manager=self.screen_manager)

        menu_screen = Screen(name="menu")
        menu_screen.add_widget(menu_page)
        self.screen_manager.add_widget(menu_screen)

        game_screen = Screen(name="game")
        game_screen.add_widget(game_page)
        self.screen_manager.add_widget(game_screen)

        return self.screen_manager


if __name__ == '__main__':
    BlackJackGUI().run()