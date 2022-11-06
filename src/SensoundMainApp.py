from kivy.core.text import Label
import pickle
import datetime
import os
import re
import wave
from datetime import date

from kivy.properties import ObjectProperty
import matplotlib.pyplot as plt
import mysql.connector
import numpy as np
import pyaudio
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from plyer import filechooser

import emotion_classify2
import preprocess_separate_recognize_clear_function1
import preprocessing_functions1

# from pydub import AudioSegment


helpstr = '''
ScreenManager:
    WelcomeScreen:
    EmailScreen:
    UserNameScreen:
    PasswordScreen:
    RecordScreen:
    SignInScreen:
    MainScreen:
    FeelingScreen:
    FeelingInfoScreen:
<WelcomeScreen>:
    name : 'welcomescreen'
    MDLabel:
        text:'Welcome To'
        font_style: 'H2'
        halign: 'center'
        pos_hint: {'center_y':0.8}
    Image :
        source : "newlogo.png"
        #opacity : .9
        pos_hint: {"center_x": .5, "center_y": .55}
        size_hint : .7,.7
    MDFloatingActionButton:
        id:disabled_button
        icon: 'account-plus'
        md_bg_color:app.theme_cls.primary_color
        pos_hint: {'center_x':0.35,'center_y':0.25}
        user_font_size : '35sp'
        on_press:
            root.manager.current = 'emailscreen'
            root.manager.transition.direction = 'left'
    MDLabel:
        text:'Sign up'
        font_style: 'H6'
        pos_hint: {'center_x':0.81,'center_y':0.15}
    MDFloatingActionButton:
        id:disabled_button
        icon: 'account-arrow-left'
        md_bg_color:app.theme_cls.primary_color
        pos_hint: {'center_x':0.65,'center_y':0.25}
        user_font_size : '35sp'
        on_press:
            root.manager.current = 'signinscreen'
            root.manager.transition.direction = 'left'
    MDLabel:
        text:'Sign in'
        font_style: 'H6'
        pos_hint: {'center_x':1.11,'center_y':0.15}
<EmailScreen>
    name:'emailscreen'
    MDFloatingActionButton:
        icon: 'arrow-left'
        md_bg_color:app.theme_cls.primary_color
        pos_hint: {'center_x':0.1,'center_y':0.1}
        user_font_size : '45sp'
        on_press:
            root.manager.current = 'welcomescreen'
            root.manager.transition.direction = 'right'
    MDFloatingActionButton:
        id:disabled_button
        disabled: True
        icon: 'arrow-right'
        md_bg_color:app.theme_cls.primary_color
        pos_hint: {'center_x':0.9,'center_y':0.1}
        user_font_size : '45sp'
        on_press:
            root.manager.current = 'usernamescreen'
            root.manager.transition.direction = 'left'
    MDProgressBar:
        value:25
        pos_hint: {'center_y':0.02}
    MDLabel:
        text:'Email Address'
        font_style: 'H2'
        halign: 'center'
        pos_hint : {'center_y':0.8}
    MDTextField:
        id:email
        pos_hint: {'center_x':0.5,'center_y':0.6}
        size_hint: (0.7,0.1)
        hint_text : 'Email'
        helper_text: 'Required'
        helper_text_mode: 'on_error'
        icon_right: 'account'
        icon_right_color: app.theme_cls.primary_color
        required : True
    MDFloatingActionButton:
        icon:'account-plus'
        md_bg_color:app.theme_cls.primary_color
        pos_hint: {'center_x':0.5,'center_y':0.2}
        user_font_size: '35sp'
        on_press: app.checkEmail()
    MDBoxLayout:
        orientation : 'vertical'
        Image :
            source : "newlogo.png"
            opacity : .05
            pos_hint: {'center_x': .5,'center_y':0.3}
            size_hint : .7,.7
<UserNameScreen>:
    name:'usernamescreen'
    MDFloatingActionButton:
        icon: 'arrow-left'
        md_bg_color:app.theme_cls.primary_color
        pos_hint: {'center_x':0.1,'center_y':0.1}
        user_font_size : '45sp'
        on_press:
            root.manager.current = 'emailscreen'
            root.manager.transition.direction = 'right'
    MDFloatingActionButton:
        id:disabled_button
        disabled: True
        icon: 'arrow-right'
        md_bg_color:app.theme_cls.primary_color
        pos_hint: {'center_x':0.9,'center_y':0.1}
        user_font_size : '45sp'
        on_press:
            root.manager.current = 'passwordscreen'
            root.manager.transition.direction = 'left'
    MDProgressBar:
        value:50
        pos_hint: {'center_y':0.02}
    MDLabel:
        text:'User Details'
        font_style: 'H2'
        halign: 'center'
        pos_hint : {'center_y':0.85}
    MDTextField:
        id:username
        pos_hint: {'center_x':0.5,'center_y':0.7}
        size_hint: (0.7,0.1)
        hint_text : 'username'
        helper_text: 'Required'
        helper_text_mode: 'on_error'
        icon_right: 'account'
        icon_right_color: app.theme_cls.primary_color
        required : True
    MDTextField:
        id:dob
        pos_hint: {'center_x':0.5,'center_y':0.6}
        size_hint: (0.7,0.1)
        hint_text : 'Date of Birth'
        helper_text: 'Required in form DD-MM-YYYY'
        helper_text_mode: 'on_focus'
        icon_right: 'account'
        icon_right_color: app.theme_cls.primary_color
        required : True
    MDTextField:
        id:gender
        pos_hint: {'center_x':0.5,'center_y':0.5}
        size_hint: (0.7,0.1)
        hint_text : 'Gender'
        helper_text: 'Male/Female/Other'
        helper_text_mode: 'on_focus'
        icon_right: 'account'
        icon_right_color: app.theme_cls.primary_color
    ######
# # BoxLayout:
#     Label:
#         text: "Gender:"
#         font_size:16
# 
#     GridLayout:
#         cols:2
# 
#         Label:
#             text: "Male"
#             font_size:16
#         CheckBox:
#             group: "genders"
#             on_active: root.checkbox_click(self, self.active, "Male")
# 
#         Label:
#             text: "Female"
#             font_size:16
#         CheckBox:
#             group: "genders"
#             on_active: root.checkbox_click(self, self.active, "Female")
# 
#         Label:
#             text: "Other"
#             font_size:16
#         CheckBox:
#             group: "genders"
#             on_active: root.checkbox_click(self, self.active, "Other")
    MDTextField:
        id:country
        pos_hint: {'center_x':0.5,'center_y':0.4}
        size_hint: (0.7,0.1)
        hint_text : 'Country'
        icon_right: 'account'
        icon_right_color: app.theme_cls.primary_color
    MDFloatingActionButton:
        icon:'account-plus'
        md_bg_color:app.theme_cls.primary_color
        pos_hint: {'center_x':0.5,'center_y':0.2}
        user_font_size: '35sp'
        on_press: app.check_user_details()

    MDBoxLayout:
        orientation : 'vertical'
        Image :
            source : "newlogo.png"
            opacity : .05
            pos_hint: {'center_x': .5,'center_y':0.3}
            size_hint : .7,.7
    MDFloatingActionButton:
        icon:'arrow-left'
        md_bg_color:app.theme_cls.primary_color
        pos_hint: {'center_x':0.1,'center_y':0.1}
        user_font_size: '45sp'
        on_press: root.manager.current = 'emailscreen'
            root.manager.transition.direction = 'left'

<PasswordScreen>:
    name : 'passwordscreen'
    MDFloatingActionButton:
        icon: 'arrow-left'
        md_bg_color:app.theme_cls.primary_color
        pos_hint: {'center_x':0.1,'center_y':0.1}
        user_font_size : '45sp'
        on_press:
            root.manager.current = 'usernamescreen'
            root.manager.transition.direction = 'right'
    MDFloatingActionButton:
        id:disabled_button
        disabled: True
        icon: 'arrow-right'
        md_bg_color:app.theme_cls.primary_color
        pos_hint: {'center_x':0.9,'center_y':0.1}
        user_font_size : '45sp'
        on_press:
            # app.insertValue()
            root.manager.current = 'recordscreen'
            root.manager.transition.direction = 'left'
    MDProgressBar:
        value:75
        pos_hint: {'center_y':0.02}
    MDLabel:
        text:'Choose Password'
        font_style: 'H2'
        halign: 'center'
        pos_hint : {'center_y':0.8}
    MDTextField:
        id:password1
        pos_hint: {'center_x':0.5,'center_y':0.6}
        size_hint: (0.7,0.1)
        hint_text : 'password'
        helper_text: 'Required'
        helper_text_mode: 'on_error'
        icon_right: 'eye-off'
        password : True
        icon_right_color: app.theme_cls.primary_color
        required : True
    MDTextField:
        id:password2
        pos_hint: {'center_x':0.5,'center_y':0.5}
        size_hint: (0.7,0.1)
        hint_text : 'Verify password'
        helper_text: 'Required'
        password : True
        helper_text_mode: 'on_error'
        icon_right: 'eye-off'
        icon_right_color: app.theme_cls.primary_color
        required : True

    MDFloatingActionButton:
        icon:'account-plus'
        md_bg_color:app.theme_cls.primary_color
        pos_hint: {'center_x':0.5,'center_y':0.2}
        user_font_size: '35sp'
        on_press: app.checkPassword()

    MDBoxLayout:
        orientation : 'vertical'
        Image :
            source : "newlogo.png"
            opacity : .05
            pos_hint: {'center_x': .5,'center_y':0.3}
            size_hint : .7,.7
    MDFloatingActionButton:
        icon:'arrow-left'
        md_bg_color:app.theme_cls.primary_color
        pos_hint: {'center_x':0.1,'center_y':0.1}
        user_font_size: '45sp'
        on_press: root.manager.current = 'usernamescreen'
            root.manager.transition.direction = 'left'

<RecordScreen>:
    name : 'recordscreen'
    MDFloatingActionButton:
        icon: 'arrow-left'
        md_bg_color:app.theme_cls.primary_color
        pos_hint: {'center_x':0.1,'center_y':0.1}
        user_font_size : '45sp'
        on_press:
            root.manager.current = 'passwordscreen'
            root.manager.transition.direction = 'right'
    MDFloatingActionButton:
        id:disabled_button
        disabled: True
        icon: 'arrow-right'
        md_bg_color:app.theme_cls.primary_color
        pos_hint: {'center_x':0.9,'center_y':0.1}
        user_font_size : '45sp'
        on_press:
            app.insertValue()
            root.manager.current = 'mainscreen'
            root.manager.transition.direction = 'left'
    MDProgressBar:
        value:100
        pos_hint: {'center_y':0.02}
    MDLabel:
        text:'Please insert a short record'
        font_style: 'H2'
        halign: 'center'
        pos_hint : {'center_y':0.8}

    MDLabel:
        text:'Please make sure you are in a quiet environment.\\n Press on the record button, wait 2 seconds and then say three times:\\n In Australia, my voice identifies me'
        font_style: 'H5'
        halign: 'center'
        pos_hint : {'center_y':0.6}

    MDFloatingActionButton:
        icon:'record-rec'
        pos_hint: {'center_x':0.5,'center_y':0.3}
        user_font_size: '50sp'
        background_color: (1, 0, 0, 0)
        #### define a function of record
        on_press:             
            app.get_record()

    MDBoxLayout:
        orientation : 'vertical'
        Image :
            source : "newlogo.png"
            opacity : .05
            pos_hint: {'center_x': .5,'center_y':0.3}
            size_hint : .7,.7

<SignInscreen>:
    name : 'signinscreen'
    MDFloatingActionButton:
        icon: 'arrow-left'
        md_bg_color:app.theme_cls.primary_color
        pos_hint: {'center_x':0.1,'center_y':0.1}
        user_font_size : '45sp'
        on_press:
            root.manager.current = 'welcomescreen'
            root.manager.transition.direction = 'right'
    MDFloatingActionButton:
        id:disabled_button
        disabled: True
        icon: 'arrow-right'
        md_bg_color:app.theme_cls.primary_color
        pos_hint: {'center_x':0.9,'center_y':0.1}
        user_font_size : '45sp'
        on_press:
            # app.username_changer()
            root.manager.current = 'mainscreen'
            root.manager.transition.direction = 'left'
    MDLabel:
        text:'Sign in'
        font_style: 'H2'
        halign: 'center'
        pos_hint : {'center_y':0.8}
    MDTextField:
        id:email
        pos_hint: {'center_x':0.5,'center_y':0.6}
        size_hint: (0.7,0.1)
        hint_text : 'Email'
        helper_text: 'Required'
        helper_text_mode: 'on_error'
        icon_right: 'account'
        icon_right_color: app.theme_cls.primary_color
        required : True
    MDTextField:
        id:password
        pos_hint: {'center_x':0.5,'center_y':0.5}
        size_hint: (0.7,0.1)
        hint_text : 'Password'
        helper_text: 'Required'
        password : True
        helper_text_mode: 'on_error'
        icon_right: 'eye-off'
        icon_right_color: app.theme_cls.primary_color
        required : True
    MDFloatingActionButton:
        icon:'account-plus'
        md_bg_color:app.theme_cls.primary_color
        pos_hint: {'center_x':0.5,'center_y':0.2}
        user_font_size: '35sp'
        on_press: app.checkDetailsSignin()
    MDBoxLayout:
        orientation : 'vertical'
        Image :
            source : "newlogo.png"
            opacity : .05
            pos_hint: {'center_x': .5,'center_y':0.3}
            size_hint : .7,.7
<MainScreen>:
    name : 'mainscreen'
    MDLabel:
        id:profile_name
        text: 'Welcome to Sensound'
        font_style : 'H2'
        halign : 'center'
        pos_hint : {'center_y':0.85}
    MDLabel:
        id:profile_name
        text: '“It’s really how you speak—not just what you say—that matters for conveying emotion.” —Michael Kraus, a psychologist at the Yale School of Management.'
        font_style : 'H6'
        halign : 'center'
        pos_hint : {'center_y':0.65}
    MDLabel:
        id:profile_name
        text: 'Please upload a phone call'
        font_style : 'H6'
        halign : 'center'
        pos_hint : {'center_y':0.4}
    MDBoxLayout:
        orientation : 'vertical'
        Image :
            source : "newlogo.png"
            opacity : .05
            pos_hint: {'center_x': .5,'center_y':0.3}
            size_hint : .7,.7
    MDFloatingActionButton:
        id:disabled_button
        disabled: True
        icon: 'arrow-right'
        md_bg_color:app.theme_cls.primary_color
        pos_hint: {'center_x':0.9,'center_y':0.1}
        user_font_size : '45sp'
        on_press:
            root.manager.current = 'feelingscreen'
            root.manager.transition.direction = 'left'

    MDRaisedButton:
        text: "Upload"
        md_bg_color: app.theme_cls.primary_color
        height: 30
        pos_hint: {'center_x':0.5,'center_y':0.3}
        on_release: app.fileChooser()
<FeelingScreen>
    name : 'feelingscreen'
    MDLabel:
        id:profile_name
        text: 'Your feelings distribution is: '
        font_style : 'H4'
        halign : 'center'
        pos_hint : {'center_y':0.9}
    MDBoxLayout:
        orientation : 'vertical'
        Image :
            source : "currPie.png"
            pos_hint: {'center_x': .5,'center_y':0.3}
            size_hint : .55,.55
    MDFloatingActionButton:
        icon: 'arrow-right'
        md_bg_color:app.theme_cls.primary_color
        pos_hint: {'center_x':0.9,'center_y':0.1}
        user_font_size : '45sp'
        on_press:
            app.pop_up_emotion()
            root.manager.current = 'feelinginfoscreen'
            root.manager.transition.direction = 'left'
    MDFloatingActionButton:
        icon: 'arrow-left'
        md_bg_color:app.theme_cls.primary_color
        pos_hint: {'center_x':0.1,'center_y':0.1}
        user_font_size : '45sp'
        on_press:
            root.manager.current = 'mainscreen'
            root.manager.transition.direction = 'right'

<FeelingInfoScreen>
    name : 'feelinginfoscreen'
    MDLabel:
        id:profile_name
        text: 'Did you know?'
        font_style : 'H4'
        halign : 'center'
        pos_hint : {'center_y':0.9}

    MDBoxLayout:
        orientation : 'vertical'
        Image :
            source : "newlogo.png"
            opacity : .05
            pos_hint: {'center_x': .5,'center_y':0.3}
            size_hint : .7,.7
    MDFloatingActionButton:
        icon: 'arrow-left'
        md_bg_color:app.theme_cls.primary_color
        pos_hint: {'center_x':0.1,'center_y':0.1}
        user_font_size : '45sp'
        on_press:
            root.manager.current = 'feelingscreen'
            root.manager.transition.direction = 'right'
'''


class WelcomeScreen(Screen):
    pass


class EmailScreen(Screen):
    pass


class UserNameScreen(Screen):
    pass


class PasswordScreen(Screen):
    pass


class RecordScreen(Screen):
    pass


class SignInScreen(Screen):
    pass


class MainScreen(Screen):
    pass


class FeelingScreen(Screen):
    pass


class FeelingInfoScreen(Screen):
    pass


sm = ScreenManager()
sm.add_widget(WelcomeScreen(name='welcomescreen'))
sm.add_widget(EmailScreen(name='emailscreen'))
sm.add_widget(UserNameScreen(name='usernamescreen'))
sm.add_widget(PasswordScreen(name='passwordscreen'))
sm.add_widget(RecordScreen(name='recordscreen'))
sm.add_widget(SignInScreen(name='signinscreen'))
sm.add_widget(MainScreen(name='main_screen'))
sm.add_widget(FeelingScreen(name='feelingscreen'))
sm.add_widget(FeelingInfoScreen(name='feelinginfoscreen'))
email_pattern = "^[a-zA-Z0-9-_]+[\._]?[A-Z a-z 0-9]+@[a-zA-Z0-9]+\.[a-z]+[\._]?[a-z]{2,3}$"



"""
Function that will calculate the age by the date of birth
"""
def calculateAge(birthDate):
    today = date.today()
    age = today.year - birthDate.year - ((today.month, today.day) <
                                         (birthDate.month, birthDate.day))
    return age


class NewApp(MDApp):
    def build(self):
        self.strng = Builder.load_string(helpstr)
        self.title = 'Sensound'
        return self.strng

    """
    check if the email address is valid and that the field is full.
    if not- than an error window will pop up
    If the mail is already exist in the DB than an error window will pop up
    """

    def checkEmail(self):
        self.email = self.strng.get_screen('emailscreen').ids.email.text
        email_check_false = True
        emailExist = NewApp.checkEmailExist(self)
        try:
            int(self.email)
        except:
            email_check_false = False
        if email_check_false or self.email.split() == []:
            cancel_btn_email_dialogue = MDFlatButton(text='Retry', on_release=self.close_email_dialogue)
            self.dialog = MDDialog(title='This field is required', text="Please enter an Email address",
                                   size_hint=(0.7, 0.2),
                                   buttons=[cancel_btn_email_dialogue])
            self.dialog.open()
        elif self.email:
            if emailExist:
                cancel_btn_password_dialogue = MDFlatButton(text='Retry', on_release=self.close_username_dialogue)
                self.dialog = MDDialog(title='Email exists', text="This email is already exist in the database."
                                                                  "\n Please log in or enter another email address",
                                       size_hint=(0.7, 0.2),
                                       buttons=[cancel_btn_password_dialogue])
                self.dialog.open()
            elif not re.match(email_pattern, self.email):
                cancel_btn_email_dialogue = MDFlatButton(text='Retry', on_release=self.close_email_dialogue)
                self.dialog = MDDialog(title='Invalid Email', text="Please enter a valid Email address",
                                       size_hint=(0.7, 0.2),
                                       buttons=[cancel_btn_email_dialogue])
                self.dialog.open()
            else:

                self.strng.get_screen('emailscreen').ids.disabled_button.disabled = False

    """
    check that the fields of user name and date of birth are filled
    if not, it will raise an error window.
    this function also check that the user age is above 16.
    country and age fields are allowed
    """

    def check_user_details(self):
        self.username_text = self.strng.get_screen('usernamescreen').ids.username.text
        self.dateBirth = self.strng.get_screen('usernamescreen').ids.dob.text
        self.gender = self.strng.get_screen('usernamescreen').ids.gender.text
        self.country = self.strng.get_screen('usernamescreen').ids.country.text
        valid_gender = ['male', 'Male', 'Female', 'female', 'Other', 'other', '']
        username_check_false = True
        username_age_false = True
        try:
            int(self.username_text)
        except:
            username_check_false = False
        if username_check_false or self.username_text.split() == []:
            cancel_btn_username_dialogue = MDFlatButton(text='Retry', on_release=self.close_username_dialogue)
            self.dialog = MDDialog(title='Invalid user name', text="Please enter a valid user name",
                                   size_hint=(0.7, 0.2),
                                   buttons=[cancel_btn_username_dialogue])
            self.dialog.open()
        else:
            splitDob = self.dateBirth.split("-")
            s = [str(integer) for integer in splitDob]
            a_string = "".join(s)
            # for i in range(len(splitDob)):
            #     if a_string[0] == "0":
            #         new_string = int(a_string[i + 1:])
            # if a_string.isalpha() or not isinstance(new_string, int):
            if not a_string.isalpha() or a_string != "":
                username_age_false = False

            if len(splitDob) != 3 or username_age_false or self.dateBirth.split() == []:
                cancel_btn_username_dialogue = MDFlatButton(text='Retry', on_release=self.close_username_dialogue)
                self.dialog = MDDialog(title='Invalid Date of birth',
                                       text="Please enter a valid date in a DD-MM-YYYY format", size_hint=(0.7, 0.2),
                                       buttons=[cancel_btn_username_dialogue])
                self.dialog.open()
            else:
                self.date_time_obj = (datetime.datetime.strptime(self.dateBirth, '%d-%m-%Y')).date()
                if calculateAge(self.date_time_obj) < 16:
                    cancel_btn_username_dialogue = MDFlatButton(text='Retry', on_release=self.close_username_dialogue)
                    self.dialog = MDDialog(title='You are not in the right age',
                                           text="You must be 16 years old in order to use Sensound",
                                           size_hint=(0.7, 0.2),
                                           buttons=[cancel_btn_username_dialogue])
                    self.dialog.open()
                else:
                    if self.gender in valid_gender:
                        self.strng.get_screen('usernamescreen').ids.disabled_button.disabled = False
                    else:
                        cancel_btn_username_dialogue = MDFlatButton(text='Retry',
                                                                    on_release=self.close_username_dialogue)
                        self.dialog = MDDialog(title='Gender is not valid',
                                               text="You can choose to enter a gender. "
                                                    "\nIf you choose so then fill one of this options: Male/Female/Other."
                                                    "\nElse - keep it empty",
                                               size_hint=(0.7, 0.2),
                                               buttons=[cancel_btn_username_dialogue])
                        self.dialog.open()

    """
    verify that the passwords are the same
    """
    def checkPassword(self):
        self.password1 = self.strng.get_screen('passwordscreen').ids.password1.text
        self.password2 = self.strng.get_screen('passwordscreen').ids.password2.text
        password_check_false = True
        try:
            int(self.password1)
        except:
            password_check_false = False
        if password_check_false or self.password1.split() == [] or self.password2.split() == []:
            cancel_btn_password_dialogue = MDFlatButton(text='Retry', on_release=self.close_username_dialogue)
            self.dialog = MDDialog(title='Enter password', text="Please input a password", size_hint=(0.7, 0.2),
                                   buttons=[cancel_btn_password_dialogue])
            self.dialog.open()

        else:
            if self.password1 != self.password2:
                cancel_btn_password_dialogue = MDFlatButton(text='Retry', on_release=self.close_username_dialogue)
                self.dialog = MDDialog(title='Verification failed',
                                       text="Please enter the same password in both fields", size_hint=(0.7, 0.2),
                                       buttons=[cancel_btn_password_dialogue])
                self.dialog.open()
            else:
                self.strng.get_screen('passwordscreen').ids.disabled_button.disabled = False

    """
    returns True if the email is already exist in the DB
    """

    def checkEmailExist(self):
        self.email = self.strng.get_screen('emailscreen').ids.email.text
        email, password = NewApp.getEmailPassSignin(self)
        if self.email == email:
            return True
        else:
            return False

    """
    check that the fields in the Sign in window are filled.
    if not- will pop up an error window.
    Also, check if the user mail exists in the DB.
    if Yes- it verifies that the password is correct
    if not- will pop up an error window.
    """
    def checkDetailsSignin(self):
        self.email = self.strng.get_screen('signinscreen').ids.email.text
        self.password = self.strng.get_screen('signinscreen').ids.password.text
        email_check_false = True
        self.login_check = False
        try:
            int(self.email)
        except:
            email_check_false = False
        if email_check_false or self.email.split() == [] or self.password.split() == []:
            cancel_btn_email_dialogue = MDFlatButton(text='Retry', on_release=self.close_email_dialogue)
            self.dialog = MDDialog(title='These fields are required', text="Please fill all the fields",
                                   size_hint=(0.7, 0.2),
                                   buttons=[cancel_btn_email_dialogue])
            self.dialog.open()
        elif self.email and self.password:
            curr_email, curr_password = NewApp.getEmailPassSignin(self)
            if not curr_email:
                cancel_btn_email_dialogue = MDFlatButton(text='Retry', on_release=self.close_email_dialogue)
                self.dialog = MDDialog(title='This email does not exist in the data base', text="Please sign up",
                                       size_hint=(0.7, 0.2),
                                       buttons=[cancel_btn_email_dialogue])
                self.dialog.open()
            else:
                if curr_password == self.password:
                    self.strng.get_screen('signinscreen').ids.disabled_button.disabled = False
                else:
                    cancel_btn_email_dialogue = MDFlatButton(text='Retry', on_release=self.close_email_dialogue)
                    self.dialog = MDDialog(title='Incorrect password', text="Please try again",
                                           size_hint=(0.7, 0.2),
                                           buttons=[cancel_btn_email_dialogue])
                    self.dialog.open()
        else:
            self.login_check = True
            self.strng.get_screen('signinscreen').ids.disabled_button.disabled = False

    def close_email_dialogue(self, obj):
        self.dialog.dismiss()

    def close_username_dialogue(self, obj):
        self.dialog.dismiss()

    """
    Connect to the DB
    """
    def connectToDB(self):
        conn = mysql.connector.connect(user='sensoundAdmin',
                                       host='sensound-mysql.cnlubimbgubt.eu-west-2.rds.amazonaws.com',
                                       password='Technion2022',
                                       database='mysql')
        return conn

    """
    Insert user's Details to the DB after Sign in
    """
    def insertValue(self):
        conn = NewApp.connectToDB(self)
        mycursor = conn.cursor()
        sqlInsert = "INSERT INTO sensound.Users (username, password, email, DateOfBirth, gender, country,User_Features) VALUES (%s, %s, %s, %s, %s, %s,%s)"
        val = (self.username_text, self.password1, self.email, self.date_time_obj, self.gender, self.country,
               str(self.emotion_list[0]))
        mycursor.execute(sqlInsert, val)
        conn.commit()
        print("End inserting")
        mycursor.close()
        conn.close()


    """
    Checks if the user's details in the sign in window are exist in the DB.
    If yes so return them.
    """
    def getEmailPassSignin(self):
        conn = NewApp.connectToDB(self)
        mycursor = conn.cursor()
        select_email = "SELECT email, password from sensound.Users where email= %s"
        val = self.email
        email, password = False, False
        mycursor.execute(select_email, (val,))
        records = mycursor.fetchall()
        # mycursor.close()
        # conn.close()
        if len(records) == 0:
            return email, password
        else:
            for row in records:
                email = row[0]
                password = row[1]
        return email, password

    """
    Allows the user recording his\her voice in order to analyzing their voice features.
    after the recording has finished, it will be analyzing by the extract_feature function and
    returns the user's features.
    """
    def get_record(self):
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 8000
        RECORD_SECONDS = 8
        WAVE_OUTPUT_FILENAME = "userRecord.wav"

        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        frames = []

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        recordSucceeded = MDFlatButton(text='continue', on_release=self.close_username_dialogue)
        self.dialog = MDDialog(title='Record has finished', text="Your recording has successfully upload!",
                               size_hint=(0.7, 0.2),
                               buttons=[recordSucceeded])
        self.dialog.open()
        print("* done recording")

        stream.stop_stream()
        stream.close()
        p.terminate()
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        self.user_features = preprocessing_functions1.extract_feature(WAVE_OUTPUT_FILENAME, mfcc=True, chroma=True,
                                                                      mel=True).reshape(1, -1)
        # self.emotion_list = np.array((self.user_features).tolist())
        self.emotion_list = (self.user_features).tolist()
        self.strng.get_screen('recordscreen').ids.disabled_button.disabled = False
        return self.user_features

    def dismiss_popup(self):
        self._popup.dismiss()

    """
    Allows the user to upload a file to the App from the file explorer
    """
    def fileChooser(self):
        filechooser.open_file(on_selection=self.finally_selected_converted)

    def finally_selected_converted(self, selection):
        if selection:
            self.wavFile = selection[0]
            if self.wavFile:
                np_feature_tuple = NewApp.convertFinalFeatureType(self)
                wavName = (os.path.split(self.wavFile))[1]
                preprocess_separate_recognize_clear_function1.separation_and_recognition(wavName, np_feature_tuple)
                print("finally selected")
                select_raya = NewApp.selectedRecordAnalyzing(self, "clear_recording.wav")
                return select_raya

    """
    This function organizes the user's features voice that was retrieve from the DB to the correct shape.
    It deletes the characters [ or ] or , or ) or ( or ' or \n that exist in the value that inserted to the DB
    """
    def convertingFeature(self, user_feature):
        haf_str = str(user_feature)
        list = []
        for i in haf_str:
            if i == "[" or i == "]" or i == "\n" or i == "," or i == ")" or i == "(" or i == "'":
                continue
            list.append(i)
        import re
        str1 = ''.join(list)
        splited = re.split('  | ', str1)
        arr = np.array(splited)
        new = []
        for i in arr:
            if i == "":
                continue
            new.append(i)
        return new

    """
    converts the user's features type from string (that is how it kept in the DB) to numpy.ndarraay
    """
    def convertFinalFeatureType(self):
        conn = NewApp.connectToDB(self)
        mycursor = conn.cursor()
        curr_email = self.email
        sql = "SELECT User_Features FROM sensound.Users where email = %s"
        mycursor.execute(sql, (curr_email,))
        self.records = mycursor.fetchall()
        self.good = NewApp.convertingFeature(self, self.records)
        float_list = []
        for i in self.good:
            float_list.append(float(i))
        tuplearray = np.array([(float_list)])
        return tuplearray

    def selectedRecordAnalyzing(self, selection):
        if selection:
            self.wavFile = selection[0]
            if self.wavFile:
                emotions = emotion_classify2.emo_chart(selection)
                totalEmotions = ['neutral', 'happy', 'sad', 'angry', 'fearful']
                listEmo = [0, 0, 0, 0, 0]
                for emotion in totalEmotions:
                    if emotion in emotions[0]:
                        indexTotalEmotions = totalEmotions.index(emotion)
                        indexLables = emotions[0].index(emotion)
                        listEmo[indexTotalEmotions] = emotions[1][indexLables]
                self.neutral = listEmo[0]
                self.happy = listEmo[1]
                self.sad = listEmo[2]
                self.angry = listEmo[3]
                self.fearful = listEmo[4]
                # maxvalue = max(emotions[1])
                self.maxemotion = emotions[2]
                self.emotioninformation = NewApp.identifyEmotion(self)
                # idx, emotion, self.header, self.info = NewApp.identifyEmotion(self)
                self.strng.get_screen('mainscreen').ids.disabled_button.disabled = False
                plt.pie(emotions[1], labels=emotions[0], startangle=90, autopct='%1.1f%%')
                plt.legend(loc="best")
                plt.axis('equal')
                plt.tight_layout()
                plt.savefig('currPie.png')
                plt.show()

    """
    insert to DB the feelings that was identified in the records according to the exact time now
    """
    def insertFeelingsToDB(self):
        conn = NewApp.connectToDB(self)
        mycursor = conn.cursor()
        nowDate = date.today()
        self.formatted_date = nowDate.strftime('%Y-%m-%d %H:%M:%S')
        sqlInsert = "INSERT INTO sensound.UsersEmotions (DateOfRecord, email, neutral, happy, sad, angry,fearful) VALUES (%s, %s, %s, %s, %s, %s,%s)"
        val = (self.formatted_date, self.email, self.neutral, self.happy, self.sad, self.angry, self.fearful)
        mycursor.execute(sqlInsert, val)
        conn.commit()


    """
    chooses a fact randomly from the DB about the identified dominant value
    """
    def identifyEmotion(self):
        conn = NewApp.connectToDB(self)
        mycursor = conn.cursor()
        val = self.maxemotion
        sql = "SELECT * FROM sensound.feelingsInfo where feelingType = %s ORDER BY RAND() LIMIT 1"
        mycursor.execute(sql, (val,))
        records = mycursor.fetchall()
        return list(records[0])
    """
    Pops up a window that shows what is the dominant feeling of the user and a fact about it
    """
    def pop_up_emotion(self):
        idx, emotion, header, info = NewApp.identifyEmotion(self)
        self.dialog = MDDialog(title='Your dominant feeling is: ' + emotion, text=header + "\n" + info,
                               size_hint=(0.7, 0.2))
        self.dialog.open()

NewApp().run()
