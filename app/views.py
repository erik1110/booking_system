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

# 歸還頁面
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

# 預約頁面
@app.route('/reservations', methods=['GET', 'POST'])
def reservations():
    if 'customer' not in session.keys():
        flash('您還沒有登入哦！')
        return redirect(url_for('login'))
  
    if 'reservations' not in session.keys():
        return render_template('reservations.html', list=[])
    
    reservations = session['reservations']
    list = []
    for item in reservations:
        # 購物車每一个元素[商品id, 商品名稱, 商品價格, 商品數量]
        new_item = (item[0], item[1])
        list.append(new_item)
    print('list:', list)
    return render_template('reservations.html', list=list)
    
@app.route('/reserve_ok/<record>', methods=['GET', 'POST'])
def reserve_ok(record):
    res_list = db.session.query(Records).filter_by(records_id=record).first()
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
def show_items_detail():
    if 'customer' not in session.keys():
        flash('您還沒有登入哦！')
        return redirect(url_for('login'))
    item_id = request.args['item_id']
    item = db.session.query(Items).filter_by(item_id=item_id).first()
    return render_template('items_detail.html', item=item)

# 添加預約頁面
@app.route('/add_reservation')
def add_reservation():
    if 'customer' not in session.keys():
        flash('您還沒有登入哦！')
        return redirect(url_for('login'))

    item_id = int(request.args['item_id'])
    item = db.session.query(Items).filter_by(item_id=item_id).first()
    name = item.name
    # 判斷Session中是否有購物車數據
    if 'reservations' not in session.keys():
        session['reservations'] = []  

    reservations = session['reservations']
    # flag 如果0表示預約單中没有當前商品,1表示預約單代表有當前商品
    flag = 0
    for item in reservations:
        if item[0] == item_id:  # item[0]保存在預約單的物品id
            item[2] += 1  # item[3]保存在預約單的物品數量,對當前數量+1
            flag = 1
            break

    if flag == 0:
        # 第一次添加商品到預約數量是1
        reservations.append([item_id, name, 1])

    session['reservations'] = reservations

    flash('已經添加物品【' + name + '】到預約清單')
    return redirect(url_for('show_items_list'))