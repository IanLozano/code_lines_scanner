from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, SelectField, HiddenField,
                     PasswordField, TextAreaField, BooleanField)
from wtforms.validators import (DataRequired, Email, Length,
                                EqualTo,NoneOf, AnyOf)


# PIP INSTALL FLASK-WTF WTFORMS EMAIL-VALIDATOR


class EmailFooterForm(FlaskForm):
    
    
    email = StringField("email", validators = [DataRequired(), Email(), Length(min=12, max=30)],
                        render_kw = {"placeholder": "Sign up for updates...", "class_": "email-sign-up"})
    
    submit = SubmitField("Submit", render_kw = {"class_": "email-sign-up"})
    
    

class RegisterForm(FlaskForm):
    
    username = StringField("first name", validators = [DataRequired(),
                                                     Length(min=3, max=22)], 
                           
                           render_kw = {"placeholder":"Enter your first name...", "class_": "username"})
    
    last_name = StringField("last name", validators = [DataRequired(),
                                                     Length(min=3, max=22)], 
                            
                            render_kw = {"placeholder":"Enter your last name...", "class_": "last_name"})
    
    
    
    
    
    # Email() checks for the @ symbol, if not there, invalid form
    email = StringField("email", 
                validators = [DataRequired(),Email(),
                 Length(min=8, max=30)], 
                        render_kw = {"placeholder":"Enter a email...", "class_": "email"})
    
    
    password = PasswordField("password", 
                validators = [DataRequired(),Length(min=8, max=20)],
                     render_kw = {"placeholder":"Enter a password...", "class_": "password"})
    
    confirm_password = PasswordField("confirm password", 
                 validators = [DataRequired(),
                   EqualTo("password", message="Passwords must match!")],
                 render_kw = {"placeholder":"Enter a confirm password...", "class_": "confirm_password"})
    
    submit = SubmitField("Sign-up")
    
    
    
class LoginPopupForm(FlaskForm):

    # Email() checks for the @ symbol, if not there, invalid form
    login_email = StringField("login_email", 
            validators = [DataRequired(),Email(),
             Length(min=8, max=30)], 
                    render_kw = {"placeholder":"Enter a email..."})

    login_password = PasswordField("login_password", 
            validators = [DataRequired(),Length(min=8, max=20)],
                 render_kw = {"placeholder":"Enter a password..."})

    login_submit = SubmitField("Login")

    
    
    
class LoginForm(FlaskForm):

    # Email() checks for the @ symbol, if not there, invalid form
    email = StringField("email", 
            validators = [DataRequired(),Email(),
             Length(min=8, max=30)], 
                    render_kw = {"placeholder":"Enter a email..."})

    password = PasswordField("password", 
            validators = [DataRequired(),Length(min=8, max=20)],
                 render_kw = {"placeholder":"Enter a password..."})

    submit = SubmitField("Login")


class RequestTokenForm(FlaskForm):
    
    email = StringField("email", 
        validators = [DataRequired(),Email(),
        Length(min=8, max=30)], 
        render_kw = {"placeholder":"Enter a email..."})

    submit = SubmitField("Request Token")
    

    
    
    
    

class ResetPasswordForm(FlaskForm):
   
    password = PasswordField("password", 
            validators = [DataRequired(),Length(min=3, max=20)],
            render_kw = {"placeholder":"Enter a password..."})

    confirm_password = PasswordField("confirm_password", 
            validators = [DataRequired(),
            EqualTo("password", message="Passwords must match!")],
            render_kw = {"placeholder":"Enter a confirm_password..."})
    
    submit = SubmitField("Reset Password")
    
    
    
    
    
    
    
    
    
    
###################################################################
######### CONTACT PAGE ##########################################
###################################################################
class ContactUserForm(FlaskForm):
    

    query = TextAreaField("query", validators = [DataRequired(), Length(min=10, max= 400)],
                         render_kw = {"placeholder": "Please keep the query clear and concise. Thank you."})
    
    
    
    reason = SelectField("Reason for email",
                         validators = [DataRequired()],
                         choices = [("1", "can't access course I paid for"),
                                    ("2", "lecture video won't load/start"),
                                    ("3", "how can I get a refund?"),
                                    ("4", "how can I become a paid instructor?"),
                                    ("5", "can I find more about the people behind Holistic Python?"),
                                    ("6", "can I discuss a business with Holistic Python?"),
                                    ("7", "other")])
    
    
    
    submit = SubmitField("Submit")
    
    
    
    

    
    
class ContactVisitorForm(FlaskForm):
    
    
    email = StringField("email", validators = [DataRequired(), Email(), Length(min=10, max=30)],
                        render_kw = {"placeholder": "Enter a valid email..."})
    
    query = TextAreaField("query", validators = [DataRequired(), Length(min=10, max=500)],
                          render_kw = {"placeholder": "Please keep the query clear and concise. Thank you."})
    
    first_name = StringField("first name", validators = [DataRequired(), Length(min=2, max=28)],
                             render_kw = {"placeholder": "Please enter a valid first name..."})
    

    
    last_name = StringField("last name", validators = [DataRequired(), Length(min=2, max=28)],
                             render_kw = {"placeholder": "Please enter a valid last name..."})
    
    
    reason = SelectField("Reason for email",
                         validators = [DataRequired()],
                         choices = [("1", "How can I become a paid instructor?"),
                                    ("2", "Can I discuss a business venture?"),
                                    ("3", "Do you offer your services?"),
                                    ("4", "other")])
    
    submit = SubmitField("Submit")
                         
                                    
class AdminLoginForm(FlaskForm):

    # Email() checks for the @ symbol, if not there, invalid form
    email = StringField("email", 
            validators = [DataRequired(),Email(),
             Length(min=8, max=35)], 
                    render_kw = {"placeholder":"Enter a email..."})

    pin = PasswordField("pin", 
            validators = [DataRequired(),Length(min=5, max=6)],
                 render_kw = {"placeholder":"Enter secret"})
    
    role = StringField("role", validators = [DataRequired(), Length(min=4, max=20)],
                       render_kw = {"placeholder":"Enter role"})

    submit = SubmitField("Login")

    
    
    
    
    
    
    
class CommentForm(FlaskForm):
    
    
    comment = TextAreaField("Comment", validators = [DataRequired(),
                                               Length(min=4, max=200)],
                    
                         render_kw = {"placeholder": "Add a comment..."})
    
    submit = SubmitField("Comment")
    
    
    

class RequestTokenForm(FlaskForm):
    
    email = StringField("email", 
        validators = [DataRequired(),Email(),
        Length(min=8, max=30)], 
        render_kw = {"placeholder":"Enter a email..."})

    submit = SubmitField("Request Token")
    

    
    
    
    

class ResetPasswordForm(FlaskForm):
   
    password = PasswordField("password", 
            validators = [DataRequired(),Length(min=3, max=20)],
            render_kw = {"placeholder":"Enter a password..."})

    confirm_password = PasswordField("confirm_password", 
            validators = [DataRequired(),
            EqualTo("password", message="Passwords must match!")],
            render_kw = {"placeholder":"Enter a confirm_password..."})
    
    submit = SubmitField("Reset Password")
    
    
    
    
    
class RefundForm(FlaskForm):
    
    reason = TextAreaField("Comment", validators = [Length(min=3, max=250), DataRequired()],
                           render_kw = {"placeholder": "Comment why you wanted a refund? This helps us help you for future courses. Thank you :)"})
    
    choose = SelectField("Main reason for requesting a refund?",
                         validators = [DataRequired()],
                         choices = [("1", "videos won't load"),
                                    ("2", "inaccurate information"),
                                    ("3", "content was boring"),
                                    ("4", "too expensive"),
                                    ("5", "not enough content"),
                                    ("6", "found a better course"),
                                    ("7", "didn't meet my expectations"),
                                    ("8", "no reason really")])
    
    submit = SubmitField("Request Refund")
    
    
    
    
    
class RefundSubForm(FlaskForm):
    
    reason = TextAreaField("Comment", validators = [Length(min=3, max=300), DataRequired()],
                           render_kw = {"placeholder": "Please comment why you want a refund? This helps us help you for future courses. Thank you :)"})
    
    choose = SelectField("Main reason for requesting a refund?",
                         validators = [DataRequired()],
                         choices = [("1", "videos won't load"),
                                    ("2", "inaccurate information"),
                                    ("3", "content was boring"),
                                    ("4", "too expensive"),
                                    ("5", "not enough content"),
                                    ("6", "found a better courses"),
                                    ("7", "didn't meet my expectations"),
                                    ("8", "no reason really"),
                                   ("9", "want to change subscription")])
    
    submit = SubmitField("Request Refund")
    
    
    
    
    
    
    
    
class CancelSubForm(FlaskForm):
    
    reason = TextAreaField("Comment", validators = [Length(min=3, max=300), DataRequired()],
                           render_kw = {"placeholder": "Please comment why you want to cancel your subscription? This helps us help you for future courses. Thank you :)"})
    
    choose = SelectField("Main reason for requesting a cancellation?",
                         validators = [DataRequired()],
                         choices = [("1", "videos won't load"),
                                    ("2", "inaccurate information"),
                                    ("3", "content was boring"),
                                    ("4", "too expensive"),
                                    ("5", "not enough content"),
                                    ("6", "found a better courses"),
                                    ("7", "didn't meet my expectations"),
                                    ("8", "no reason really"),
                                   ("9", "want to change subscription")])
    
    submit = SubmitField("Request Cancel")
    
    
    
    
    
    
class RegisterVisitorForm(FlaskForm):
    
    username = StringField("first name", validators = [DataRequired(),
                                                     Length(min=3, max=22)], 
                           
                           render_kw = {"placeholder":"Enter your first name...", "class_": "username"})
    
    last_name = StringField("last name", validators = [DataRequired(),
                                                     Length(min=3, max=22)], 
                            
                            render_kw = {"placeholder":"Enter your last name...", "class_": "last_name"})
    
    
    
    
    
    # Email() checks for the @ symbol, if not there, invalid form
    email = StringField("email", 
                validators = [DataRequired(),Email(),
                 Length(min=8, max=30)], 
                        render_kw = {"placeholder":"Enter a email...", "class_": "email"})
    
    
    password = StringField("password", 
                validators = [DataRequired(),Length(min=8, max=20)],
                     render_kw = {"placeholder":"Enter a password...", "class_": "password"})
    
    confirm_password = StringField("confirm password", 
                 validators = [DataRequired(),
                   EqualTo("password", message="Passwords must match!")],
                 render_kw = {"placeholder":"Enter a confirm password...", "class_": "confirm_password"})
    
    submit = SubmitField("Sign-up")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
###################################################################
######### CONTACT PAGE ##########################################
###################################################################
class ContactForm(FlaskForm):
    

    
    
     
    query = TextAreaField("query", validators = [DataRequired(), Length(min=10, max= 400)],
                         render_kw = {"placeholder": "Please keep the query clear and concise. Thank you."})
    
    
    
    reason = SelectField("Reason for email",
                         validators = [DataRequired()],
                         choices = [("1", "can't access course I paid for"),
                                    ("2", "lecture video won't load/start"),
                                    ("3", "how can I get a refund?"),
                                    ("4", "how can I become a paid instructor?"),
                                    ("5", "can I find more about the people behind Holistic Python?"),
                                    ("6", "can I discuss a business with Holistic Python?"),
                                    ("7", "other")])
    
    
    
    submit = SubmitField("Submit")
    

      
    
    
    
class ContactVisitorForm(FlaskForm):
    
    
    email = StringField("email", validators = [DataRequired(), Email(), Length(min=8, max=28)],
                           render_kw = {"placeholder": "Enter a email..."})
    
    
     
    query = TextAreaField("query", validators = [DataRequired(), Length(min=10, max= 400)],
                         render_kw = {"placeholder": "Please keep the query clear and concise. Thank you."})
    
    first_name = StringField("first name", validators=[DataRequired(), Length(min = 2, max= 25)],
                             render_kw = {"placeholder":"Please enter a valid first name..."})
    
    last_name = StringField("last name", validators=[DataRequired(), Length(min = 2, max= 25)],
                             render_kw = {"placeholder":"Please enter a valid last name..."})
    
    
    
    
    reason = SelectField("Reason for email",
                         validators = [DataRequired()],
                         choices = [("1", "can't access course I paid for"),
                                    ("2", "lecture video won't load/start"),
                                    ("3", "my certificate is missing"),
                                    ("4", "how can I become a paid instructor?"),
                                    ("5", "can I find more about the people behind Holistic Python?"),
                                    ("6", "can I discuss a business with Holistic Python?"),
                                    ("7", "other")])
    
    
    
    submit = SubmitField("Submit")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
class FreeForm(FlaskForm):
    
    
    submit = SubmitField("Enroll")
    
    
    
    
    
class RegisterEnrollForm(FlaskForm):
    
    
    
    hidden_course = HiddenField("course_id")
    
    username = StringField("username", validators = [DataRequired(), Length(min=3, max=25)],
                           render_kw = {"placeholder": "Enter a username..."})
    
    
    last_name = StringField("last_name", validators = [DataRequired(), Length(min=3, max=25)],
                           render_kw = {"placeholder": "Enter a last name..."})
    

    
    email = StringField("email", validators = [DataRequired(), Email(), Length(min=8, max=28)],
                           render_kw = {"placeholder": "Enter a email..."})
    
    password = PasswordField("password", validators = [DataRequired(), Length(min=8, max=25),
               ],
                           render_kw = {"placeholder": "Enter a password..."})
    
    confirm_password = PasswordField("confirm_password", validators = [DataRequired(), 
                                      EqualTo("password", message="Password must match")],
                       render_kw = {"placeholder": "Enter a confirm password..."})
    
    
    submit = SubmitField("Sign up")
    
    
    
    
    
    
class SubscribeForm(FlaskForm):

    email = StringField("email", validators = [DataRequired(), Email(), Length(min=8, max=32)],
                           render_kw = {"placeholder": "Enter a valid email..."})
    

    submit = SubmitField("Subscribe Today")
    
    
class EmailListForm(FlaskForm):

    email = StringField("email", validators = [DataRequired(), Email(), Length(min=8, max=32)],
                           render_kw = {"placeholder": "Enter a valid email..."})
    

    submit = SubmitField("Sign up Today")
    
    
    
class CommentForm(FlaskForm):
    
    
    comment = TextAreaField("comment", validators = [DataRequired(),
                                               Length(min=4, max=400)],
                    
                         render_kw = {"placeholder": "Add a comment..."})
    
    submit = SubmitField("Comment")
    
    
    
    
    
    
    