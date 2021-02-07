from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired


class CompareForm(FlaskForm):
    first_player_name = StringField('First Player Name', validators=[DataRequired()])
    first_season_start = IntegerField('First Player From Season', validators=[DataRequired()])
    first_season_end = IntegerField('First Player To Season', validators=[DataRequired()])

    second_player_name = StringField('Second Player Name', validators=[DataRequired()])
    second_season_start = IntegerField('Second Player From Season', validators=[DataRequired()])
    second_season_end = IntegerField('Second Player To Season', validators=[DataRequired()])
    submit = SubmitField('Compare')
