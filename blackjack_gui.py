from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


class BlackJackGUI(App):

    def build(self):
        layout = BoxLayout(orientation='vertical')
        label = Label(text="BlackJack")
        play_button = Button(text="Play")
        statistics_button = Button(text="Player statistics")
        exit_button = Button(text="Exit")

        layout.add_widget(label)
        layout.add_widget(play_button)
        layout.add_widget(statistics_button)
        layout.add_widget(exit_button)
        return layout


BlackJackGUI().run()