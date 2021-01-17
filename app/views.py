from flask import Flask, request, session, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from app.forms import CustomerRegForm, LoginForm
from app.models import Users, Items, Records, Reservation
import config
import random
import datetime
from datetime import date
from datetime import datetime


app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)

@app.context_processor
def inject_now():
    return {'now': datetime.now().strftime('%Y-%m-%d')}

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
    
@app.route('/submit_reservations', methods=['POST'])
def submit_reservations():
    # 從表單中取出數據添加到Orders模式對象中
    reserve = Reservation()
    reservation_list = request.form.getlist("reservation_list")
    for key in request.form:
         print("key:", key)
    for checkbox in reservation_list:
        print("checkbox:", checkbox)
    #print("reservation_list:", reservation_list)
    # for item in reservation_list:
    #     # 生成訂單id，規則為當前時間戳記+一位隨機數
    #     n = random.randint(0, 9)
    #     d = datetime.datetime.today()
    #     reservation_id = str(int(d.timestamp() * 1e6)) + str(n)
    #     reserve.reservation_id = reservation_id
    #     reserve.item_id = 
    #     reserve.user_id = session['customer']['id']
    #     reserve.reverse_date = d.strftime('%Y-%m-%d %H:%M:%S')
    #     db.session.add(reserve)
    # db.session.commit()
    # 清除預約清單
    session.pop('reservations', None)
    return render_template('reserve_ok.html')

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

    # Add session
    session['reservations'].append([item_id, name, 1])

    flash('已經添加物品【' + name + '】到預約清單')
    return redirect(url_for('show_items_list'))

# 顯示用戶資訊
@app.route('/account')
def account():
    if 'customer' not in session.keys():
        flash('您還沒有登入哦！')
        return redirect(url_for('login'))
    acn = db.session.query(Users).filter_by(user_id=session['customer']['id']).first()
    return render_template('account.html', acn=acn)

# 添加借用頁面
@app.route('/add_borrows')
def add_borrows():
    if 'customer' not in session.keys():
        flash('您還沒有登入哦！')
        return redirect(url_for('login'))

    item_id = int(request.args['item_id'])
    item = db.session.query(Items).filter_by(item_id=item_id).first()
    name = item.name
    available_day = item.available_day
    return_date = item.return_date
    # 判斷Session中是否有購物車數據
    if 'borrows' not in session.keys():
        session['borrows'] = []
    elif item_id in ([x[0] for x in session['borrows']]):
        flash('物品ID=【'+str(item_id)+'】的【'+ name + '】：已加入過借用清單')
    else:
        # Add session
        session['borrows'].append([item_id, name, available_day, return_date, 1])
        print(session['borrows'])
        flash('物品ID=【'+str(item_id)+'】的【'+ name + '】：成功加入借用清單')

    return redirect(url_for('show_items_list'))

# 借用頁面
@app.route('/borrows', methods=['GET', 'POST'])
def borrows():
    if 'customer' not in session.keys():
        flash('您還沒有登入哦！')
        return redirect(url_for('login'))
  
    if 'borrows' not in session.keys():
        return render_template('borrows.html', list=[])
    
    borrows = session['borrows']
    list = []
    for item in borrows:
        # 購物車每一个元素[商品id, 商品名稱, 商品價格, 商品數量]
        new_item = (item[0], item[1], item[2], item[3])
        list.append(new_item)
    print('list:', list)
    print(list[0][1])
    return render_template('borrows.html', list=list)
    
@app.route('/submit_borrows', methods=['POST'])
def submit_borrows():
    # 從表單中取出數據添加到Orders模式對象中
    borrows = Records()
    borrows_list = request.form.getlist('check')
    print("borrows_list:", borrows_list)
    print('session:', session['customer'])
    # for item in reservation_list:
    #     # 生成訂單id，規則為當前時間戳記+一位隨機數
    #     n = random.randint(0, 9)
    #     d = datetime.datetime.today()
    #     reservation_id = str(int(d.timestamp() * 1e6)) + str(n)
    #     reserve.reservation_id = reservation_id
    #     reserve.item_id = 
    #     reserve.user_id = session['customer']['id']
    #     reserve.reverse_date = d.strftime('%Y-%m-%d %H:%M:%S')
    #     db.session.add(reserve)
    # db.session.commit()
    # 清除購物車
    session.pop('borrows', None)
    return render_template('borrows_ok.html')