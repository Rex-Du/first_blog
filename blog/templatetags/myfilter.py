from django import template
register = template.Library()


@register.filter
def month_upper(key):
    return ['一','二','三','四','五','六'][key.month-1]

# @register.filter
# def month_upper(a=datetime.date.today()):
#     return ['一','二','三','四','五'][a.month-1]

# register.filter('month_upper',month_upper)


@register.filter
def label_class(value, arg):
    return value.label_tag(attrs={'class': arg})
