from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, validators
from wtforms.fields import simple

class LoginForm(Form):
    '''渲染用户登入HTML表單'''

    userid = StringField('用戶帳號：', [validators.DataRequired('用戶帳號必須輸入')])
    password = PasswordField('用戶密碼：', [validators.DataRequired('用戶帳號必須輸入')])


class CustomerRegForm(Form):
    '''渲染客户註冊HTML表单'''

    userid = StringField('用戶帳號：', [validators.DataRequired('用戶帳號必須輸入')])
    name = StringField('用戶姓名：', [validators.DataRequired('用戶姓名必須輸入')])
    password = PasswordField('用戶密碼：', [validators.DataRequired('用戶帳號必須輸入')])
    password2 = PasswordField('再次輸入密碼：', [validators.EqualTo('password', message='兩次密碼不一致')])

    # 驗證的正則表達式 YYYY-MM-DD YY-MM-DD
    reg_date = r'^((((19|20)(([02468][048])|([13579][26]))-02-29))|((20[0-9][0-9])|(19[0-9][0-9]))-((((0[1-9])|(1[0-2]))-((0[1-9])|(1\d)|(2[0-8])))|((((0[13578])|(1[02]))-31)|(((0[1,3-9])|(1[0-2]))-(29|30)))))$'
    birthday = StringField('出生日期：', [validators.Regexp(reg_date, message='輸入的日期無效')])
    address = StringField('通訊地址：')
    phone = StringField('電話號碼：')

# 留言板表单
class MessageForm(Form):
    msg = simple.TextAreaField(
        label='輸入留言',
        validators=[validators.DataRequired()])
    submit = SubmitField(label=u'提交留言' )
