from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
import hashlib
import os
from flask import session

app = Flask(__name__)
login_manager = LoginManager(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mariadb+mysqlconnector://root:1q2w_1q2w@localhost:3306/catalogue'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}
app.secret_key = '111'
db = SQLAlchemy(app)


class User(UserMixin):
    def __init__(self, user_id, username):
        self.id = user_id
        self.username = username


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(64), nullable=False)
    salt = db.Column(db.String(32), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.salt = os.urandom(16).hex()
        self.password_hash = self._hash_password(password)

    def _hash_password(self, password):
        return hashlib.sha256((password + self.salt).encode('utf-8')).hexdigest()


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    image_url = db.Column(db.String(255))
    short_description = db.Column(db.Text)
    characteristics = db.Column(db.Text)
    detailed_description = db.Column(db.Text)
    category = db.Column(db.Integer)
    cost = db.Column(db.Integer)
    category_for_site = db.Column(db.String(255))

    def __repr__(self):
        return f'<Product {self.id}: {self.name}>'


class categories(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    name_for_site = db.Column(db.String(255), nullable=False)
    image_url = db.Column(db.String(255))


class Bucket(db.Model):
    pid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_user = db.Column(db.Integer)
    id_item = db.Column(db.Integer)
    quantity = db.Column(db.Integer, default=0)


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    surname = db.Column(db.String(255))
    post = db.Column(db.String(255))
    photo = db.Column(db.String(255))


class totals(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_user = db.Column(db.Integer)
    total = db.Column(db.Integer)


class contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    subject = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)


@login_manager.user_loader
def load_user(user_id):
    # Замените эту часть кода на логику загрузки пользователя из базы данных
    user = Users.query.get(user_id)
    return User(user.id, user.username) if user else None


@app.route('/')
@app.route('/index')
def hello_world():  # put application's code here
    return render_template('index.html')


@app.route('/about')
def about_company():
    return render_template('about.html')


@app.route('/promotions')
def promotions():
    return render_template('promotions.html')


@app.route('/catalogue')
def catalog():
    products = categories.query.all()
    return render_template('catalogue2.html', products=products)


@app.route('/landing')
def land():
    return render_template('landing.html')


@app.route('/catalog/', methods=['GET'])
def catalog2():
    search_query = request.args.get('search', '')

    # Поиск продуктов по параметру short_description
    products = Products.query.filter(Products.name.ilike(f'%{search_query}%')).all()
    return render_template('search_results.html', products=products, search_query=search_query)


@app.route('/catalogue/<string:name>')
def catalog_2(name):
    if name == "suspensions":
        temp = "suspensions/"
        description = 'Подвески'
        return render_template('catalogue.html', products=Products.query.filter_by(category=3).all(),
                               temp=temp, description=description)
    elif name == "rings":
        temp = "rings/"
        description = 'Кольца'
        return render_template('catalogue.html', products=Products.query.filter_by(category=1).all(),
                               temp=temp, description=description)
    elif name == "earrings":
        temp = "earrings/"
        description = 'Серьги'
        return render_template('catalogue.html', products=Products.query.filter_by(category=2).all(),
                               temp=temp, description=description)
    elif name == "necklaces":
        description = 'Колье'
        temp = "necklaces/"
        return render_template('catalogue.html', products=Products.query.filter_by(category=4).all(),
                               temp=temp, description=description)


@app.route('/catalogue/<string:name>/<int:id>')
def elem(name, id):
    elemement = Products.query.get(id)
    return render_template("element.html", elemement=elemement, name=name)


@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    try:
        product = Products.query.get(product_id)
        if not current_user.is_authenticated:
            flash('Необходимо войти в аккаунт для добавления товара в корзину', 'error')
            return redirect(url_for('elem', name=product.category_for_site, id=product.id))
        if product and current_user.is_authenticated:
            existing_item = Bucket.query.filter_by(id_user=current_user.get_id(), id_item=product.id).first()
            if existing_item:
                existing_item.quantity += 1
                flash('Количество товара в корзине увеличено', 'info')
            else:
                cart_item = Bucket(
                    id_user=current_user.id,
                    id_item=product.id,
                    quantity=1
                )
                db.session.add(cart_item)
                flash('Товар добавлен в корзину', 'success')

            db.session.commit()
        else:
            flash('Продукт не найден или пользователь не аутентифицирован', 'error')

    except Exception as e:
        print(f'Ошибка при добавлении в корзину: {e}')
        flash('Произошла ошибка. Попробуйте еще раз.', 'error')

    return redirect(url_for('elem', name=product.category_for_site, id=product.id, message='Товар добавлен в корзину'))


@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']

        new_contact = contact(name=name, email=email, subject=subject, message=message)
        db.session.add(new_contact)
        db.session.commit()
        return redirect(url_for('contacts'))
    return render_template('contacts.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        #    Проверка существования пользователя и совпадения пароля
        user = Users.query.filter_by(username=username).first()
        if user and user.password_hash == hashlib.sha256((password + user.salt).encode('utf-8')).hexdigest():
            # Успешная аутентификация
            session['current_user'] = {'username': user.username}
            login_user(User(user.id, user.username))
            return redirect(url_for('hello_world'))
        else:
            flash('Неправильный логин или пароль', 'error')
    return render_template('login.html')


@app.route('/user_profile')
def user_profile():
    # Проверка, что пользователь аутентифицирован
    if 'current_user' in session and 'username' in session['current_user']:
        user_data = Bucket.query.filter_by(id_user=current_user.get_id()).all()
        product_data = []
        for data in user_data:
            product_data.append(Products.query.filter_by(id=data.id_item).first())
        totals_data = totals.query.filter_by(id_user=current_user.get_id()).first()
        if totals_data:
            total_cost = totals_data.total
        else:
            total_cost = 0
        return render_template('user_profile2.html', username=session['current_user']['username'],
                               user_data=user_data, product_data=product_data, total_cost=total_cost)
    else:
        # Если пользователь не аутентифицирован, перенаправляем на страницу входа
        return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        existing_user = Users.query.filter_by(username=username).first()
        if existing_user:
            flash('Пользователь с таким именем уже зарегистрирован', 'error')
            return render_template('register.html')
        if password != confirm_password:
            flash("Passwords do not match", "error")
            return render_template('register.html')
        new_user = Users(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        user = Users.query.filter_by(username=username).first()
        session['current_user'] = {'username': user.username}
        login_user(User(user.id, user.username))
        return redirect(url_for('hello_world'))
    return render_template('register.html')


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('current_user', None)
    logout_user()
    return redirect(url_for('hello_world'))


@app.route('/team')
def team():
    employees = Employee.query.all()
    return render_template("team.html", employees=employees)


@app.route('/update_quantity', methods=['POST'])
def update_quantity():
    product_id = request.form.get('product_id')
    change = int(request.form.get('change'))
    cost = int(request.form.get('cost'))
    total_cost = 0
    existing_item = Bucket.query.filter_by(id_user=current_user.get_id(), id_item=product_id).first()
    if existing_item:
        if existing_item.quantity > 1:
            existing_item.quantity += change
            db.session.commit()
            total_cost = totals.query.filter_by(id_user=current_user.get_id()).first().total
            return jsonify({'new_quantity': existing_item.quantity, 'new_total': total_cost})
        elif existing_item.quantity == 1 and change == 1:
            existing_item.quantity += change
            db.session.commit()
            total_cost = totals.query.filter_by(id_user=current_user.get_id()).first().total
            return jsonify({'new_quantity': existing_item.quantity, 'new_total': total_cost})
        else:
            return jsonify({'error': 'Product not found'}), 404

    return jsonify({'error': 'Product not found'}), 404


@app.route('/delete-product/<int:pid>', methods=['DELETE'])
def delete_product(pid):
    item = Bucket.query.get_or_404(pid)
    print(item)
    db.session.delete(item)
    db.session.commit()

    # Вернуть ответ об успешном удалении
    return jsonify({'message': 'Товар успешно удален'}), 200


if __name__ == '__main__':
    app.secret_key = '111'
    app.run(host='localhost', port=5002, debug=True)
