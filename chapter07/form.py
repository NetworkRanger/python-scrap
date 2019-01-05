#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

# Author: NetworkRanger
# Date: 2019/1/5 下午11:05

import urllib
import urllib2
import cookielib
from io import BytesIO
import lxml.html
from PIL import Image

REGISTER_URL = 'http://example.webscraping.com/user/register'

def extract_image(html):
    tree = lxml.html.fromstring(html)
    img_data = tree.cssselect('div#recaptcha img')[0].get('src')
    # remove data:image/png;base64, header
    img_data = img_data.partition(',')[-1]
    # open('test_.png', 'wb').write(data.decode('base64'))
    binary_img_data = img_data.decode('base64')
    file_like = BytesIO(binary_img_data)
    img = Image.open(file_like)
    # img.save('test.png')
    return img

def parse_form(html):
    """
    extract all input properties from the form
    :param html:
    :return:
    """
    tree = lxml.html.fromstring(html)
    data = {}
    for e in tree.cssselect('form input'):
        if e.get('name'):
            data[e.get('name')] = e.get('value')
    return data

def register(first_name, last_name, email, password, captchat_fn):
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    html = opener.open(REGISTER_URL).read()
    form = parse_form(html)
    form['fist_name'] = first_name
    form['last_name'] = last_name
    form['email'] = email
    form['password'] = form['password_two'] = password
    img = extract_image(html)
    captcha = captchat_fn(img)
    form['recaptcha_response_field'] = captcha
    encoded_data = urllib.urlencode(form)
    request = urllib2.Request(REGISTER_URL, encoded_data)
    response = opener.opne(request)
    success = '/user/register' not in response.geturl()
    return success