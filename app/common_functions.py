import base64
import hashlib
import locale
import re
from datetime import datetime, date
import os
import random
import string
import calendar;
import time;

from Crypto.Cipher import AES
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
# from django.utils.decorators import available_attrs
from django.http import HttpResponseRedirect
from functools import wraps
from django.utils.timezone import now



def make_pagination_html(query_string, current_page, total_pages):
    pagination_string = ""

    if total_pages == 1:
        return pagination_string

    if current_page > 1:
        pagination_string += '<li><a href="?page=%s&%s">Previous</a></li>' % (current_page - 1, query_string)
        value = current_page - 1
    else:
        value = current_page

    count_limit = 1

    while value <= total_pages and count_limit < 6:
        if value == current_page:
            pagination_string += "<li class='active'><a href='?page=%s&%s'>%s</a></li>" % (
                current_page, query_string, current_page)
        else:
            pagination_string += "<li><a href='?page=%s&%s'>%s</a></li>" % (value, query_string, value)

        value += 1
        count_limit += 1

    if current_page < total_pages:
        pagination_string += '<li><a href="?page=%s&%s">Next</a></li>' % (current_page + 1, query_string)

    return pagination_string


def handle_uploaded_file_local(file, path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)

        image_ext = file.name.split('.')
        name = image_ext[len(image_ext) - len(image_ext)]
        image_ext = image_ext[len(image_ext) - 1]

        with open(path + file.name, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
            destination.close()

        image_encript = hashlib.md5((file.name).encode()).hexdigest()

        new_filename = str(name) + '-' + str(image_encript) + '.' + image_ext

        os.rename(path + file.name, path + new_filename)

        return new_filename
    except Exception:
        return path + settings.DEFAULT_PROFILE_PICT


def upload_file(file, path, name_user, type):
    try:
        if not os.path.exists(path):
            os.makedirs(path)

        ts = calendar.timegm(time.gmtime())

        file_ext = file.name.split('.')
        file_ext = file_ext[len(file_ext) - 1]

        with open(path + file.name, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
            destination.close()

        new_filename = str(name_user) + '-' + str(ts) + '-' + str(type) + '.' + file_ext

        os.rename(path + file.name, path + new_filename)

        return new_filename
    except Exception:
        return path + settings.DEFAULT_PROFILE_PICT


def uploads(directory, file):
    static_dir = '/static/uploads/' + directory + '/'
    path_dir = settings.BASE_DIR + static_dir

    if not os.path.exists(path_dir):
        os.makedirs(path_dir)

    ts = calendar.timegm(time.gmtime())
    file_ext = file.name.split('.')

    file_name = file_ext[len(file_ext) - len(file_ext)]
    file_ext = file_ext[len(file_ext) - 1]

    with open(path_dir + file.name, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()

    new_filename = str(file_name) + '-' + str(ts) + '.'  + file_ext
    filename = static_dir + new_filename
    os.rename(path_dir + file.name, path_dir + new_filename)

    return filename


def check_type_file(files, tipe, url):
    try:
        type = ['jpg', 'jpeg', 'pdf', 'png', 'doc', 'docx']
        file_ext = files.name.split('.')
        file_ext = file_ext[len(file_ext) - 1]
        if file_ext not in type:
            response = redirect(reverse(str(url)))
            response.set_cookie('error_msg', 'Tipe file ' + tipe + ' yang anda masukkan tidak support.', max_age=2)
        return response
    except Exception:
        pass


def from_dob_to_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def password_generator():
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    size = random.randint(8, 12)
    return ''.join(random.choice(chars) for x in range(size))


def convert_datestr_to_datetime(date_str):

    date_split = date_str.split('/')
    year = date_split[2].replace(' ', '')
    month = date_split[1].replace(' ', '')
    date = date_split[0].replace(' ', '')

    new_date_str = '{y}-{m}-{d}'.format(y=year, m=month, d=date)
    new_date = datetime.strptime(new_date_str, '%Y-%m-%d')

    return new_date


def convert_datehtml_to_datetime(date_str):

    date_split = date_str.split('-')
    year = date_split[0].replace(' ', '')
    month = date_split[1].replace(' ', '')
    date = date_split[2].replace(' ', '')

    new_date_str = '{y}-{m}-{d}'.format(y=year, m=month, d=date)
    new_date = datetime.strptime(new_date_str, '%Y-%m-%d')

    return new_date


def get_date_range(date_str, range):

    date_split = date_str.split('-')
    year = date_split[0].replace(' ', '')
    month = date_split[1].replace(' ', '')
    date = date_split[2].replace(' ', '')

    year = int(year) - int(range)

    print(year)

    new_date_str = '{y}-{m}-{d}'.format(y=year, m=month, d=date)
    new_date = datetime.strptime(new_date_str, '%Y-%m-%d')

    return new_date


CIPHER = AES.new(b'N1pP0n_3xpre5s_1')


def aes_encrypt(s):
    pad = (16 - len(s) % 16) * ' '
    cipher = base64.b64encode(CIPHER.encrypt("{}{}".format(s, pad))).decode()
    return base64.b64encode(cipher.encode('utf-8'))


def aes_decrypt(e):

    decode_cipher = base64.b64decode(e).decode('utf-8')
    return CIPHER.decrypt(base64.b64decode(decode_cipher)).rstrip().decode()


def number_format(num, places=0):
    return locale.format("%.*f", (places, num), True)


def validate_user_entry_menu(id_action_menu):
    def real_decorator(view_func):
        @wraps(view_func)
        def wrap(request, *args, **kwargs):

            false_respon = HttpResponseRedirect(reverse('dashboard'))
            msg_1 = 'Forbidden to access current menu'

            if not request.user.is_staff:
                false_respon.set_cookie('error_msg', msg_1, max_age=2)
                return false_respon

            menu_list = request.session['menu']
            if id_action_menu not in menu_list:
                false_respon.set_cookie('error_msg', msg_1, max_age=2)
                return false_respon
            return view_func(request, *args, **kwargs)
        return wrap
    return real_decorator


def password_check(password):
    """
    Verify the strength of 'password'
    Returns a dict indicating the wrong criteria
    A password is considered strong if:
        8 characters length or more
        1 digit or more
        1 symbol or more
        1 uppercase letter or more
        1 lowercase letter or more
    """

    # calculating the length
    length_error = len(password) < 8

    # searching for digits
    digit_error = re.search(r"\d", password) is None

    # searching for uppercase
    uppercase_error = re.search(r"[A-Z]", password) is None

    # searching for lowercase
    lowercase_error = re.search(r"[a-z]", password) is None

    # searching for symbols
    symbol_error = re.search(r"\W", password) is None

    # overall result
    password_ok = not ( length_error or digit_error or uppercase_error or lowercase_error or symbol_error )

    return {
        'password_ok' : password_ok,
        'length_error' : length_error,
        'digit_error' : digit_error,
        'uppercase_error' : uppercase_error,
        'lowercase_error' : lowercase_error,
        'symbol_error' : symbol_error,
    }
