'''
練習プログラム
'''
from bottle import Bottle,\
    jinja2_tempateas as template,\
        static_file, request, redirect
        
from bottle import response, run 
import psycopg2
import psycopg2.extras

#DB接続情報
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'book_data'
DB_USER = 'book_user'
DB_PASS = 'musashi0724'

def get_connection():
    '''
    DBの接続を行う
    '''
    dsn = 'host={host} port={port} dbname={dbname} \
        user={user} passward={passward}'
    dsn = dsn.format(user=DB_USER, passward=DB_PASS, \
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME)
    return psycopg2.connect(dsn)




def index():
    return 'Hello World'

@app.route('/', method=['Get', 'POST'])
def add():
    #ユーザー登録フォームのHTML
    form_html = '''<html>
    <head>登録フォーム</head>
    <body>
    <form action='/add' method='post'>
    ユーザーID:<input type='next' name='passwd' value='<!--passwd-->' /><br />
    パスワード:<input type='text' name='passwd' value='<!--passwd-->' /><br />
    email:<input type='text' name='email' value='<!--email-->' /><br />
    氏：<input type='text' name='user_shi' value='<!--user_shi-->' /><br />
    名：<input type='text' name='user_mei' value='<!--user_mei-->' /><br />
    <input type='submit' value='確認' name='next'/>
    </form>
    </body>
    </html>
    '''
#ユーザー登録　確認画面のHTML
    confirm_html = '''<html>
    <head>登録フォーム</head>
    <body>
    <form action='/regist' method='post'>
    ユーザID:
    パスワード:
    email:<!--email--><br />
    氏:<!--user_shi--><br />
    名:<!--user_mei--><br />
    <input type='hidden' name='user_id' value='<!--user_id-->' />
    <input type='hidden' name='passwd' value='<!--passwd-->' />
    <input type='hidden' name='email' value='<!--email-->' />
    <input type='hidden' name='user_shi' value='<!--user_shi-->' />
    <input type='hidden' name='user_mei' value='<!--user_mei-->' />
    <input type='submit' name='back' name='next'/>$nbsp;&nbsp;
    <input type='submit' name='regist' name='next' />
    </form>
    </body>
    </html>
    '''
    #GETでアクセスされたら
    if request.method == 'GET' or request.forms.get('next') == 'back':
        return form_html.replace('<!--user_id-->','').\
        replace('<!--passward-->','').\
        replace('<!--email-->','').\
        replace('<!--user_shi-->','').\
        replace('<!--user_mei-->','')
    else:
        #postされたフォームの値を取得する
        form = {}
        form['user_id'] = request.forms.decode().get('user_id')
        form['passwd'] = request.forms.decode().get('passwd')
        form['email'] = request.forms.decode().get('email')
        form['user_shi'] = request.forms.decode().get('user_shi')
        form['user_mei'] = request.forms.decode().get('user_mei')
        
        if request.forms.get('next') == 'back':
            #戻る処理
            html = form_html
        else:
            #確認処理
            html = confirm_html
            
        #受け取った値を置換する
        #メソッドは重ね掛けできる
        return html.replace('<--user_id-->', form['user_id']).\
        replace('<!--passwd-->',form['passwd']).\
        replace('<!--email-->',form['email']).\
        replace('<!--user_shi-->',form['user_shi']).\
        replace('<!--user_mei-->',form['user_mei'])
        
@appp.route('/regist', method=['POST'])
def regist():
    if request.forms.get('next') == 'back':
        #確認画面から戻るボタンを押す
        #登録フォームに戻る
        response.status = 307
        response.set_header('Location', '/add')
        return response
    else:
        #フォームから値を入力する
        user_id = request.form.decode().get('user_id')
        passwd = request.form.decode().get('passwd')
        email = request.form.decode().get('email')
        user_shi = request.form.decode().get('user_shi')
        user_mei = request.form.decode().get('user_mei')
        
        #sqlを記入する
        sql = '''insert into ook_user \
        (user_id, passwd, email, user_shi, user_mei, del) \
        values \
        (%(user_id)s, %(passwd)s, %(email)s %(user_shi)s, %(user_mei)s, false);'''
        #入力する値の辞書を設定する
        val = {'user_id':user_id, 'passwd':passwd,\
            'email':email, 'user_shi':user_shi, \
            'user_mei':user_mei}
        with get_connection() as con:# DBの接続を取得
            with con.cursor() as cur:#　カーソルを取得
                cur.execute(sql, val)
            con.commit()
        redirect('/add')
        
@app.route('/list')
def list():
    sql = '''select user_id, email, user_shi,\
        user_mei from book_user \
        where del = false \
        order by user_id asc;'''
    with get_connection() as con:
        with con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            #dict型で受け取りたいので上記のようにオプション指定
            cur.execute(sql)
            rows = cur.fetchall()
            #下記の内容表記を挟む必要がある
            rows = [dict(rows) for row in rows]
    return template('list.html', rows=rows)

if __name__ == '__main__':
    run(app=app, host='0.0.0.0', port=8889, reloader=True, debug=True)