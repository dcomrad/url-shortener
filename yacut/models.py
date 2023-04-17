from datetime import datetime
from random import choice, randrange

from settings import Config

from . import db
from .exceptions import (BadIDException, BadOriginalLinkException,
                         NotUniqueIDException)

ALLOWED_SYMBOLS = [(48, 58), (65, 91), (97, 123)]  # 0-9, A-Z, a-z


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text, nullable=False)
    short = db.Column(db.Text, unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self, host) -> dict:
        return dict(
            url=self.original,
            short_link=host + self.short,
        )

    def from_dict(self, data):
        setattr(self, 'original', data.get('url', ''))
        setattr(self, 'short', data.get('custom_id', ''))

    @classmethod
    def add(cls, original_link: str, short_id: str):
        if not cls.check_original_link(original_link):
            raise BadOriginalLinkException()

        if short_id:
            if not cls.check_short_id(short_id):
                raise BadIDException()
            if not cls.is_unique(short_id):
                raise NotUniqueIDException()

        urlmap = cls(original=original_link,
                     short=short_id or cls.get_unique_short_id())
        db.session.add(urlmap)
        db.session.commit()
        return urlmap

    @classmethod
    def get(cls, short_id: str):
        urlmap = cls.query.filter_by(short=short_id).first()
        if not urlmap:
            raise BadIDException()

        return urlmap

    @classmethod
    def get_unique_short_id(cls, length=6) -> str:
        """Генерация уникального случайного ID."""
        buffer = []
        for _ in range(length):
            start, end = choice(ALLOWED_SYMBOLS)
            buffer.append(chr(randrange(start, end)))
        new_id = ''.join(buffer)

        if not cls.is_unique(new_id):
            return cls.get_unique_short_id()

        return new_id

    @classmethod
    def is_unique(cls, short_id: str) -> bool:
        """Проверка отсутствия в БД полученной короткой ссылки."""
        return not cls.query.filter_by(short=short_id).first()

    @staticmethod
    def check_original_link(original_link: str) -> bool:
        """Проверка оригинальной ссылки на допустимую длину."""
        return len(original_link) <= Config.ORIGINAL_LINK_LENGTH

    @staticmethod
    def check_short_id(short_id: str) -> bool:
        """Проверка короткой ссылки на допустимую длину и корректность."""
        if len(short_id) > Config.SHORT_ID_LENGTH:
            return False

        for char in short_id:
            is_ok = False
            for start, end in ALLOWED_SYMBOLS:
                if start <= ord(char) < end:
                    is_ok = True
            if not is_ok:
                return False

        return True
