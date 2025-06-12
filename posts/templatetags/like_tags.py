from django import template
from posts.models import PostLike

register = template.Library()

@register.simple_tag
def is_liked(post, user):
    return PostLike.objects.filter(post=post, user=user, deleted=False).exists()
