import email.message as em
import smtplib

import os

from flask import Flask, render_template, request, redirect, flash, session, Blueprint
from flask.helpers import url_for
from flask_login import login_required, current_user, login_user, logout_user

from datetime import timedelta
from itsdangerous import URLSafeTimedSerializer

from models import UserModel, ProjectsModel, db, login, CommentModel, FriendModel, InternshipModel
from dotenv import load_dotenv
import datetime 
import secrets

load_dotenv()

EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

def send_mail(TO, TOKEN):
    URL = "http://127.0.0.1:5000/authentication/reset/{}".format(TOKEN)
    msgstr = '''<table border="0" cellpadding="0" cellspacing="0" class="nl-container" role="presentation" style="background-color:#d9dffa" width="100%"><tbody><tr><td><table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-1" role="presentation" style="background-color:#09f" width="100%"><tbody><tr><td><table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content stack" role="presentation" style="color:#000" width="600"><tbody><tr><th class="column" style="font-weight:400;text-align:left;vertical-align:top;padding-top:20px;padding-bottom:0;border-top:0;border-right:0;border-bottom:0;border-left:0" width="100%"><table border="0" cellpadding="0" cellspacing="0" class="image_block" role="presentation" width="100%"><tr><td style="width:100%;padding-right:0;padding-left:0"><div align="center" style="line-height:10px"><img alt="Card Header with Border and Shadow Animated" class="big" src="https://d1oco4z2z1fhwp.cloudfront.net/templates/default/3991/animated_header.gif" style="display:block;height:auto;border:0;width:600px;max-width:100%" title="Card Header with Border and Shadow Animated" width="600"></div></td></tr></table></th></tr></tbody></table></td></tr></tbody></table><table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-2" role="presentation" style="background-color:#09f;background-position:top center" width="100%"><tbody><tr><td><table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content stack" role="presentation" style="background-color:#fff;color:#000" width="600"><tbody><tr><th class="column" style="font-weight:400;text-align:left;vertical-align:top;background-color:#fff;padding-left:50px;padding-right:50px;padding-top:15px;padding-bottom:15px;border-top:0;border-right:0;border-bottom:0;border-left:0" width="100%"><table border="0" cellpadding="10" cellspacing="0" class="text_block" role="presentation" style="word-break:break-word" width="100%"><tr><td><div style="font-family:sans-serif"><div style="font-size:14px;color:#09f;line-height:1.2;font-family:Helvetica Neue,Helvetica,Arial,sans-serif"><p style="margin:0;font-size:14px"><strong><span style="font-size:38px">Forgot your password?</span></strong></p></div></div></td></tr></table><table border="0" cellpadding="10" cellspacing="0" class="text_block" role="presentation" style="word-break:break-word" width="100%"><tr><td><div style="font-family:sans-serif"><div style="font-size:14px;color:#40507a;line-height:1.2;font-family:Helvetica Neue,Helvetica,Arial,sans-serif"><p style="margin:0;font-size:14px"><span style="font-size:16px">Hey, we received a request to reset your password.</span></p></div></div></td></tr></table><table border="0" cellpadding="10" cellspacing="0" class="text_block" role="presentation" style="word-break:break-word" width="100%"><tr><td><div style="font-family:sans-serif"><div style="font-size:14px;color:#40507a;line-height:1.2;font-family:Helvetica Neue,Helvetica,Arial,sans-serif"><p style="margin:0;font-size:14px"><span style="font-size:16px">Lets get you a new one!</span></p></div></div></td></tr></table><table border="0" cellpadding="0" cellspacing="0" class="button_block" role="presentation" width="100%"><tr><td style="padding-bottom:20px;padding-left:10px;padding-right:10px;padding-top:20px;text-align:left"><a href="{}" style="text-decoration:none;display:inline-block;color:#fff;background-color:#09f;border-radius:16px;width:auto;border-top:0 solid TRANSPARENT;border-right:0 solid TRANSPARENT;border-bottom:0 solid TRANSPARENT;border-left:0 solid TRANSPARENT;padding-top:8px;padding-bottom:8px;font-family:Helvetica Neue,Helvetica,Arial,sans-serif;text-align:center;word-break:keep-all" target="_blank"><span style="padding-left:25px;padding-right:20px;font-size:15px;display:inline-block;letter-spacing:normal"><span style="font-size:16px;line-height:2;word-break:break-word"><span data-mce-style="font-size: 15px; line-height: 30px;" style="font-size:15px;line-height:30px"><strong>RESET MY PASSWORD</strong></span></span></span></a></td></tr></table><table border="0" cellpadding="10" cellspacing="0" class="text_block" role="presentation" style="word-break:break-word" width="100%"><tr><td><div style="font-family:sans-serif"><div style="font-size:14px;color:#40507a;line-height:1.2;font-family:Helvetica Neue,Helvetica,Arial,sans-serif"><p style="margin:0;font-size:14px"><span style="font-size:14px">Having trouble?<a href="#" rel="noopener" style="text-decoration:none;color:#40507a" target="_blank" title="@socialaccount"><strong>@socialaccount</strong></a></span></p></div></div></td></tr></table><table border="0" cellpadding="10" cellspacing="0" class="text_block" role="presentation" style="word-break:break-word" width="100%"><tr><td><div style="font-family:sans-serif"><div style="font-size:14px;color:#40507a;line-height:1.2;font-family:Helvetica Neue,Helvetica,Arial,sans-serif"><p style="margin:0;font-size:14px">Didnt request a password reset? You can ignore this message.</p></div></div></td></tr></table></th></tr></tbody></table></td></tr></tbody></table><table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-3" role="presentation" style="background-color:#09f" width="100%"><tbody><tr><td><table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content stack" role="presentation" style="color:#000" width="600"><tbody><tr><th class="column" style="font-weight:400;text-align:left;vertical-align:top;padding-top:0;padding-bottom:5px;border-top:0;border-right:0;border-bottom:0;border-left:0" width="100%"><table border="0" cellpadding="0" cellspacing="0" class="image_block" role="presentation" width="100%"><tr><td style="width:100%;padding-right:0;padding-left:0"><div align="center" style="line-height:10px"><img alt="Card Bottom with Border and Shadow Image" class="big" src="https://d1oco4z2z1fhwp.cloudfront.net/templates/default/3991/bottom_img.png" style="display:block;height:auto;border:0;width:600px;max-width:100%" title="Card Bottom with Border and Shadow Image" width="600"></div></td></tr></table></th></tr></tbody></table></td></tr></tbody></table><table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-4" role="presentation" style="background-color:#09f" width="100%"><tbody><tr><td><table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content stack" role="presentation" style="color:#000" width="600"><tbody><tr><th class="column" style="font-weight:400;text-align:left;vertical-align:top;padding-left:10px;padding-right:10px;padding-top:10px;padding-bottom:20px;border-top:0;border-right:0;border-bottom:0;border-left:0" width="100%"><table border="0" cellpadding="10" cellspacing="0" class="text_block" role="presentation" style="word-break:break-word" width="100%"><tr><td><div style="font-family:sans-serif"><div style="font-size:14px;color:#000;line-height:1.2;font-family:Helvetica Neue,Helvetica,Arial,sans-serif"><p style="margin:0;font-size:14px;text-align:center"><span style="font-size:16px">This link will expire in the next 5 minutes.</span><br><span style="font-size:16px">Please feel free to contact us at email@up-learn.com.</span></p></div></div></td></tr></table></th></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table>'''.format(URL)
    msg = em.Message()
    msg['Subject'] = 'Password change request'
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(msgstr)
    s = smtplib.SMTP("smtp.outlook.com", 587)
    s.starttls()
    s.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    s.sendmail(EMAIL_ADDRESS, TO, msg.as_string())
    s.quit()

def getCurrentDate():
    current_time = datetime.datetime.now() 
    date = current_time.strftime("%d/%m/%Y")
    hour = current_time.hour
    minutes = current_time.minute
    return date + " " + str(hour) + ":" + str(minutes)