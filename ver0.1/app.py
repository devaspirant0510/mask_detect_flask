from flask import Flask,request,render_template,redirect,url_for,session,flash
from flask_mysqldb import MySQL,MySQLdb
import bcrypt

#텐서플로우 모델 먼저 실행후
#플라스크 서버 실행

app=Flask(__name__)

#데이터 베이스 정보 입력
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''#비밀번호
app.config['MYSQL_DB']='flasklogin'
app.config['MYSQL_CURCORCLASS']='DictCursor'
mysql=MySQL(app)

num=1

@app.route('/')
def home():
    return render_template("index.html")

@app.route("/login",methods=['POST','GET'])
def login():
    if request.method=='POST':
        userid= request.form.get("id")
        password=request.form.get("password").encode('utf-8')
        curl=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM user WHERE userid=%s", (userid,))
        # user db에 있는 아이디와 로그인페이지에서 입력한 아이디가 매치되는지 확인
        user=curl.fetchone()
        curl.close()
        # curl값이  None이면 매치되는 아이디가 없음
        # 즉 !=None 매치되는 아이디가 있을때 실행
        if user!=None:
            # 아이디가 매치될경우 비밀번호도 매치되는지 확인
            if bcrypt.hashpw(password, user['password'].encode('utf-8')) == user['password'].encode("utf-8"):
                session['userid'] = user['userid']
                session['password'] = user['password']
                return redirect(url_for("home"))
            else:
                flash("아이디 또는 비번이 다릅니다.",'danger')
                return render_template("register.html")
        else:
            flash("아이디 또는 비번이 다릅니다.", 'danger')
            return render_template("register.html")
    else:
        return render_template("login.html")

@app.route("/register",methods=['POST','GET'])
def register():
    if request.method=='POST':
        #input태그값 모두 가져오기
        username = request.form.get('name')
        email = request.form.get('email')
        userid=request.form.get('id')
        password=request.form.get('password').encode('utf-8')
        #비번 암호화
        hash_password=bcrypt.hashpw(password,bcrypt.gensalt())
        check=request.form.get('check').encode('utf-8')
        print(hash_password)
        #처음입력한 비번과 비번 재확인 비번이 같은지 확인
        if password!=check:
            flash("비밀번호가 다릅니다.",'danger')
            return render_template("register.html")
        # if len(userid)<4 or len(username)<4 or len(password)<4:
        #     flash("4글자 이상 입력해주세요","danger")
        #     return render_template("register.html")
        else:
            #회원가입정보 db에 저장
            cur=mysql.connection.cursor()
            cur.execute("INSERT INTO user (username,email,userid,password) VALUES (%s,%s,%s,%s)",(username,email,userid,hash_password))
            mysql.connection.commit()

            return  redirect(url_for('home'))
    else:
        return render_template("register.html")

@app.route("/photo",methods=['GET','POST'])
def photo():
    global num
    if request.method=='POST':
        file=request.files.get('test')
        file.save(f"static/aa{num}.jpg")
        num+=1
        return redirect(url_for("upload"))
    return render_template("photo.html")

@app.route('/upload',methods=['GET','POST'])
def upload():
    global num

    print(num)
    if request.method=='POST':
        return "s"
    else:
        return render_template("upload.html",num=num-1)


if __name__=='__main__':
    app.secret_key='($*%N#Fk34hf9@^Fb3k2'
    app.run(debug=True)
