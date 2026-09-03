from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField,
    DateField,
    TimeField,
    DecimalField,
    SubmitField,IntegerField,TextAreaField
)
from wtforms.validators import DataRequired, Length, Optional,Email,EqualTo
from wtforms import (Form, StringField, SelectField,
                     DecimalField, SubmitField, FieldList, FormField,PasswordField,BooleanField)
from wtforms.fields.numeric import FloatField

class PostForm(FlaskForm):
    class Meta:
        csrf = False

    name = StringField("የአስመጪው ስም", validators=[DataRequired(message="የአስመጪው ስም ያስፈልጋል።")])
    importer_id = IntegerField("Importer ID", validators=[Optional()])
    phone = StringField("ስልክ ቁጥር", validators=[DataRequired(message="የስልክ ቁጥር ያስፈልጋል።"), Length(max=20)])
    location = StringField("የአስመጪው አድራሻ", validators=[DataRequired(message="የአስመጪው አድራሻ ያስፈልጋል።"), Length(max=200)])
    img = FileField("የምርቱ ፎቶ", validators=[DataRequired(message="photo ያስፈልጋል።")])
    date = DateField("የመድረሻ ቀን", format="%Y-%m-%d", validators=[DataRequired()])
    time = TimeField("የመድረሻ ሰዓት", validators=[Optional()])
    wage = DecimalField("የማምጫ ዋጋ (ETB)", places=2, validators=[Optional()])


class PostMainForm(FlaskForm):
    posts = FieldList(FormField(PostForm), min_entries=1)
    submit = SubmitField("Post")



class ImporterEntryForm(FlaskForm):
    class Meta:
        csrf = False

    name = StringField("Importer Name", validators=[DataRequired(), Length(max=150)])
    phone = StringField("Phone Number", validators=[Optional(), Length(max=20)])
    location = StringField("Location", validators=[Optional(), Length(max=200)])


class ProductEntryForm(FlaskForm):
    class Meta:
        csrf = False

    name = StringField("Product Name", validators=[DataRequired(), Length(max=150)])
    unit = StringField("Unit", validators=[Optional(), Length(max=30)])
    price = DecimalField("Unit Price", places=2, validators=[Optional()])
    description = TextAreaField("Description", validators=[Optional(), Length(max=500)])


class RegistrationForm(FlaskForm):
    importers = FieldList(FormField(ImporterEntryForm), min_entries=1)
    products = FieldList(FormField(ProductEntryForm), min_entries=1)
    submit = SubmitField("Save All Records")



class PostEditForm(FlaskForm):
    class Meta:
        csrf = True  # top-level form now, not a sub-form — needs its own CSRF

    name = StringField("የአስመጪው ስም", validators=[DataRequired(), Length(max=200)])
    phone = StringField("ስልክ ቁጥር", validators=[DataRequired(), Length(max=20)])
    location = StringField("የአስመጪው አድራሻ", validators=[Optional(), Length(max=200)])
    img = FileField("የምርቱ ፎቶ")  # optional on edit — keep existing image if left blank
    date = DateField("የመድረሻ ቀን", format="%Y-%m-%d", validators=[DataRequired()])
    time = TimeField("የመድረሻ ሰዓት", validators=[Optional()])
    wage = DecimalField("የማምጫ ዋጋ (ETB)", places=2, validators=[DataRequired()])



class Post2Form(FlaskForm):
    """Only the wage field is a real WTForms field. Per-product received/
    taxed/tax inputs are dynamic (one PostHistoryItem set per archived post),
    so — consistent with how products were handled in /new-post and edit_post
    — they are parsed directly from request.form rather than as a FieldList."""
    actual_wage_paid = DecimalField("Actual Wage Paid", places=2, validators=[DataRequired()])




class FinalPostEditForm(FlaskForm):
    importer_name = StringField("አስመጪ", validators=[DataRequired(), Length(max=200)])
    importer_phone = StringField("ስልክ", validators=[Optional(), Length(max=20)])
    location = StringField("አድራሻ", validators=[Optional(), Length(max=200)])
    date = DateField("የመድረሻ ቀን", format="%Y-%m-%d", validators=[DataRequired()])
    time = TimeField("የመድረሻ ሰዓት", validators=[Optional()])
    actual_wage_paid = DecimalField("በኋላ የተከፈለ ደመወዝ", places=2, validators=[DataRequired()])

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('password', message='Passwords must match')]
    )
    submit = SubmitField('Create Account')

class ImporterEdit(FlaskForm):
    class Meta:
        csrf = False

    name = StringField("Importer Name", validators=[DataRequired(), Length(max=150)])
    phone = StringField("Phone Number", validators=[Optional(), Length(max=20)])
    submit = SubmitField('save change')


class ProductEdit(FlaskForm):
    name = StringField(
        "Product Name",
        validators=[DataRequired(message="Product name is required.")]
    )
    submit = SubmitField("Save Changes")