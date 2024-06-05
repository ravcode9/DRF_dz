import re
from rest_framework import serializers


class YouTubeLinkValidator:
    """
    Валидатор для проверки ссылок, ведущих только на youtube.com.
    """
    def __init__(self, message=None):
        if message is None:
            self.message = "Ссылки на сторонние ресурсы запрещены. Допустимы только ссылки на youtube.com."
        else:
            self.message = message

    def __call__(self, value):
        youtube_url = r'^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+$'
        if not re.match(youtube_url, value):
            raise serializers.ValidationError(self.message)
        return value
