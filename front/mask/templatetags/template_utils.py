from django import template

from ..utils import get_alert

register = template.Library()


@register.filter
def show_alert(request):
    """
    Convert msg into raw html
    :param alert: dictionary with title and msg, type
    :type alert: dict
    :return: string of raw html
    """
    """
    PRIMARY     (blue)          primary
    NORMAL      (light black)   secondary
    SUCCESS     (green)         success
    DANGER      (red)           danger
    WARN        (yellow)        warning
    INFO        (light blue)    info
    HELP        (light gray)    light
    DARK        (black)         dark
    """
    alert = get_alert(request)

    if not alert:
        return ""
    else:

        TYPES = {
            "primary": "primary",
            "normal": "secondary",
            "success": "success",
            "danger": "danger",
            "warn": "warning",
            "info": "info",
            "help": "light",
            "dark": "dark"
        }

        msg = """
        <div class="alert alert-{type} alert-dismissible fade show" role="alert">
            <strong>{title}</strong>  {msg}
            <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                <span aria-hidden="true">&times;</span>
            </button>
        </div>
    """.format(
            type=TYPES[alert['type']],
            title=alert['title'],
            msg=alert['msg']
        )
    return msg
