from flask import Flask, request, session, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from app.forms import CustomerRegForm, LoginForm
from app.models import Users, Items, Records, Reservation
import config
import random
import datetime
from datetime import date

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)


# 註冊
@app.route('/reg', methods=['GET', 'POST'])
def register():
    form = CustomerRegForm()
    if request.method == 'POST':
        if form.validate():
            new_customer = Users()
            new_customer.user_id = form.userid.data
            new_customer.name = form.name.data
            new_customer.password = form.password.data
            new_customer.address = form.address.data
            new_customer.birthday = form.birthday.data
            new_customer.phone = form.phone.data

            db.session.add(new_customer)
            db.session.commit()

            print('註冊成功')
            return render_template('customer_reg_success.html', form=form)

    return render_template('customer_reg.html', form=form)


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate():
            c = db.session.query(Users).filter_by(user_id=form.userid.data).first()
            if c is not None and c.password == form.password.data:
                print('登入成功')
                customer = {}
                customer['id'] = c.user_id
                customer['name'] = c.name
                customer['password'] = c.password
                customer['address'] = c.address
                customer['phone'] = c.phone
                customer['birthday'] = c.birthday
                # customer保持到HTTP Session
                session['customer'] = customer

                return redirect(url_for('main'))
            else:
                flash('您輸入的帳號密碼有錯！')
                return render_template('login.html', form=form)
    return render_template('login.html', form=form)


@app.route('/main')
def main():
    if 'customer' not in session.keys():
        flash('您還沒有登入哦！')
        return redirect(url_for('login'))
    return render_template('main.html')

#歸還頁
@app.route('/returns', methods=['GET', 'POST'])
def returns():
    if 'customer' not in session.keys():
        flash('您還沒有登入哦！')
        return redirect(url_for('login'))
    else:
#        c_all = db.session.query(Records).filter_by(user_id=session['customer']['id'],return_date='').all()
        c_all = db.session.query(Records).filter_by(user_id=session['customer']['id']).all()
        return render_template('returns.html',c_all=c_all)
    return render_template('login.html', form=form)

@app.route('/return_ok/<record>', methods=['GET', 'POST'])
def return_ok(record):
    c = db.session.query(Records).filter_by(records_id=record).first()
    c.return_date=date.today()
    db.session.commit()
    return render_template('return_ok.html')

# 顯示借用物品列表
@app.route('/list')
def show_items_list():
    if 'customer' not in session.keys():
        flash('您還沒有登入哦！')
        return redirect(url_for('login'))

    items_list = db.session.query(Items).all()
    return render_template('items_list.html', list=items_list)


# 顯示借用物品詳細資訊
@app.route('/detail')
def show_goods_detail():
    if 'customer' not in session.keys():
        flash('您還沒有登入哦！')
        return redirect(url_for('login'))

    item_id = request.args['id']
    item = db.session.query(Items).filter_by(item_id=item_id).first()

    return render_template('goods_detail.html', goods=goods)

# 添加購物車
@app.route('/add')
def add_cart():
    if 'customer' not in session.keys():
        flash('您還沒有登入哦！')
        return redirect(url_for('login'))

    goodsid = int(request.args['id'])
    goodsname = request.args['name']
    goodsprice = float(request.args['price'])

    # 判斷Session中是否有購物車數據
    if 'cart' not in session.keys():
        session['cart'] = []  

    cart = session['cart']
    # flag 如果0表示購物車中没有當前商品,1表示購物車代表有當前商品
    flag = 0
    for item in cart:
        if item[0] == goodsid:  # item[0]保存在購物車的商品id
            item[3] += 1  # item[3]保存在購物車的商品數量,對當前數量+1
            flag = 1
            break

    if flag == 0:
        # 第一次添加商品到購物車數量是1
        cart.append([goodsid, goodsname, goodsprice, 1])

    session['cart'] = cart

    print(cart)

    flash('已經添加商品【' + goodsname + '】到購物車')
    return redirect(url_for('show_goods_list'))


# 查看购物车
@app.route('/cart')
def show_cart():
    if 'customer' not in session.keys():
        flash('您還沒有登入哦！')
        return redirect(url_for('login'))

    if 'cart' not in session.keys():
        return render_template('cart.html', list=[], total=0.0)

    cart = session['cart']
    list = []
    total = 0.0
    for item in cart:
        # 購物車每一个元素[商品id, 商品名稱, 商品價格, 商品數量]
        # 添加一个小計
        subtotal = item[2] * item[3]
        total += subtotal
        new_item = (item[0], item[1], item[2], item[3], subtotal)
        list.append(new_item)

    return render_template('cart.html', list=list, total=total)


# 提交訂單
@app.route('/submit_order', methods=['POST'])
def submit_order():
    # 從表單中取出數據添加到Orders模式對象中
    orders = Orders()
    # 生成訂單id，規則為當前時間戳記+一位隨機數
    n = random.randint(0, 9)
    d = datetime.datetime.today()
    orderid = str(int(d.timestamp() * 1e6)) + str(n)
    orders.id = orderid
    orders.orderdate = d.strftime('%Y-%m-%d %H:%M:%S')
    orders.status = 1  # 1 待付款 0 已付款

    db.session.add(orders)
    # 購物車每一個元素[商品id, 商品名稱, 商品價格, 商品数量]
    cart = session['cart']
    total = 0.0
    for item in cart:
        quantity = request.form['quantity_' + str(item[0])]
        try:
            quantity = int(quantity)
        except:
            quantity = 0

        # 小計
        subtotal = item[2] * quantity
        total += subtotal

        order_line_item = OrderLineItem()
        order_line_item.quantity = quantity
        order_line_item.goodsid = item[0]
        order_line_item.orderid = orderid
        order_line_item.subtotal = subtotal

        db.session.add(order_line_item)

    orders.total = total
    # 提交事務
    db.session.commit()

    # 清除購物車
    session.pop('cart', None)

    return render_template('order_finish.html', orderid=orderid)

# 註冊
@app.route('/reg', methods=['GET', 'POST'])
def register():
    form = CustomerRegForm()
    if request.method == 'POST':
        if form.validate():
            new_customer = Users()
            new_customer.user_id = form.userid.data
            new_customer.name = form.name.data
            new_customer.password = form.password.data
            new_customer.address = form.address.data
            new_customer.birthday = form.birthday.data
            new_customer.phone = form.phone.data

            db.session.add(new_customer)
            db.session.commit()

            print('註冊成功')
            return render_template('customer_reg_success.html', form=form)

    return render_template('customer_reg.html', form=form)


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate():
            c = db.session.query(Users).filter_by(user_id=form.userid.data).first()
            if c is not None and c.password == form.password.data:
                print('登入成功')
                customer = {}
                customer['id'] = c.user_id
                customer['name'] = c.name
                customer['password'] = c.password
                customer['address'] = c.address
                customer['phone'] = c.phone
                customer['birthday'] = c.birthday
                # customer保持到HTTP Session
                session['customer'] = customer

                return redirect(url_for('main'))
            else:
                flash('您輸入的帳號密碼有錯！')
                return render_template('login.html', form=form)
    return render_template('login.html', form=form)


@app.route('/main')
def main():
    if 'customer' not in session.keys():
        flash('您還沒有登入哦！')
        return redirect(url_for('login'))
    return render_template('main.html')


# 顯示借用物品列表
@app.route('/list')
def show_items_list():
    if 'customer' not in session.keys():
        flash('您還沒有登入哦！')
        return redirect(url_for('login'))

    items_list = db.session.query(Items).all()
    return render_template('items_list.html', list=items_list)


# 顯示借用物品詳細資訊
@app.route('/detail')
def show_goods_detail():
    if 'customer' not in session.keys():
        flash('您還沒有登入哦！')
        return redirect(url_for('login'))

    item_id = request.args['id']
    item = db.session.query(Items).filter_by(item_id=item_id).first()

    if item.status == '未借出':
        return render_template('items_detail.html', goods=item)
    elif item.status == '已借出':
        return render_template('items_detail_borrow.html', goods=item)

# 歸還頁
@app.route('/returns', methods=['GET', 'POST'])
def returns():
    if 'customer' not in session.keys():
        flash('您還沒有登入哦！')
        return redirect(url_for('login'))
    else:
        c_all = db.session.query(Records).filter_by(user_id=session['customer']['id'],return_date='').all()
        return render_template('returns.html',c_all=c_all)
    return render_template('login.html', form=form)

# 歸還完成頁
@app.route('/return_ok/<record>', methods=['GET', 'POST'])
def return_ok(record):
    c = db.session.query(Records).filter_by(records_id=record).first()
    c.return_date=date.today()
    db.session.commit()
    return render_template('return_ok.html')

# 添加購物車
@app.route('/add')
def add_cart():
    if 'customer' not in session.keys():
        flash('您還沒有登入哦！')
        return redirect(url_for('login'))

    goodsid = int(request.args['id'])
    goodsname = request.args['name']
    goodsprice = float(request.args['price'])

    # 判斷Session中是否有購物車數據
    if 'cart' not in session.keys():
        session['cart'] = []  

    cart = session['cart']
    # flag 如果0表示購物車中没有當前商品,1表示購物車代表有當前商品
    flag = 0
    for item in cart:
        if item[0] == goodsid:  # item[0]保存在購物車的商品id
            item[3] += 1  # item[3]保存在購物車的商品數量,對當前數量+1
            flag = 1
            break

    if flag == 0:
        # 第一次添加商品到購物車數量是1
        cart.append([goodsid, goodsname, goodsprice, 1])

    session['cart'] = cart

    print(cart)

    flash('已經添加商品【' + goodsname + '】到購物車')
    return redirect(url_for('show_goods_list'))


# 查看购物车
@app.route('/cart')
def show_cart():
    if 'customer' not in session.keys():
        flash('您還沒有登入哦！')
        return redirect(url_for('login'))

    if 'cart' not in session.keys():
        return render_template('cart.html', list=[], total=0.0)

    cart = session['cart']
    list = []
    total = 0.0
    for item in cart:
        # 購物車每一个元素[商品id, 商品名稱, 商品價格, 商品數量]
        # 添加一个小計
        subtotal = item[2] * item[3]
        total += subtotal
        new_item = (item[0], item[1], item[2], item[3], subtotal)
        list.append(new_item)

    return render_template('cart.html', list=list, total=total)


# 提交訂單
@app.route('/submit_order', methods=['POST'])
def submit_order():
    # 從表單中取出數據添加到Orders模式對象中
    orders = Orders()
    # 生成訂單id，規則為當前時間戳記+一位隨機數
    n = random.randint(0, 9)
    d = datetime.datetime.today()
    orderid = str(int(d.timestamp() * 1e6)) + str(n)
    orders.id = orderid
    orders.orderdate = d.strftime('%Y-%m-%d %H:%M:%S')
    orders.status = 1  # 1 待付款 0 已付款

    db.session.add(orders)
    # 購物車每一個元素[商品id, 商品名稱, 商品價格, 商品数量]
    cart = session['cart']
    total = 0.0
    for item in cart:
        quantity = request.form['quantity_' + str(item[0])]
        try:
            quantity = int(quantity)
        except:
            quantity = 0

        # 小計
        subtotal = item[2] * quantity
        total += subtotal

        order_line_item = OrderLineItem()
        order_line_item.quantity = quantity
        order_line_item.goodsid = item[0]
        order_line_item.orderid = orderid
        order_line_item.subtotal = subtotal

        db.session.add(order_line_item)

    orders.total = total
    # 提交事務
    db.session.commit()

    # 清除購物車
    session.pop('cart', None)

    return render_template('order_finish.html', orderid=orderid)
