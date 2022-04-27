from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import SubmitField
from wtforms.validators import DataRequired


class StockForm(FlaskForm):
    name = StringField('Заголовок', validators=[DataRequired()])
    description = TextAreaField("Описание товара", validators=[DataRequired()])
    price = TextAreaField('Цена товара', validators=[DataRequired()])
    photo = StringField('Фотография товара')
    amount = StringField('Количество на складе', validators=[DataRequired()])
    submit = SubmitField('Применить')
