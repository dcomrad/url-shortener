from flask import abort, redirect, render_template, request

from . import app, db
from .forms import URLMapForm
from .models import URLMap
from .utils import get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def index():
    form = URLMapForm()
    if request.method == 'POST' and form.validate_on_submit():
        short_id = form.custom_id.data or get_unique_short_id()
        urlmap = URLMap(original=form.original_link.data, short=short_id)
        db.session.add(urlmap)
        db.session.commit()
        return render_template('index.html', form=form,
                               short_url=request.base_url + short_id)

    return render_template('index.html', form=form)


@app.route('/<string:short_id>', methods=['GET'])
def short_url(short_id: str):
    urlmap = URLMap.query.filter_by(short=short_id).first() or abort(404)
    return redirect(urlmap.original)
