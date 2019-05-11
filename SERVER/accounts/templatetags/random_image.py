import random
from django import template

register = template.Library()

# 참고링크 : https://docs.djangoproject.com/en/2.2/howto/custom-template-tags/

@register.simple_tag
def image_num():
    return random.randint(1, 47)
