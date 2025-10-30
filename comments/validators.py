from html.parser import HTMLParser
from rest_framework import serializers

ALLOWED_TAGS = ['a', 'code', 'i', 'strong']

class TagValidator(HTMLParser):
    def __init__(self):
        super().__init__()
        self.unallowed_tags = []

    def handle_starttag(self, tag, attrs):
        if tag not in ALLOWED_TAGS:
            self.unallowed_tags.append(tag)

    def handle_endtag(self, tag):
        if tag not in ALLOWED_TAGS:
            self.unallowed_tags.append(tag)

def validate_allowed_html(value):
    parser = TagValidator()
    try:
        parser.feed(value)
        parser.close()
    except Exception:
        raise serializers.ValidationError("Malformed HTML detected.")

    if parser.unallowed_tags:
        raise serializers.ValidationError(
            f"Tags {set(parser.unallowed_tags)} are not allowed."
        )

    return value
