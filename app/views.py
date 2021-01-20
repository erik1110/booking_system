from flask import Flask, request, session, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from app.forms import CustomerRegForm, LoginForm
from app.models import Users, Items, Orders, ItemsHist
import config
import random
import datetime
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)

# 當前日期
@app.context_processor
def inject_now():
    return {'now': datetime.now().strftime('%Y-%m-%d')}

# 註冊頁面
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

# 登入頁面
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

# 主頁面
@app.route('/main')
def main():
    if 'customer' not in session.keys():
        flash('您還沒有登入哦！')
        return redirect(url_for('login'))
    return render_template('main.html')

# 顯示用戶資訊
@app.route('/account')
def account():
    if 'customer' not in session.keys():
        flash('您還沒有登入哦！')
        return redirect(url_for('login'))
    acn = db.session.query(Users).filter_by(user_id=session['customer']['id']).first()
    return render_template('account.html', acn=acn)

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

# 歸還頁面
@app.route('/returns', methods=['GET', 'POST'])
def returns():
    if 'customer' not in session.keys():
        flash('您還沒有登入哦！')
        return redirect(url_for('login'))
    else:
        result = db.session.query(Items.name, \
                                  Items.user_id, \
                                  Items.borrow_date, \
                                  Items.expected_date, \
                                  Items.booking_status, \
                                  ItemsHist.borrow_order_id, \
                                  ItemsHist.item_id, \
                                  ItemsHist.hist_id). \
                                  filter_by(user_id=session['customer']['id'], booking_status='已借出'). \
                            join(Items, Items.item_id==ItemsHist.item_id)
        return render_template('returns.html', list=result)

# 歸還成功頁面
@app.route('/submit_returns', methods=['POST'])
def submit_returns():
    # 初始化 Orders 對象
    orders = Orders() 
    # 從前端拉回資訊
    returns_list = request.form.getlist('check')
    # 創立單據號碼
    today = datetime.today()
    n = random.randint(0, 9)
    order_id = 'RET' + str(datetime.today().timestamp() * 1e6) + str(n)
    orders.order_id = order_id
    orders.action = '歸還'
    orders.user_id = session['customer']['id']
    orders.total = len(returns_list)
    orders.order_date = today
    db.session.add(orders)
    # 更新資訊
    for hist_id in returns_list:
        # 更新 ItemsHist 新增資訊
        db.session.query(ItemsHist).filter_by(hist_id=hist_id).update(dict(
                                                               return_date=today,
                                                               return_order_id=order_id))
        item_id = db.session.query(ItemsHist).filter_by(hist_id=hist_id).first().item_id                  
        # 更新物品狀態為未借閱
        db.session.query(Items).filter_by(item_id=item_id).update(dict(user_id='',
                                                                       borrow_date='',
                                                                       expected_date='',
                                                                       return_date='',
                                                                       reserve_date='',
                                                                       booking_status='未借出'))
    db.session.commit()
    return render_template('return_ok.html', order_id=order_id, returns_list=returns_list)

# 添加預約頁面
@app.route('/add_reservation')
def add_reservation():
    if 'customer' not in session.keys():
        flash('您還沒有登入哦！')
        return redirect(url_for('login'))
    item_id = request.args['item_id']
    item = db.session.query(Items).filter_by(item_id=item_id).first()
    name = item.name
    # 判斷Session中是否有購物車數據
    if 'reservations' not in session.keys():
        session['reservations'] = []
    if item_id in ([x[0] for x in session['reservations']]):
        flash('物品ID=【'+str(item_id)+'】的【'+ name + '】已加入過預約清單')
    else:
        # Add session
        session['reservations'].append(item_id)
        flash('物品ID=【'+str(item_id)+'】的【'+ name + '】加入預約清單')
    return redirect(url_for('show_items_list'))

# 預約頁面
@app.route('/reservations', methods=['GET', 'POST'])
def reservations():
    if 'customer' not in session.keys():
        flash('您還沒有登入哦！')
        return redirect(url_for('login'))
  
    if 'reservations' not in session.keys():
        return render_template('reservations.html', list=[])
    
    item_ids = session['reservations']
    data_list = []
    for item_id in item_ids:
        items = db.session.query(Items).filter_by(item_id=item_id).first()
        data_list.append([items.item_id, items.name, items.booking_status, items.expected_date])
    
    return render_template('reservations.html', data_list=data_list)
    
@app.route('/submit_reservations', methods=['POST'])
def submit_reservations():
    user_id = session['customer']['id']
    # 從表單中取出數據添加到 Reservation 模式對象中
    reserve_list = request.form.getlist("reserve_checked")
    print("reservation_list:", reserve_list)
    # 檢查是否有被預約
    for item_id in reserve_list:
        items = db.session.query(Items).filter_by(item_id=item_id).first()
        if items.reserve_status=='已預約':
            flash('有人已經搶先預約過【' + items.name + '】成功了！')
            return redirect(url_for('reservations'))
    # 初始化 Orders 對象
    orders = Orders() 
    # 創立單據號碼
    n = random.randint(0, 9)
    order_id = 'RES' + str(datetime.today().timestamp() * 1e6) + str(n)
    orders.order_id = order_id
    orders.action = '預約'
    orders.user_id = session['customer']['id']
    orders.total = len(reserve_list)
    orders.order_date = datetime.today()
    db.session.add(orders)
    # 寫入Resevation
    data＿list = []
    for item_id in reserve_list:
        itemshist = ItemsHist()
        # 寫入物品歷史紀錄
        n = random.randint(0, 9)
        itemshist.hist_id = 'HIST' + str(datetime.today().timestamp() * 1e6) + str(n)
        itemshist.item_id = item_id
        itemshist.user_id = session['customer']['id']
        itemshist.reverse_date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        itemshist.reserve_order_id = order_id
        data_list.append(itemshist)
        # 更新物品資訊為已預約
        db.session.query(Items).filter_by(item_id=item_id).update(dict(user_id='',
                                                                       borrow_date='',
                                                                       expected_date='',
                                                                       return_date='',
                                                                       reserve_date='',
                                                                       reserve_status='已預約'))
    db.session.add_all(data_list)
    db.session.commit()
    # 清除預約清單
    session.pop('reservations', None)
    return render_template('reserve_ok.html')

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
    # 判斷Session中是否有購物車數據
    if 'borrows' not in session.keys():
        session['borrows'] = []

    if item_id in ([x[0] for x in session['borrows']]):
        flash('物品ID=【'+str(item_id)+'】的【'+ name + '】：已加入過借用清單')
    else:
        # Add session
        session['borrows'].append([item_id, name, available_day])
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
        new_item = (item[0], item[1], item[2])
        list.append(new_item)
    print('list:', list)
    print(list[0][1])
    return render_template('borrows.html', list=list)

# 借用成功頁面
@app.route('/submit_borrows', methods=['POST'])
def submit_borrows():
    # 創立單據詳細資訊 
    borrows_list = request.form.getlist('check')
    # 創立單據號碼
    orders = Orders()
    d = datetime.today()
    order_id = 'BOR' + str(d.strftime('%Y%m%d%H%M%S'))
    orders.order_id = order_id
    orders.action = '借用'
    orders.user_id = session['customer']['id']
    orders.order_date = d.strftime('%Y-%m-%d')
    orders.total =  len(borrows_list)
    db.session.add(orders)

    data = []
    for item in borrows_list:
        num_day = db.session.query(Items).filter_by(item_id=int(item)).first().available_day
        items_hist = ItemsHist()
        items_hist.hist_id = 'I' + item.zfill(3) + 'D' + str(d.strftime('%Y%m%d%H%M%S'))
        items_hist.item_id = int(item)
        items_hist.user_id = session['customer']['id']
        items_hist.borrow_date = d.strftime('%Y-%m-%d')
        items_hist.expected_date = (d + relativedelta(days=num_day)).strftime('%Y-%m-%d')
        items_hist.borrow_order_id = order_id
        data.append(items_hist)
        # 更新物品狀態為已借用
        db.session.query(Items).filter_by(item_id=int(item)).update(dict(user_id=items_hist.user_id,
                                                                         borrow_date=items_hist.borrow_date,
                                                                         expected_date=items_hist.expected_date,
                                                                         return_date='',
                                                                         booking_status='已借出'))
    db.session.add_all(data)
    db.session.commit()
    session.pop('borrows', None)
    return render_template('borrows_ok.html', order_id=order_id)
