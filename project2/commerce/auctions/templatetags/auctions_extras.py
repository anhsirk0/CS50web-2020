from django import template

register = template.Library()

@register.filter
def get_unseen(user):
    return len(user.notifications.filter(seen=False))


@register.filter
def get_date(time):
    return time.split(" ")[0]
