from django import template

register = template.Library()

@register.filter
def format_duration(seconds):
    seconds = int(seconds)

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    if hours > 0:
        return f"{hours} год {minutes} хв {secs} сек"
    elif minutes > 0:
        return f"{minutes} хв {secs} сек"
    else:
        return f"{secs} сек"