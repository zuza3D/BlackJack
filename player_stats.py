import os
import json


class PlayerStats:
    def __init__(self):
        self._stats_file = "player_stats.json"
        if os.path.exists(self._stats_file):
            self._player_stats = self._load_stats()
        else:
            self._player_stats = {"balance": 1000, "wins": 0, "losses": 0}
            self._save_stats()

    @property
    def stats(self):
        return self._player_stats

    @property
    def balance(self):
        return self._player_stats['balance']

    @balance.setter
    def balance(self, new_balance):
        self._player_stats['balance'] = new_balance
        self._save_stats()

    def _load_stats(self):
        if os.path.exists(self._stats_file):
            try:
                with open(self._stats_file, 'r') as file:
                    return json.load(file)
            except json.JSONDecodeError:
                return {"balance": 1000, "wins": 0, "losses": 0}

    def _save_stats(self):
        with open(self._stats_file, 'w') as file:
            json.dump(self._player_stats, file)

    def update_stats(self, result, bet, blackjack=False):
        print(result)
        if result['player']:
            if blackjack:
                self._player_stats['balance'] += bet
            self._player_stats["balance"] += 2 * bet
            self._player_stats["wins"] += 1
        elif result['dealer']:
            self._player_stats["losses"] += 1
        else:
            self._player_stats["balance"] += bet
        self._save_stats()

    def show_statistics(self):
        return f"Wins: {self._player_stats['wins']} \nLosses: {self._player_stats['losses']}"

    def reset_statistics(self):
        self._player_stats = {"balance": 1000, "wins": 0, "losses": 0}
        self._save_stats()