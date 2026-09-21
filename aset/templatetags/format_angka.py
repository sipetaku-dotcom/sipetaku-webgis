from django import template

register = template.Library()


@register.filter
def format_ribuan(value):

    if value in (
        None,
        ''
    ):
        return '0'

    try:

        angka = int(
            float(value)
        )

        return (
            f'{angka:,}'
            .replace(',', '.')
        )

    except (
        ValueError,
        TypeError
    ):

        return value