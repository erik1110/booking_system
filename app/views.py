from flask import Flask, request, session, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from app.forms import CustomerRegForm, LoginForm, MessageForm
from app.models import Users, Items, Orders, ItemsHist, Comments
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

# 顯示其他用戶資訊
@app.route('/other_account')
def other_account():
    if 'customer' not in session.keys():
        flash('您還沒有登入哦！')
        return redirect(url_for('login'))
    user_id = request.args['user_id']
    acn = db.session.query(Users).filter_by(user_id=user_id).first()
    return render_template('account.html', acn=acn)

@app.route('/list')
def show_items_list():
    if 'customer' not in session.keys():
        flash('您還沒有登入哦！')
        return redirect(url_for('login'))
    items_list = db.session.query(Items).all()
    popular = db.session.query( ItemsHist.user_id , func.count('*').label('times') ).group_by( ItemsHist.user_id ).order_by(func.count('*').desc())
    item_popu = (db.session.query(Items.name, Items.description, func.count(ItemsHist.item_id).label('times'))
                                .join(ItemsHist, Items.item_id == ItemsHist.item_id)
                                .group_by(ItemsHist.item_id)).order_by(func.count(ItemsHist.item_id).desc())
    return render_template('items_list.html', list=items_list, popular=popular, item_popu=item_popu)

# 顯示歷史借用物品列表
@app.route('/record_history')
def show_items_list_hist():
    if 'customer' not in session.keys():
        flash('您還沒有登入哦！')
        return redirect(url_for('login'))
    items_list = db.session.query(ItemsHist.borrow_date, ItemsHist.return_date, Items.item_id, Items.name).filter_by(user_id=session['customer']['id']).join(Items,Items.item_id == ItemsHist.item_id, isouter=True).all()
    return render_template('record_hist.html', list=items_list)

# 顯示借用物品詳細資訊
@app.route('/detail')
def show_items_detail():
    if 'customer' not in session.keys():
        flash('您還沒有登入哦！')
        return redirect(url_for('login'))
    item_id = request.args['item_id']
    item = db.session.query(Items).filter_by(item_id=item_id).first()
    # 刷留言區
    form = MessageForm()
    if form.validate_on_submit():
        ## 初始化 Comments 對象
        comments = Comments() 
        ## 創立單據號碼
        d = datetime.today()
        comments.comment_id = 'COM' + str(d.strftime('%Y%m%d%H%M%S'))
        comments.item_id = item_id
        comments.user_id = session['customer']['id']
        comments.content = request.form["content"]
        comments.comment_date = d
        flash('留言成功')
        redirect('/detail')
    messages = db.session.query(Comments).order_by(Comments.comment_date.desc()).all()
    return render_template('items_detail.html', 
                           item=item,
                           user_id=session['customer']['id'],
                           form=form, messages=messages)
# 單據管理頁面
@app.route('/order_list')
def show_order_list():
    if 'customer' not in session.keys():
        flash('您還沒有登入哦！')
        return redirect(url_for('login'))
    order_list = db.session.query(Orders).filter_by(user_id=session['customer']['id']).all()

    return render_template('order_list.html', list=order_list)

# 單據管理詳細頁面
@app.route('/order_list_detail', methods=['GET'])
def show_order_detail():
    if 'customer' not in session.keys():
        flash('您還沒有登入哦！')
        return redirect(url_for('login'))
    order_id = request.args.get('order_id')
    order_status = request.args.get('order_status')
    if order_status == 'borrow':
        hist_list = db.session.query(ItemsHist).filter_by(borrow_order_id=order_id).all()
        return render_template('order_detail_borrow.html', list=hist_list, order_id=order_id)
    elif order_status == 'return':
        hist_list = db.session.query(ItemsHist).filter_by(return_order_id=order_id).all()
        return render_template('order_detail_return.html', list=hist_list, order_id=order_id)
    elif order_status == 'reserve':
        hist_list = db.session.query(ItemsHist).filter_by(reserve_order_id=order_id).all()
        return render_template('order_detail_reserve.html', list=hist_list, order_id=order_id)


# 歸還頁面
@app.route('/returns', methods=['GET', 'POST'])
def returns():
    if 'customer' not in session.keys():
        flash('您還沒有登入哦！')
        return redirect(url_for('login'))
    else:
        result = db.session.query(ItemsHist.item_id, \
                                  ItemsHist.borrow_order_id, \
                                  Items.name, \
                                  ItemsHist.user_id, \
                                  ItemsHist.borrow_date, \
                                  ItemsHist.expected_date, \
                                  ItemsHist.order_status,
                                  ItemsHist.hist_id). \
                                  filter_by(user_id=session['customer']['id'], order_status='borrow'). \
                            join(ItemsHist, ItemsHist.item_id==Items.item_id)
        return render_template('returns.html', list=result)

# 歸還成功頁面
@app.route('/submit_returns', methods=['POST'])
def submit_returns():
    # 初始化 Orders 對象
    orders = Orders() 
    # 從前端拉回資訊
    returns_list = request.form.getlist('check')
    # 創立單據號碼
    d = datetime.today()
    order_id = 'RET' + str(d.strftime('%Y%m%d%H%M%S'))
    orders.order_id = order_id
    orders.order_type = 'return'
    orders.user_id = session['customer']['id']
    orders.total = len(returns_list)
    orders.order_date = d.strftime('%Y-%m-%d')
    db.session.add(orders)
    # 更新資訊
    for hist_id in returns_list:
        # 更新 ItemsHist 新增資訊
        db.session.query(ItemsHist).filter_by(hist_id=hist_id).update(dict(
                                                               return_date=datetime.today(),
                                                               return_order_id=order_id,
                                                               order_status='return'))
        item_id = db.session.query(ItemsHist).filter_by(hist_id=hist_id).first().item_id                  
        # 更新物品狀態為未借閱
        db.session.query(Items).filter_by(item_id=item_id).update(dict(borrow_user_id='',
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
    # 判斷Session中是否有預約單數據
    if 'reservations' not in session.keys():
        session['reservations'] = []
    if item_id in ([x for x in session['reservations']]):
        flash('物品ID=【'+str(item_id)+'】的【'+ name + '】已加入過預約清單')
    else:
        # Add session
        session['reservations'].append(item_id)
        flash('物品ID=【'+str(item_id)+'】的【'+ name + '】成功加入預約清單')
    return redirect(url_for('show_items_list'))

# 預約頁面
@app.route('/reservations', methods=['GET', 'POST'])
def reservations():
    if 'customer' not in session.keys():
        flash('您還沒有登入哦！')
        return redirect(url_for('login'))
    # 目前您的預約清單
    data_list1 = db.session.query(ItemsHist.item_id, \
                              ItemsHist.borrow_order_id, \
                              Items.name, \
                              Items.borrow_user_id, \
                              Items.expected_date, \
                              ItemsHist.reserve_date, \
                              ItemsHist.order_status). \
                              filter_by(user_id=session['customer']['id'], order_status='reserve'). \
                    join(ItemsHist, ItemsHist.item_id==Items.item_id)
    # 本次您想預約清單
    if 'reservations' not in session.keys():
        return render_template('reservations.html', list=[])
    item_ids = session['reservations']
    data_list2 = []
    for item_id in item_ids:
        items = db.session.query(Items).filter_by(item_id=item_id).first()
        data_list2.append([items.item_id, items.name, items.booking_status, items.expected_date])
    
    return render_template('reservations.html', data_list1=data_list1, data_list2=data_list2)
    
@app.route('/submit_reservations', methods=['POST'])
def submit_reservations():
    user_id = session['customer']['id']
    # 從表單中取出數據添加到 Reservation 模式對象中
    item_ids = request.form.getlist("reserve_checked")
    # 檢查是否有被預約
    for item_id in item_ids:
        items = db.session.query(Items).filter_by(item_id=item_id).first()
        if items.reserve_status=='已預約':
            flash('有人已經搶先預約過【' + items.name + '】成功了！')
            return redirect(url_for('reservations'))
    # 初始化 Orders 對象
    orders = Orders() 
    # 創立單據號碼
    d = datetime.today()
    order_id = 'RES' + str(d.strftime('%Y%m%d%H%M%S'))
    orders.order_id = order_id
    orders.order_type = 'reserve'
    orders.user_id = session['customer']['id']
    orders.total = len(item_ids)
    orders.order_date = d.strftime('%Y-%m-%d')
    db.session.add(orders)
    # 寫入Resevation
    data_list = []
    for item_id in item_ids:
        itemshist = ItemsHist()
        # 寫入物品歷史紀錄
        n = random.randint(0, 10000)
        itemshist.hist_id = 'HIST' + str(d.strftime('%Y%m%d%H%M%S')) + str(n)
        itemshist.item_id = item_id
        itemshist.user_id = session['customer']['id']
        itemshist.reserve_date = datetime.today()
        itemshist.reserve_order_id = order_id
        itemshist.order_status = 'reserve'
        data_list.append(itemshist)
        # 更新物品資訊為已預約
        db.session.query(Items).filter_by(item_id=item_id).update(dict(reserve_user_id=session['customer']['id'],
                                                                       reserve_status='已預約'))
    db.session.add_all(data_list)
    db.session.commit()
    # 清除預約清單
    session.pop('reservations', None)
    return render_template('reserve_ok.html', order_id=order_id)

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
        new_item = (item[0], item[1], item[2])
        list.append(new_item)
    return render_template('borrows.html', list=list)

# 借用成功頁面
@app.route('/submit_borrows', methods=['POST'])
def submit_borrows():
    # 創立單據詳細資訊 
    borrows_list = request.form.getlist('check')

    if len(borrows_list)==0:
        flash('未勾選任何物品，無法提交借用單')
        return redirect(url_for('borrows'))
    else:
        # 創立單據號碼
        orders = Orders()
        d = datetime.today()
        order_id = 'BOR' + str(d.strftime('%Y%m%d%H%M%S'))
        orders.order_id = order_id
        orders.order_type = 'borrow'
        orders.user_id = session['customer']['id']
        orders.order_date = d.strftime('%Y-%m-%d')
        orders.total =  len(borrows_list)
        db.session.add(orders)

        data = []
        for item in borrows_list:
            num_day = db.session.query(Items).filter_by(item_id=int(item)).first().available_day
            itemshist = ItemsHist()
            n = random.randint(0, 10000)
            itemshist.hist_id = 'HIST' + str(d.strftime('%Y%m%d%H%M%S')) + str(n)
            itemshist.item_id = int(item)
            itemshist.user_id = session['customer']['id']
            itemshist.borrow_date = d.strftime('%Y-%m-%d')
            itemshist.expected_date = (d + relativedelta(days=num_day)).strftime('%Y-%m-%d')
            itemshist.borrow_order_id = order_id
            itemshist.order_status = 'borrow'
            data.append(itemshist)
            # 更新物品狀態為已借用
            db.session.query(Items).filter_by(item_id=int(item)).update(dict(borrow_user_id=itemshist.user_id,
                                                                             borrow_date=itemshist.borrow_date,
                                                                             expected_date=itemshist.expected_date,
                                                                             return_date='',
                                                                             booking_status='已借出'))
        db.session.add_all(data)
        db.session.commit()
        session.pop('borrows', None)
        return render_template('borrows_ok.html', order_id=order_id)
    
