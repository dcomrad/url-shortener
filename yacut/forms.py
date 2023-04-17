from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import (URL, DataRequired, Length, Optional,
                                ValidationError)

from settings import Config

from .models import URLMap


class Messages:
    MISSED_REQUIRED_FIELD = 'Заполните все обязательные поля'

    BAD_ORIGINAL_LINK = 'Некорректная длинная ссылка'
    TOO_LONG_ORIGINAL_LINK = ('Ссылка должна быть не более '
                              f'{Config.ORIGINAL_LINK_LENGTH} символов')

    BAD_ID = ('Некорректная короткая ссылка. Ссылка может содержать только '
              'цифры, маленькие и большие латинские буквы')
    NOT_UNIQUE_ID = 'Имя {} уже занято!'
    TOO_LONG_ID = (f'Ссылка должна быть не более {Config.SHORT_ID_LENGTH} '
                   'символов')


class URLMapForm(FlaskForm):
    original_link = URLField(
        label='Длинная ссылка*',
        validators=[DataRequired(message=Messages.MISSED_REQUIRED_FIELD),
                    Length(max=Config.ORIGINAL_LINK_LENGTH,
                           message=Messages.TOO_LONG_ORIGINAL_LINK),
                    URL(message=Messages.BAD_ORIGINAL_LINK)]
    )
    custom_id = StringField(
        label='Ваш вариант короткой ссылки',
        validators=[Length(max=Config.SHORT_ID_LENGTH,
                           message=Messages.TOO_LONG_ID),
                    Optional()]
    )
    submit = SubmitField('Создать')

    def validate_custom_id(self, field):
        if not URLMap.check_short_id(field.data):
            raise ValidationError(Messages.BAD_ID)

        if not URLMap.is_unique(field.data):
            raise ValidationError(Messages.NOT_UNIQUE_ID.format(field.data))
