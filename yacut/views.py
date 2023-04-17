from flask import abort, redirect, render_template, request

from . import app
from .exceptions import (BadIDException, BadOriginalLinkException,
                         NotUniqueIDException)
from .forms import URLMapForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index():
    form = URLMapForm()

    if request.method == 'GET' or not form.validate_on_submit():
        return render_template('index.html', form=form)

    try:
        urlmap = URLMap.add(form.original_link.data, form.custom_id.data)
    except (BadIDException, NotUniqueIDException, BadOriginalLinkException):
        # Валидация данных осуществляется в forms.py.
        # Если выполнение кода дошло сюда, в приложении присутствует ошибка.
        abort(500)

    return render_template('index.html', form=form,
                           short_url=request.base_url + urlmap.short)


@app.route('/<string:short_id>', methods=['GET'])
def short_url(short_id: str):
    try:
        urlmap = URLMap.get(short_id)
    except BadIDException:
        abort(404)

    return redirect(urlmap.original)
