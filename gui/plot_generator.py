import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')


class PlotGenerator:
    def __init__(self, statistics):
        self._data = statistics
        self._histogram_path = 'images/stats/histogram.png'
        self._pie_chart_path = 'images/stats/pie_chart.png'

    @property
    def histogram_path(self):
        return self._histogram_path

    @property
    def pie_chart_path(self):
        return self._pie_chart_path

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, new_stats):
        self._data = new_stats

    def get_game_result(self, tie=True):
        if tie:
            return {key: self._data[key] for key in self._data if key != 'balance'}
        return {key: self._data[key] for key in self._data if key != 'balance' and key != 'tie'}

    def generate_game_result_histogram(self):
        bar_color = (38 / 255, 3 / 255, 21 / 255, 1)
        background_color = (240 / 255, 215 / 255, 135 / 255, 1)
        game_result = self.get_game_result()

        fig, ax = plt.subplots()
        ax.set_facecolor(background_color)
        ax.bar(list(game_result.keys()), game_result.values(), color=bar_color)
        ax.tick_params(axis='both', which='major', labelsize=20, colors=background_color)
        plt.savefig(self._histogram_path, transparent=True)
        plt.close()

    def incorrect_data(self):
        data = self.get_game_result(tie=True)
        return True if data['wins'] == 0 or data['losses'] == 0 else False

    def generate_game_result_pie_graph(self):
        if self.incorrect_data():
            return
        game_result = self.get_game_result(tie=False)
        labels = game_result.keys()
        sizes = game_result.values()
        colors = [(38 / 255, 3 / 255, 21 / 255, 1), (240 / 255, 215 / 255, 135 / 255, 1)]

        fig, ax = plt.subplots()
        wedges, texts, autotexts = ax.pie(sizes, colors=colors, labels=labels, autopct='%1.1f%%', startangle=90)
        idx = 1
        for text in autotexts:
            text.set_color(colors[idx % 2])
            text.set_fontsize(18)
            idx += 1
        for text in texts:
            text.set_color((240 / 255, 215 / 255, 135 / 255, 1))
            text.set_fontsize(20)
            idx += 1
        plt.savefig(self._pie_chart_path, transparent=True)
        plt.close()
