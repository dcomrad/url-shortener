from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import (URL, DataRequired, Length, Optional,
                                ValidationError)

from .utils import check_short_id, is_unique


class Messages:
    MISSED_REQUIRED_FIELD = 'Заполните все обязательные поля'
    BAD_ORIGINAL_ID = 'Некорректная длинная ссылка'

    BAD_ID = ('Некорректная короткая ссылка. Ссылка может содержать только '
              'цифры, маленькие и большие латинские буквы')
    NOT_UNIQUE_ID = 'Имя {} уже занято!'
    TOO_LONG_ID = 'Ссылка должна быть не более 16 символов'


class URLMapForm(FlaskForm):
    original_link = URLField(
        label='Длинная ссылка*',
        validators=[DataRequired(message=Messages.MISSED_REQUIRED_FIELD),
                    URL(message=Messages.BAD_ORIGINAL_ID)]
    )
    custom_id = StringField(
        label='Ваш вариант короткой ссылки',
        validators=[Length(1, 16, message=Messages.TOO_LONG_ID), Optional()]
    )
    submit = SubmitField('Создать')

    def validate_custom_id(self, field):
        if not check_short_id(field.data):
            raise ValidationError(Messages.BAD_ID)

        if not is_unique(field.data):
            raise ValidationError(Messages.NOT_UNIQUE_ID.format(field.data))
