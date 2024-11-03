from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap5 import Bootstrap
from flask_wtf import FlaskForm
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean, Float
from wtforms import StringField, IntegerField, FloatField, BooleanField, SubmitField
from wtforms.validators import DataRequired, URL, NumberRange
import os

app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URI", "sqlite:///cafes.db")
db = SQLAlchemy(app)


class CafeForm(FlaskForm):
    name = StringField("Cafe Name", validators=[DataRequired()])
    map_url = StringField("Map URL", validators=[DataRequired(), URL()])
    img_url = StringField("Image URL", validators=[DataRequired(), URL()])
    location = StringField("Location", validators=[DataRequired()])
    has_sockets = BooleanField("Has Sockets")
    has_toilet = BooleanField("Has Toilet")
    has_wifi = BooleanField("Has WiFi")
    can_take_calls = BooleanField("Can Take Calls")
    seats = IntegerField("Number of Seats", validators=[DataRequired(), NumberRange(min=1)])
    coffee_price = FloatField("Coffee Price", validators=[DataRequired()])
    submit = SubmitField("Save Cafe")


class Cafe(db.Model):
    __tablename__ = "cafe"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    img_url: Mapped[str] = mapped_column(String, nullable=False)
    location: Mapped[str] = mapped_column(String, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    seats: Mapped[int] = mapped_column(Integer, nullable=False)
    coffee_price: Mapped[float] = mapped_column(Float, nullable=False)


@app.route('/')
def index():
    cafes = Cafe.query.all()
    return render_template('index.html', cafes=cafes)


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_cafe = Cafe(
            name=form.name.data,
            map_url=form.map_url.data,
            img_url=form.img_url.data,
            location=form.location.data,
            has_sockets=form.has_sockets.data,
            has_toilet=form.has_toilet.data,
            has_wifi=form.has_wifi.data,
            can_take_calls=form.can_take_calls.data,
            seats=form.seats.data,
            coffee_price=form.coffee_price.data
        )
        db.session.add(new_cafe)
        db.session.commit()
        flash("Cafe added successfully!", "success")
        return redirect(url_for('index'))
    return render_template('add_cafe.html', form=form)


@app.route('/delete/<int:cafe_id>', methods=['GET', 'POST'])
def delete_cafe(cafe_id):
    cafe = Cafe.query.get_or_404(cafe_id)
    db.session.delete(cafe)
    db.session.commit()
    flash("Cafe deleted successfully.", "success")
    return redirect(url_for('index'))


@app.route('/edit/<int:cafe_id>', methods=['GET', 'POST'])
def edit_cafe(cafe_id):
    cafe = Cafe.query.get(cafe_id)
    form = CafeForm(obj=cafe)
    if form.validate_on_submit():
        cafe.name = form.name.data
        cafe.map_url = form.map_url.data
        cafe.img_url = form.img_url.data
        cafe.location = form.location.data
        cafe.has_sockets = form.has_sockets.data
        cafe.has_toilet = form.has_toilet.data
        cafe.has_wifi = form.has_wifi.data
        cafe.can_take_calls = form.can_take_calls.data
        cafe.seats = form.seats.data
        cafe.coffee_price = form.coffee_price.data
        db.session.commit()
        flash("Cafe updated successfully!", "success")
        return redirect(url_for('index'))
    return render_template('edit_cafe.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)

