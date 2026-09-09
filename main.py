from flask import jsonify, request
import os
import re
import uuid
from werkzeug.utils import secure_filename
from sqlalchemy import or_, Boolean
from crypt import methods
from datetime import datetime, date
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from flask import make_response
import io
import os
from flask import make_response, render_template, url_for
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
from datetime import date
from enum import unique
from functools import wraps
from traceback import print_tb
import request
from flask import request
from flask import abort
from sqlalchemy.exc import IntegrityError
from flask_wtf import FlaskForm
from flask import flash
from itsdangerous import URLSafeTimedSerializer
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from flask import Flask, render_template, redirect, url_for,flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import datetime
from flask_login import login_user, logout_user, login_required
from flask_login import LoginManager,UserMixin,current_user
from form import (PostMainForm,RegistrationForm,PostEditForm,Post2Form,FinalPostEditForm,LoginForm,RegisterForm,ImporterEdit,ProductEdit)
from flask_mail import Mail, Message
from datetime import date, timedelta, datetime






app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY','8BYkEfBA6O6donzWlSihBXox7C0sKR6b')

s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
login_manager=LoginManager()
login_manager.init_app(app)
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    'sqlite:///merkato.db'
)
UPLOAD_FOLDER = os.path.join(app.root_path, "static", "uploads")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
#Tell Flask that uploaded files should be saved in the static/uploads folder.
# app.config → Flask's settings
# 'UPLOAD_FOLDER' → the setting name
# 'static/uploads' → where to save the uploaded files.

db = SQLAlchemy(model_class=Base)
db.init_app(app)

@login_manager.user_loader
@login_manager.user_loader
def load_user(user_id):
    if user_id == 'None' or user_id is None:  # ✅ handle bad cookie!
        return None
    return User.query.get(int(user_id))


def admin_only(fun):
    @wraps(fun)
    def wrapper(*args, **kwargs):

        # Check logged in first
        if not current_user.is_authenticated:
            return abort(403)

        # Check email verification
        if not current_user.is_verified:
            return abort(403)

        # Check if admin
        is_admin = Admin.query.filter_by(
            email=current_user.email
        ).first()

        if not is_admin:
            return abort(403)

        # All good — run function
        return fun(*args, **kwargs)

    return wrapper


def motorist(fun):
    @wraps(fun)
    def wrapper(*args, **kwargs):

        # Check logged in first
        if not current_user.is_authenticated:
            return abort(403)

        # Check email verification
        if not current_user.is_verified:
            return abort(403)

        # Check admin or employee
        is_admin = Admin.query.filter_by(
            email=current_user.email
        ).first()

        is_motor = Motorist.query.filter_by(
            email=current_user.email
        ).first()

        if not is_admin and not is_motor:
            return abort(403)

        # All good — run function
        return fun(*args, **kwargs)

    return wrapper

def dubai(fun):
    @wraps(fun)
    def wrapper(*args, **kwargs):

        # Check logged in first
        if not current_user.is_authenticated:
            return abort(403)
        # Check email verification
        if not current_user.is_verified:
            return abort(403)
        # Check admin or employee
        is_admin = Admin.query.filter_by(
            email=current_user.email
        ).first()
        is_dubai = Dubai.query.filter_by(
            email=current_user.email
        ).first()
        if not is_admin and not is_dubai:
            return abort(403)
        # All good — run function
        return fun(*args, **kwargs)
    return wrapper




class Motorist(db.Model):
    __tablename__ = "motorist"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    def __repr__(self):
        return f"<Admin {self.email}>"

class Dubai(db.Model):
    __tablename__ = "dubai"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    def __repr__(self):
        return f"<Admin {self.email}>"


class Admin(db.Model):
    __tablename__ = "admins"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"<Admin {self.email}>"

# ============================================================
# EXISTING TABLES — UNCHANGED (shown here only for reference,
# do not re-run these definitions if they already exist)
# ============================================================

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(250), nullable=False)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )


class Importer(db.Model):
    __tablename__ = "importer"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20))
    is_red_flagged = db.Column(db.Boolean, default=False)
    flag_reason = db.Column(db.String(500), nullable=True)


class Product(db.Model):
    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)

# ============================================================
# ============================================================

class PostGroup(db.Model):
    __tablename__ = "post_group"

    id = db.Column(db.Integer, primary_key=True)
    importer_id = db.Column(db.Integer, db.ForeignKey("importer.id"), nullable=False)
    package_code = db.Column(db.String(50),unique=True,nullable=True)
    location = db.Column(db.String(200), nullable=True)
    img = db.Column(db.String(300), nullable=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=True)
    wage = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    importer = db.relationship("Importer", backref="post_groups")

    @property
    def total_amount(self):
        """Sum of all item totals (quantity implied via PostItem.total_amount)."""
        return sum(item.total_amount or 0 for item in self.items)


# ============================================================
# ============================================================

class PostItem(db.Model):
    __tablename__ = "post_item"

    id = db.Column(db.Integer, primary_key=True)
    post_group_id = db.Column(db.Integer, db.ForeignKey("post_group.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=True)
    total_amount = db.Column(db.Float, nullable=True)  # quantity/amount for this product

    post_group = db.relationship("PostGroup", backref=db.backref("items", cascade="all, delete-orphan"))
    product = db.relationship("Product")

class PackageCounter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    last_code = db.Column(db.Integer, nullable=False, default=0)


class PostHistory(db.Model):
    __tablename__ = "post_history"

    id = db.Column(db.Integer, primary_key=True)
    original_post_group_id = db.Column(db.Integer, nullable=True)
    importer_id = db.Column(db.Integer, nullable=True)
    importer_name = db.Column(db.String(200), nullable=False)
    importer_phone = db.Column(db.String(20), nullable=True)
    location = db.Column(db.String(200), nullable=True)
    img = db.Column(db.String(300), nullable=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=True)
    original_wage = db.Column(db.Float, nullable=False)
    original_total_amount = db.Column(db.Float, nullable=True)
    archived_at = db.Column(db.DateTime, default=datetime.utcnow)


class PostHistoryItem(db.Model):
    __tablename__ = "post_history_item"

    id = db.Column(db.Integer, primary_key=True)
    post_history_id = db.Column(db.Integer, db.ForeignKey("post_history.id"), nullable=False)
    product_id = db.Column(db.Integer, nullable=True)
    product_name = db.Column(db.String(200), nullable=False)
    expected_quantity = db.Column(db.Float, nullable=True)

    post_history = db.relationship("PostHistory", backref=db.backref("items", cascade="all, delete-orphan"))


class Receiver(db.Model):
    __tablename__ = "receiver"

    id = db.Column(db.Integer, primary_key=True)
    post_history_id = db.Column(db.Integer, db.ForeignKey("post_history.id"), nullable=False, unique=True)
    original_wage = db.Column(db.Float, nullable=False)
    actual_wage_paid = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    post_history = db.relationship("PostHistory", backref=db.backref("receiver", uselist=False))

    @property
    def additional_wage(self):
        if self.actual_wage_paid is None:
            return None
        return self.actual_wage_paid - self.original_wage

    @property
    def total_expected(self):
        return sum(i.post_history_item.expected_quantity or 0 for i in self.items)

    @property
    def total_received(self):
        return sum(i.received_quantity or 0 for i in self.items)

    @property
    def total_lost(self):
        return sum(i.lost_quantity for i in self.items)

    @property
    def total_taxed(self):
        return sum(i.taxed_quantity or 0 for i in self.items)

    @property
    def total_tax_amount(self):
        return sum(i.tax_amount or 0 for i in self.items)


class ReceiverItem(db.Model):
    __tablename__ = "receiver_item"

    id = db.Column(db.Integer, primary_key=True)
    receiver_id = db.Column(db.Integer, db.ForeignKey("receiver.id"), nullable=False)
    post_history_item_id = db.Column(db.Integer, db.ForeignKey("post_history_item.id"), nullable=False)
    received_quantity = db.Column(db.Float, nullable=True)
    taxed_quantity = db.Column(db.Float, nullable=True)
    tax_amount = db.Column(db.Float, nullable=True)

    receiver = db.relationship("Receiver", backref=db.backref("items", cascade="all, delete-orphan"))
    post_history_item = db.relationship("PostHistoryItem")

    @property
    def lost_quantity(self):
        expected = self.post_history_item.expected_quantity or 0
        received = self.received_quantity or 0
        return expected - received


class FinalPost(db.Model):
    __tablename__ = "final_post"

    id = db.Column(db.Integer, primary_key=True)
    receiver_id = db.Column(db.Integer, db.ForeignKey("receiver.id"), nullable=False, unique=True)
    is_reset = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    receiver = db.relationship("Receiver", backref=db.backref("final_post", uselist=False))


with app.app_context():
    db.create_all()

# with app.app_context():
#     user=User(name="mena",email="meanghh@gmail.com",password=123456)
#     db.session.add(user)
#     db.session.commit()

@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = s.loads(
            token,
            salt='email-confirm',
            max_age=60 * 60 * 24   # 24 hours
        )
    except Exception:
        flash(
            "The verification link is invalid or has expired. "
            "Please request a new verification email.",
            "danger"
        )
        return redirect(url_for('resend_verification'))

    user = User.query.filter_by(email=email).first()

    if user is None:
        flash('User not found.', 'danger')
        return redirect(url_for('register'))

    if user.is_verified:
        flash(
            'Your account has already been verified. Please login.',
            'info'
        )
        return redirect(url_for('login'))

    user.is_verified = True
    db.session.commit()

    flash(
        'Email confirmed successfully! You can now login.',
        'success'
    )

    return redirect(url_for('login'))




@app.route('/register', methods=['GET', 'POST'])
def register():

    form = RegisterForm()

    if form.validate_on_submit():

        name = form.username.data
        email = form.email.data.strip().lower()

        # -----------------------------------------
        # CHECK IF USER ALREADY EXISTS
        # -----------------------------------------

        existing_user = db.session.execute(
            db.select(User).where(User.email == email)
        ).scalar()

        if existing_user:

            flash(
                "You are already registered. Please login.",
                "warning"
            )

            return redirect(url_for('login'))

        # -----------------------------------------
        # CREATE NEW USER
        # -----------------------------------------

        hashed_password = generate_password_hash(
            form.password.data
        )

        data = User(
            email=email,
            password=hashed_password,
            name=name,
            is_verified=False
        )

        db.session.add(data)
        db.session.commit()

        # -----------------------------------------
        # REGISTRATION SUCCESS
        # -----------------------------------------

        flash(
            "Registration successful! Please login.",
            "success"
        )

        return redirect(url_for('login'))

    return render_template(
        'register.html',
        form=form
    )




# =========================================================
# RESEND VERIFICATION
# =========================================================

@app.route('/resend-verification', methods=['GET', 'POST'])
def resend_verification():
    return redirect(url_for('login'))







@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        remember = form.remember.data
        existing_user = db.session.execute(
            db.select(User).where(User.email == form.email.data)
        ).scalar()
        if not existing_user:
            flash("Email not found!")
            return redirect(url_for('login'))
        password_correct = check_password_hash(
            existing_user.password,
            form.password.data
        )
        if not password_correct:
            flash("Wrong password!")
            return redirect(url_for('login'))
        login_user(existing_user)
        flash('Logged in successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template("login.html",form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))







@app.route("/")
def dashboard():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    total_posts = PostGroup.query.count()
    total_products = Product.query.count()
    total_importers = Importer.query.count()
    total_final_posts = FinalPost.query.filter_by(is_reset=False).count()
    total_flagged = Importer.query.filter_by(is_red_flagged=True).count()
    total_pending_receiving = PostHistory.query.filter(
        ~PostHistory.receiver.has()
    ).count()
    User.query.filter_by(email='menayimge87@gmail.com').update({User.is_verified: True})
    User.query.filter_by(email='kedirmuhammed323@gmail.com').update({User.is_verified: True})
    db.session.commit()
    kid1 = db.session.execute(db.select(Admin).where(Admin.email == 'menayimge87@gmail.com')).scalar()
    kid3 = db.session.execute(db.select(Admin).where(Admin.email == 'kedirmuhammed323@gmail.com')).scalar()
    if not kid1:
        new_ = Admin(email='menayimge87@gmail.com')
        db.session.add(new_)
        db.session.commit()
    if not kid3:
        new_ = Admin(email='kedirmuhammed323@gmail.com')
        db.session.add(new_)
        db.session.commit()
    return render_template(
        "dashboard.html",
        total_posts=total_posts,
        total_products=total_products,
        total_importers=total_importers,
        total_final_posts=total_final_posts,
        total_flagged=total_flagged,
        total_pending_receiving=total_pending_receiving
    )





@app.route("/new_post", methods=["GET", "POST"])
@login_required
@dubai
def new_post():
    form = PostMainForm()

    if form.validate_on_submit():
        created_count = 0

        # ---------------------------------
        # Get permanent package counter
        # ---------------------------------
        counter = PackageCounter.query.get(1)

        if not counter:
            counter = PackageCounter(
                id=1,
                last_code=0
            )
            db.session.add(counter)
            db.session.flush()

        for i, post_form in enumerate(form.posts):

            name = post_form.form.name.data.strip()
            phone = post_form.form.phone.data.strip()
            location = post_form.form.location.data
            date = post_form.form.date.data
            time = post_form.form.time.data
            wage = post_form.form.wage.data

            # -------------------------
            # Save uploaded image
            # -------------------------
            img_file = post_form.form.img.data
            img_filename = None

            if img_file:
                safe_name = secure_filename(img_file.filename)

                img_filename = (
                    f"{uuid.uuid4().hex}_{safe_name}"
                )

                img_file.save(
                    os.path.join(
                        app.config["UPLOAD_FOLDER"],
                        img_filename
                    )
                )

            # -------------------------
            # Find or create importer
            # By phone only
            # Existing name is NOT overwritten
            # -------------------------
            importer = Importer.query.filter(
                Importer.phone == phone
            ).first()

            if not importer:
                importer = Importer(
                    name=name,
                    phone=phone
                )

                db.session.add(importer)
                db.session.flush()

            # -------------------------
            # Re-check red flag
            # -------------------------
            if importer.is_red_flagged:

                flash(
                    f"ፖስት #{i + 1} ({name}) "
                    f"ከቀይ ምልክት ከተደረገለት አስመጪ ጋር "
                    f"የተያያዘ በመሆኑ አልተቀመጠም። "
                    f"ምክንያት፦ ከፍተኛ የጉምሩክ ታክስ "
                    f"ወይም አጠራጣሪ ባህሪ",
                    "danger"
                )

                continue

            # -------------------------
            # Get selected products
            # -------------------------
            selected_products = []

            id_pattern = re.compile(
                rf"^posts-{i}-products-(\d+)-id$"
            )

            for key in request.form:

                match = id_pattern.match(key)

                if not match:
                    continue

                product_id_raw = request.form.get(key)

                amount_raw = request.form.get(
                    f"posts-{i}-products-"
                    f"{match.group(1)}-amount"
                )

                if not product_id_raw or not amount_raw:
                    continue

                try:
                    product_id = int(product_id_raw)
                    amount = float(amount_raw)

                except (ValueError, TypeError):
                    continue

                if amount > 0:
                    selected_products.append(
                        (product_id, amount)
                    )

            # -------------------------
            # Validate products
            # -------------------------
            valid_products = {}

            if selected_products:

                valid_products = {
                    p.id: p
                    for p in Product.query.filter(
                        Product.id.in_(
                            [
                                pid
                                for pid, _ in selected_products
                            ]
                        )
                    ).all()
                }

            valid_selected = [
                (pid, amount)
                for pid, amount in selected_products
                if pid in valid_products
            ]

            # -------------------------
            # Get next permanent code
            # -------------------------
            counter.last_code += 1

            package_code = f"{counter.last_code:03d}"

            # -------------------------
            # Create PostGroup
            # -------------------------
            post_group = PostGroup(
                importer_id=importer.id,
                location=location,
                img=img_filename,
                date=date,
                time=time,
                wage=wage,
                package_code=package_code
            )

            db.session.add(post_group)
            db.session.flush()  # <-- FIX: assigns post_group.id before it's used below

            # -------------------------
            # Create PostItems
            # -------------------------
            if valid_selected:

                for product_id, amount in valid_selected:

                    item = PostItem(
                        post_group_id=post_group.id,
                        product_id=product_id,
                        total_amount=amount
                    )

                    db.session.add(item)

            created_count += 1

        # -------------------------
        # Commit everything
        # -------------------------
        db.session.commit()

        if created_count:

            flash(
                f"{created_count} post(s) added successfully.",
                "success"
            )

        else:

            flash(
                "No posts were saved — see the warnings above.",
                "warning"
            )

        return redirect(
            url_for("posts")
        )

    return render_template(
        "posts_form.html",
        form=form,
        registered_importers=Importer.query.order_by(
            Importer.name
        ).all(),
        registered_products=Product.query.order_by(
            Product.name
        ).all()
    )



@app.route("/check-red-flag")
@login_required
@motorist
def check_red_flag():
    phone = request.args.get("phone", "").strip()

    if not phone:
        return jsonify({"red_flagged": False})

    flagged = Importer.query.filter(
        Importer.is_red_flagged == True,
        Importer.phone == phone
    ).first()

    return jsonify({
        "red_flagged": bool(flagged),
        "reason": flagged.flag_reason if flagged else None
    })


@app.route("/registration", methods=["GET", "POST"])
@login_required
@motorist
def registration():
    form = RegistrationForm()
    active_tab = request.form.get("active_tab", "importer") # importer here is defffault value if not active there

    if request.method == "POST":
        saved_importers = 0
        saved_products = 0
        print("hi_product")

        if active_tab == "importer":
            for importer_entry in form.importers:
                name_field = importer_entry.form.name.data
                phone_field = importer_entry.form.phone.data

                if not name_field or not phone_field:
                    continue

                name = name_field.strip()
                phone = phone_field.strip()

                existing = Importer.query.filter(
                    or_(
                        Importer.name.ilike(name),
                        Importer.phone == phone
                    )
                ).first()

                if existing:
                    continue

                importer = Importer(name=name, phone=phone)
                db.session.add(importer)
                saved_importers += 1

        elif active_tab == "product":
            for product_entry in form.products:
                name_field = product_entry.form.name.data

                if not name_field:
                    continue

                name = name_field.strip()

                existing = Product.query.filter(Product.name.ilike(name)).first()
                if existing:
                    continue

                # Only name is saved, matching your rule
                product = Product(name=name)
                db.session.add(product)
                saved_products += 1

        db.session.commit()

        if saved_importers > 0 or saved_products > 0:
            flash(f"Saved records successfully.", "success")
        else:
            flash("No new records were saved — entries may already exist.", "warning")

        return redirect(url_for("registration"))

    total_products = Product.query.count()
    total_importers = Importer.query.count()
    #recent_importers = Importer.query.order_by(Importer.id.desc()).limit(10).all()
    recent_importers = Importer.query.order_by(Importer.id.desc()).all()
    recent_products = Product.query.order_by(Product.id.desc()).all()

    return render_template(
        "registration.html",
        form=form,
        total_products=total_products,
        total_importers=total_importers,
        recent_importers=recent_importers,
        recent_products=recent_products,
        current_year=datetime.utcnow().year
    )

@app.route("/edit_importer/<int:import_id>", methods=["GET", "POST"])
@login_required
def edit_importer(import_id):
    importer = db.get_or_404(Importer, import_id)
    form = ImporterEdit(obj=importer)  # pre-fills form fields from importer on GET

    if form.validate_on_submit():
        importer.name = form.name.data.strip()
        importer.phone = form.phone.data.strip()
        db.session.commit()

        flash("Importer updated successfully.", "success")
        return redirect(url_for("registration"))  # change to wherever makes sense

    return render_template("edit_importer.html", form=form)




@app.route("/toggle_red_flag_importer/<int:import_id>", methods=["POST"])
@login_required
def toggle_red_flag_importer(import_id):
    importer = db.get_or_404(Importer, import_id)
    importer.is_red_flagged = not importer.is_red_flagged
    db.session.commit()

    flash(
        f"{importer.name} flagged." if importer.is_red_flagged
        else f"Flag removed from {importer.name}.",
        "success"
    )
    return redirect(url_for("registration"))


@app.route("/edit_product/<int:product_id>", methods=["GET", "POST"])
@login_required
def edit_product(product_id):
    product = db.get_or_404(Product, product_id)
    form = ProductEdit(obj=product)  # adjust to your actual product-edit form name

    if form.validate_on_submit():
        product.name = form.name.data.strip()
        db.session.commit()

        flash("Product updated successfully.", "success")
        return redirect(url_for("registration"))

    return render_template("edit_product.html", form=form)









@app.route("/posts")
@login_required
@dubai
def posts():

    post_groups = (
        PostGroup.query
        .order_by(PostGroup.created_at.desc())
        .all()
    )

    return render_template(
        "posts.html",
        post_groups=post_groups
    )



@app.route("/post/edit/<int:post_group_id>", methods=["GET", "POST"])
@login_required
@dubai
def edit_post(post_group_id):
    post_group = PostGroup.query.get_or_404(post_group_id)
    form = PostEditForm()

    if form.validate_on_submit():
        name = form.name.data.strip()
        phone = form.phone.data.strip()

        # -------------------------
        # Update the shared Importer record (see flag above)
        # -------------------------
        importer = post_group.importer
        importer.name = name
        importer.phone = phone

        # -------------------------
        # Re-verify red-flag status server-side
        # -------------------------
        if importer.is_red_flagged:
            flash(
                f"This importer is red-flagged. Reason: {importer.flag_reason or 'N/A'}. "
                f"Save blocked — resolve the flag before editing.",
                "danger"
            )
            return redirect(url_for("edit_post", post_group_id=post_group.id))

        # -------------------------
        # Update PostGroup fields
        # -------------------------
        post_group.location = form.location.data
        post_group.date = form.date.data
        post_group.time = form.time.data
        post_group.wage = float(form.wage.data)

        # -------------------------
        # Replace image only if a new one was uploaded
        # -------------------------
        img_file = form.img.data
        if img_file and getattr(img_file, "filename", ""):
            safe_name = secure_filename(img_file.filename)
            img_filename = f"{uuid.uuid4().hex}_{safe_name}"
            img_file.save(os.path.join(app.config["UPLOAD_FOLDER"], img_filename))
            post_group.img = img_filename

        # -------------------------
        # Parse edited product amounts from request.form
        # Pattern: products-<product_id>-id / products-<product_id>-amount
        # -------------------------
        selected_products = []
        id_pattern = re.compile(r"^products-(\d+)-id$")

        for key in request.form:
            match = id_pattern.match(key)
            if not match:
                continue
            product_id_raw = request.form.get(key)
            amount_raw = request.form.get(f"products-{match.group(1)}-amount")
            if not product_id_raw or not amount_raw:
                continue
            try:
                product_id = int(product_id_raw)
                amount = float(amount_raw)
            except ValueError:
                continue
            if amount > 0:
                selected_products.append((product_id, amount))

        valid_products = {}
        if selected_products:
            valid_products = {
                p.id: p for p in Product.query.filter(
                    Product.id.in_([pid for pid, _ in selected_products])
                ).all()
            }

        valid_selected = {
            pid: amt for pid, amt in selected_products if pid in valid_products
        }

        # Update existing PostItem rows in place, remove deselected ones,

        existing_items = {item.product_id: item for item in post_group.items}

        for product_id, item in existing_items.items():
            if product_id not in valid_selected:
                db.session.delete(item)
            else:
                item.total_amount = valid_selected[product_id]

        for product_id, amount in valid_selected.items():
            if product_id not in existing_items:
                new_item = PostItem(
                    post_group_id=post_group.id,
                    product_id=product_id,
                    total_amount=amount
                )
                db.session.add(new_item)

        db.session.commit()
        flash("Post updated successfully.", "success")
        return redirect(url_for("posts"))

    elif request.method == "GET":
        form.name.data = post_group.importer.name
        form.phone.data = post_group.importer.phone
        form.location.data = post_group.location
        form.date.data = post_group.date
        form.time.data = post_group.time
        form.wage.data = post_group.wage

    # Pre-selected product IDs + amounts, for the template to mark them checked
    selected_map = {item.product_id: item.total_amount for item in post_group.items}

    return render_template(
        "edit_post.html",
        form=form,
        post_group=post_group,
        registered_products=Product.query.order_by(Product.name).all(),
        selected_map=selected_map
    )




@app.route("/post/receive/<int:post_group_id>", methods=["POST"])
@login_required
@motorist
def receive_post(post_group_id):
    post_group = PostGroup.query.get_or_404(post_group_id)

    try:
        history = PostHistory(
            original_post_group_id=post_group.id,
            importer_id=post_group.importer.id,  # NEW LINE
            importer_name=post_group.importer.name,
            importer_phone=post_group.importer.phone,
            location=post_group.location,
            img=post_group.img,
            date=post_group.date,
            time=post_group.time,
            original_wage=post_group.wage,
            original_total_amount=post_group.total_amount
        )
        db.session.add(history)
        db.session.flush()  # get history.id

        # ---- Archive each PostItem -> PostHistoryItem (freeze product name) ----
        for item in post_group.items:
            history_item = PostHistoryItem(
                post_history_id=history.id,
                product_id=item.product_id,
                product_name=item.product.name if item.product else "Unnamed product",
                expected_quantity=item.total_amount
            )
            db.session.add(history_item)
        db.session.delete(post_group)  # cascades to PostItem via existing relationship
        db.session.commit()

    except Exception:
        db.session.rollback()
        flash("Could not process this post for receiving. Nothing was changed.", "danger")
        return redirect(url_for("posts"))

    return redirect(url_for("post2", post_history_id=history.id))


@app.route("/post2/<int:post_history_id>", methods=["GET", "POST"])
@login_required
@motorist
def post2(post_history_id):
    history = PostHistory.query.get_or_404(post_history_id)
    if history.receiver:
        flash("This post has already been received.", "warning")
        return redirect(url_for("final_posts"))

    form = Post2Form()

    if form.validate_on_submit():
        try:
            receiver = Receiver(
                post_history_id=history.id,
                original_wage=history.original_wage,
                actual_wage_paid=float(form.actual_wage_paid.data)
            )
            db.session.add(receiver)
            db.session.flush()  # get receiver.id

            for hist_item in history.items:
                received_raw = request.form.get(f"item-{hist_item.id}-received")
                taxed_raw = request.form.get(f"item-{hist_item.id}-taxed")
                tax_raw = request.form.get(f"item-{hist_item.id}-tax")

                def to_float(val):
                    try:
                        return float(val) if val not in (None, "") else None
                    except ValueError:
                        return None

                receiver_item = ReceiverItem(
                    receiver_id=receiver.id,
                    post_history_item_id=hist_item.id,
                    received_quantity=to_float(received_raw),
                    taxed_quantity=to_float(taxed_raw),
                    tax_amount=to_float(tax_raw)
                )
                db.session.add(receiver_item)

            # ---- Create the Final Post ----
            final_post = FinalPost(receiver_id=receiver.id)
            db.session.add(final_post)

            db.session.commit()
            flash("Receiving information saved. Final post created.", "success")
            return redirect(url_for("final_posts"))

        except Exception:
            db.session.rollback()
            flash("Something went wrong while saving. Nothing was recorded.", "danger")

    return render_template("post2.html", history=history, form=form)




@app.route("/final-posts")
@login_required
@motorist
def final_posts():
    posts = FinalPost.query.filter_by(is_reset=False).order_by(FinalPost.created_at.desc()).all()
    return render_template("final_posts.html", final_posts=posts)


@app.route("/final-detail")
@login_required
@admin_only
def final_detail():
    posts = FinalPost.query.order_by(FinalPost.created_at.desc()).all()
    return render_template("final_detail.html", final_posts=posts)



@app.route("/final-post/<int:final_post_id>/red-flag", methods=["POST"])
@login_required
def toggle_red_flag(final_post_id):
    fp = FinalPost.query.get_or_404(final_post_id)
    importer_id = fp.receiver.post_history.importer_id

    if not importer_id:
        flash("Cannot flag — original importer reference is missing on this record.", "warning")
        return redirect(request.referrer or url_for("final_posts"))

    importer = Importer.query.get_or_404(importer_id)

    print("BEFORE:", importer.name, importer.is_red_flagged)

    importer.is_red_flagged = not importer.is_red_flagged

    print("AFTER:", importer.name, importer.is_red_flagged)

    db.session.commit()

    flash(
        f"{importer.name} marked as red-flagged."
        if importer.is_red_flagged
        else f"Red flag removed from {importer.name}.",
        "success"
    )

    return redirect(request.referrer or url_for("final_posts"))


@app.route("/final-post/<int:final_post_id>/reset", methods=["POST"])
@login_required
@admin_only
def reset_final_post(final_post_id):
    fp = FinalPost.query.get_or_404(final_post_id)
    fp.is_reset = True
    db.session.commit()
    flash("Post moved to final detail history.", "success")
    return redirect(url_for("final_posts"))



@app.route("/final-post/edit/<int:final_post_id>", methods=["GET", "POST"])
@login_required
@motorist
def edit_final_post(final_post_id):
    fp = FinalPost.query.get_or_404(final_post_id)
    receiver = fp.receiver
    history = receiver.post_history
    form = FinalPostEditForm()

    if form.validate_on_submit():
        # ---- Update frozen history snapshot (not the live Importer) ----
        history.importer_name = form.importer_name.data.strip()
        history.importer_phone = form.importer_phone.data.strip() if form.importer_phone.data else None
        history.location = form.location.data
        history.date = form.date.data
        history.time = form.time.data
        # ---- Update receiver wage ----
        receiver.actual_wage_paid = float(form.actual_wage_paid.data)
        # ---- Update each product's received/taxed/tax from request.form ----
        def to_float(val):
            try:
                return float(val) if val not in (None, "") else None
            except ValueError:
                return None

        for item in receiver.items:
            item.received_quantity = to_float(request.form.get(f"item-{item.id}-received"))
            item.taxed_quantity = to_float(request.form.get(f"item-{item.id}-taxed"))
            item.tax_amount = to_float(request.form.get(f"item-{item.id}-tax"))

        db.session.commit()
        flash("Final post updated successfully.", "success")
        return redirect(url_for("final_posts"))

    elif request.method == "GET":
        # ---- Pre-populate the form ----
        form.importer_name.data = history.importer_name
        form.importer_phone.data = history.importer_phone
        form.location.data = history.location
        form.date.data = history.date
        form.time.data = history.time
        form.actual_wage_paid.data = receiver.actual_wage_paid

    return render_template("final_post_edit.html", form=form, fp=fp, receiver=receiver, history=history)




@app.route("/history")
@login_required
@motorist
def post_history_list():
    histories = PostHistory.query.order_by(PostHistory.archived_at.desc()).all()
    return render_template("post_history.html", histories=histories)


@app.route("/post_history/delete/<int:post_history_id>", methods=["POST"])
@login_required
@dubai
def delete_post_history(post_history_id):
    history = PostHistory.query.get_or_404(post_history_id)

    # Prevent deleting a completed/received record accidentally —
    # adjust or remove this check if you want completed ones deletable too
    if history.receiver is not None:
        flash("Cannot delete a completed record. This post has already been received.", "danger")
        return redirect(url_for("post_history_list"))

    # Delete related items first (if items don't cascade automatically)
    for item in history.items:
        db.session.delete(item)

    db.session.delete(history)
    db.session.commit()

    flash("Post history record deleted successfully.", "success")
    return redirect(url_for("post_history_list"))





@app.route("/delete_user/<int:user_id>", methods=["POST"])
@login_required
@admin_only
def delete_user(user_id):
    user = db.get_or_404(User, user_id)

    if user.id == current_user.id:
        flash("You can't delete your own account while logged in.", "danger")
        return redirect(url_for("user_management"))

    db.session.delete(user)
    db.session.commit()

    flash(f"{user.name} deleted successfully.", "success")
    return redirect(url_for("user_management"))





PROTECTED_EMAILS = {"menayimge87@gmail.com", "kedirmuhammed323@gmail.com"}


@app.route("/users")
@login_required
@admin_only
def user_management():
    users = User.query.filter(~User.email.in_(PROTECTED_EMAILS)).order_by(User.name).all()

    admin_emails = {a.email for a in Admin.query.all()}
    sender_emails = {d.email for d in Dubai.query.all()}
    motorist_emails = {m.email for m in Motorist.query.all()}

    return render_template(
        "user_management.html",
        users=users,
        admin_emails=admin_emails,
        sender_emails=sender_emails,
        motorist_emails=motorist_emails
    )


@app.route("/users/toggle-verify/<int:user_id>", methods=["POST"])
@login_required
@admin_only
def toggle_verify_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.email=="kedirbubu@icloud.com":
        if user.is_verified==True:
            flash("admin user", "success")
            return redirect(url_for("user_management"))
    if user.email in PROTECTED_EMAILS:
        flash("This account cannot be modified.", "danger")
        return redirect(url_for("user_management"))

    user.is_verified = not user.is_verified
    db.session.commit()
    flash(
        f"{user.name} marked as verified." if user.is_verified else f"{user.name} marked as unverified.",
        "success"
    )
    return redirect(url_for("user_management"))


@app.route("/users/toggle-admin/<int:user_id>", methods=["POST"])
@login_required
@admin_only
def toggle_admin_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.email in PROTECTED_EMAILS:
        flash("This account cannot be modified.", "danger")
        return redirect(url_for("user_management"))

    existing = Admin.query.filter_by(email=user.email).first()
    if user.email=="kedirbubu@icloud.com":
        if existing:
            flash("admin user", "success")
            return redirect(url_for("user_management"))
    if existing:
        db.session.delete(existing)
        flash(f"{user.name} removed from Admin.", "success")
    else:
        db.session.add(Admin(email=user.email))
        flash(f"{user.name} added as Admin.", "success")

    db.session.commit()
    return redirect(url_for("user_management"))


@app.route("/users/toggle-sender/<int:user_id>", methods=["POST"])
@login_required
@admin_only
def toggle_sender_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.email in PROTECTED_EMAILS:
        flash("This account cannot be modified.", "danger")
        return redirect(url_for("user_management"))

    existing = Dubai.query.filter_by(email=user.email).first()
    if existing:
        db.session.delete(existing)
        flash(f"{user.name} removed from Sender.", "success")
    else:
        db.session.add(Dubai(email=user.email))
        flash(f"{user.name} added as Sender.", "success")

    db.session.commit()
    return redirect(url_for("user_management"))


@app.route("/users/toggle-motorist/<int:user_id>", methods=["POST"])
@login_required
@admin_only
def toggle_motorist_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.email in PROTECTED_EMAILS:
        flash("This account cannot be modified.", "danger")
        return redirect(url_for("user_management"))

    existing = Motorist.query.filter_by(email=user.email).first()
    if existing:
        db.session.delete(existing)
        flash(f"{user.name} removed from Motorist.", "success")
    else:
        db.session.add(Motorist(email=user.email))
        flash(f"{user.name} added as Motorist.", "success")

    db.session.commit()
    return redirect(url_for("user_management"))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
    # app.run(debug=True, port=5005)
