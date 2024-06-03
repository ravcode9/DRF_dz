import re
from rest_framework import serializers


def validate_link(value):
    """
    Проверяет ведет ли ссылка только на youtube.com.
    """
    youtube_url = r'^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+$'
    if not re.match(youtube_url, value):
        raise serializers.ValidationError("Ссылки на сторонние ресурсы запрещены. Допустимы только ссылки на youtube.com.")
    return value
