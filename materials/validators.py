from django.core.exceptions import ValidationError
import re


class URLYouTubeValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):

        if value is None:
            return

        pattern = (
            r"^https://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)[\w-]+"
        )
        if isinstance(value, dict):
            tmp_value = value.get(self.field)
        else:
            tmp_value = value

        if tmp_value and not re.match(pattern, tmp_value):
            raise ValidationError(
                "Допускаются только HTTPS-ссылки на конкретные видео YouTube"
            )
