from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsageError
from .exceptions import (BadIDException, BadOriginalLinkException,
                         NotUniqueIDException)
from .models import URLMap


class Messages:
    EMPTY_REQUEST = 'Отсутствует тело запроса'
    LACK_OF_DEMANDED_FIELD = '"url" является обязательным полем!'
    BAD_ID = 'Указано недопустимое имя для короткой ссылки'
    NOT_UNIQUE_ID = 'Имя "{}" уже занято.'
    NOT_FOUND = 'Указанный id не найден'
    BAD_ORIGINAL_LINK = 'Ссылка "{}" не является URL'


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original(short_id: str):
    try:
        urlmap = URLMap.get(short_id)
    except BadIDException:
        raise InvalidAPIUsageError(Messages.NOT_FOUND, 404)

    return jsonify({'url': urlmap.original}), 200


@app.route('/api/id/', methods=['POST'])
def add_short():
    data = request.get_json()

    if not data:
        raise InvalidAPIUsageError(Messages.EMPTY_REQUEST)
    if not data.get('url'):
        raise InvalidAPIUsageError(Messages.LACK_OF_DEMANDED_FIELD)

    try:
        urlmap = URLMap.add(data.get('url'), data.get('custom_id'))
    except BadIDException:
        raise InvalidAPIUsageError(Messages.BAD_ID, 400)
    except NotUniqueIDException:
        raise InvalidAPIUsageError(
            Messages.NOT_UNIQUE_ID.format(data.get('custom_id')), 400
        )
    except BadOriginalLinkException:
        raise InvalidAPIUsageError(
            Messages.BAD_ORIGINAL_LINK.format(data.get('url')), 400
        )

    return jsonify(urlmap.to_dict(request.host_url)), 201
