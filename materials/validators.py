from django.core.exceptions import ValidationError
import re


class URLYouTubeValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):

        pattern = r"^https://(?:www\.)?youtube\.com/watch\?v=[\w-]+"
        tmp_value = dict(value).get(self.field)
        if not re.match(pattern, tmp_value):
            raise ValidationError(
                "Допускаются только HTTPS-ссылки на конкретные видео YouTube"
            )
