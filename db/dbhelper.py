import sqlite3

DB_FILES = './db/database.db'

# 創建數據庫中的表
def create_tables():
    f_name = 'db/store-schema.sql'
    with open(f_name, 'r', encoding='utf-8') as f:
        sql = f.read()
        conn = sqlite3.connect(DB_FILES)
        try:
            conn.executescript(sql)
            print('數據庫初始化成功')
        except Exception as e:
            print('數據庫初始化失敗')
            print('失敗原因：', e)
        finally:
            conn.close()


# 數據庫的借用物品插入數據
def load_data():
    f_name = './db/store-dataload.sql'
    with open(f_name, 'r', encoding='utf-8') as f:
        sql = f.read()
        conn = sqlite3.connect(DB_FILES)
        try:
            conn.executescript(sql)
            print('數據庫插入資料成功')
        except Exception as e:
            print('數據庫插入資料失敗')
            print('失敗原因：', e)
        finally:
            conn.close()
