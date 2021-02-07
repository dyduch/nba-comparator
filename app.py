from flask import Flask, render_template, request, redirect

from config import Config
from data.player_data import get_nba_data
from forms import CompareForm

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/', methods=['GET', 'POST'])
def compare_forms():
    form = CompareForm()

    player_data = []

    if request.method == 'POST':
        first_player_name = request.form.get('first_player_name')
        first_season_start = request.form.get('first_season_start')
        first_season_end = request.form.get('first_season_end')

        second_player_name = request.form.get('second_player_name')
        second_season_start = request.form.get('second_season_start')
        second_season_end = request.form.get('second_season_end')

        first_seasons = [str(i) for i in range(int(first_season_start), int(first_season_end)+1)]
        second_seasons = [str(i) for i in range(int(second_season_start), int(second_season_end)+1)]

        players_data = [get_nba_data(first_player_name, first_seasons),
                        get_nba_data(second_player_name, second_seasons)]

        return render_template('compare_players.html', players=players_data)

    return render_template('compare_form.html', form=form)


if __name__ == '__main__':
    app.run()
