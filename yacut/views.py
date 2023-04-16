from flask import render_template, redirect, url_for, request

from . import app

from .forms import URLMapForm
from .utils import get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def index():
    form = URLMapForm()
    if request.method == 'POST' and form.validate_on_submit():
        short_id = form.custom_id.data or get_unique_short_id()
        return render_template('index.html', form=form, short_id=short_id)
    return render_template('index.html', form=form)
