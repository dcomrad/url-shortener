from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField, StringField
from wtforms.validators import URL, DataRequired, Optional

# нужен свой валидатор


class URLMapForm(FlaskForm):
    original_link = URLField(
        label='Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле'),
                    URL(message='Некорректная ссылка')]
    )
    custom_id = StringField(
        label='Ваш вариант короткой ссылки',
        validators=[Optional()]
    )
    submit = SubmitField('Создать')
