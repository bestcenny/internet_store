from flask import Flask

from data import db_session
from data.users import User
from data.stock import Stock
from data.cart import Cart
from forms.user import RegisterForm
from flask import render_template, redirect, request
from flask_login import LoginManager, login_user, logout_user, login_required
from forms.login import LoginForm
from forms.stock import StockForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


def main():
    db_session.global_init("db/stock.db")
    app.run()


@app.route('/stock', methods=['GET', 'POST'])
@login_required
def add_product():
    form = StockForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        stock = Stock()
        stock.name = form.name.data
        stock.description = form.description.data
        stock.price = form.price.data
        stock.photo = form.photo.data
        stock.amount = form.amount.data
        db_sess.merge(stock)
        db_sess.commit()
        return redirect('/')
    return render_template('stock.html', title='Добавление товара',
                           form=form)


@app.route('/add_button', methods=['POST'])
def add_in_cart_button():
    item_id = request.form["add_button"]
    item_id = item_id.split()
    add_id = str(item_id[-1])
    len_id = len(add_id)
    add_in_cart(add_id[1:len_id - 1])
    return redirect("/")


def add_in_cart(product_id):
    db_sess = db_session.create_session()
    stock = db_sess.query(Stock).get(int(product_id))
    stock.amount = stock.amount - 1
    cart = Cart()
    cart.name = stock.name
    cart.description = stock.description
    cart.price = stock.price
    cart.photo = stock.photo
    db_sess.merge(cart)
    db_sess.commit()


@app.route('/open_cart', methods=['GET', 'POST'])
def open_cart():
    db_sess = db_session.create_session()
    cart = db_sess.query(Cart)
    return render_template("cart.html", cart=cart)


@app.route('/del_button', methods=['GET', 'POST'])
def del_button():
    product_id = request.form["del_button"]
    product_id = product_id.split()
    add_id = str(product_id[-1])
    len_id = len(add_id)
    db_sess = db_session.create_session()
    db_sess.query(Cart).filter(Cart.id == add_id[1:len_id - 1]).delete()
    db_sess.commit()
    return redirect("/")


@app.route('/add_in_stock', methods=['GET', 'POST'])
def add_in_stock():
    product_id = request.form["add_in_stock"]
    product_id = product_id.split()
    add_id = str(product_id[-1])
    len_id = len(add_id)
    db_sess = db_session.create_session()
    stock = db_sess.query(Stock).get(int(add_id[1:len_id - 1]))
    stock.amount = stock.amount + 1
    db_sess.commit()
    return redirect("/")


@app.route('/order', methods=['GET', 'POST'])
def order():
    db_sess = db_session.create_session()
    is_cart = db_sess.query(Cart).first()
    if is_cart:
        db_sess = db_session.create_session()
        db_sess.query(Cart).delete()
        db_sess.commit()
        return render_template('order.html',
                               message="Ваш заказ уже в пути!")
    else:
        return render_template('order.html',
                               message="Ваша корзина пуста.")


@app.route('/return', methods=['GET', 'POST'])
def return_button():
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    db_sess = db_session.create_session()
    db_sess.query(Cart).delete()
    db_sess.commit()
    logout_user()
    return redirect("/")


@app.route("/")
def index():
    db_sess = db_session.create_session()
    stock = db_sess.query(Stock)
    return render_template("index.html", stock=stock)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


if __name__ == '__main__':
    main()
