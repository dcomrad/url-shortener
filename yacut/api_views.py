from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsageError
from .models import URLMap
from .utils import check_short_id, get_unique_short_id, is_unique


class Messages:
    NOT_FOUND = 'Указанный id не найден'
    LACK_OF_DEMANDED_FIELD = '"url" является обязательным полем!'
    BAD_ID = 'Указано недопустимое имя для короткой ссылки'
    EMPTY_REQUEST = 'Отсутствует тело запроса'
    NOT_UNIQUE_ID = 'Имя "{}" уже занято.'


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original(short_id: str):
    urlmap = URLMap.query.filter_by(short=short_id).first()
    if not urlmap:
        raise InvalidAPIUsageError(Messages.NOT_FOUND, 404)

    return jsonify({'url': urlmap.original}), 200


@app.route('/api/id/', methods=['POST'])
def add_short():
    data = request.get_json()

    if not data:
        raise InvalidAPIUsageError(Messages.EMPTY_REQUEST)

    if not data.get('url'):
        raise InvalidAPIUsageError(Messages.LACK_OF_DEMANDED_FIELD)

    if data.get('custom_id') and not check_short_id(data.get('custom_id')):
        raise InvalidAPIUsageError(Messages.BAD_ID, 400)

    if data.get('custom_id') and not is_unique(data.get('custom_id')):
        raise InvalidAPIUsageError(
            Messages.NOT_UNIQUE_ID.format(data.get('custom_id')), 400
        )

    data['custom_id'] = data.get('custom_id') or get_unique_short_id()

    urlmap = URLMap()
    urlmap.from_dict(data)
    db.session.add(urlmap)
    db.session.commit()
    return jsonify(urlmap.to_dict(request.host_url)), 201
