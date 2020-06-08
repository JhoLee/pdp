import bcrypt


def encrypt(pw):
    """
    Hash with 'bcrypt' with salt
    :param pw: String to hash.
    :return: Hashed byte
    """
    salt = bcrypt.gensalt()
    password = pw.encode('utf-8')
    hashed = bcrypt.hashpw(password, salt)

    return hashed.decode('utf-8')


def check_pw(input_pw, hashed_pw):
    """
    Check input_pw with hashed pw.
    :param input_pw: pw from user
    :param hashed_pw: hashed pw from DB
    :return: If match True, or False.
    """
    return bcrypt.checkpw(input_pw.encode('utf-8'), hashed_pw.encode('utf-8'))


def set_alert(request, msg, title="", type="INFO"):
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
    request.session['alert'] = {
        'title': title,
        'msg': msg,
        'type': type.lower()
    }


def get_alert(request):
    if 'alert' in request.session.keys():
        alert = request.session['alert']
        request.session['alert'] = None
        return alert
    else:
        return None
