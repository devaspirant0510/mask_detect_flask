from flask import Flask,request,render_template,redirect,url_for,session,flash
from flask_mysqldb import MySQL,MySQLdb
import bcrypt
import pandas as pd
from time import sleep
import covid

#실행할때 Static 폴더에 있는 사진 모두 비우기
#csv 초기화 할때 static/dataset에서 csv초기화 프로그램 실행
#텐서플로우 모델 먼저 실행후
#플라스크 서버 실행

loc=covid.local_cov  # 국내 확진자
glo=covid.global_cov # 해외 확진자
acc=covid.cov_accumulate # 누적 확진자
acc_now=covid.cov_accumulate_now # 전일대비 확진자
check=covid.check_data_li # 검사현황
jun=covid.junilldataset # 전일 대비 확진자 데이터
dead=covid.deaddataset # 사망자 데이터
qua=covid.quarantine_release_dataset # 격리해제 데이터
nuj=covid.nujukdataset # 누적확진자 데이터
iso=covid.isolationdataset # 격리데이터


app=Flask(__name__)

#데이터 베이스 정보 입력
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']= 'your password'
app.config['MYSQL_DB']='your db name'
app.config['MYSQL_CURCORCLASS']='DictCursor'
mysql=MySQL(app)

num=1


#메인페이지
@app.route('/')
def home():
    print(session)
    return render_template("index.html")

#로그인 페이지
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
                session['username'] = user['username']
                flash(f"{session['username']}님 환영합니다.","success")
                return redirect(url_for("home"))
            else:
                flash("아이디 또는 비번이 다릅니다.",'danger')
                return render_template("login.html")
        else:
            flash("아이디 또는 비번이 다릅니다.", 'danger')
            return render_template("login.html")
    else:
        return render_template("login.html")

#로그아웃 할시
@app.route("/logout")
def logout():
    #세션정보 모두 삭제
    session.clear()
    flash("로그아웃 하였습니다.","danger")
    #홈으로 리다이렉트
    return redirect(url_for("home"))

#회원가입페이지
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
        #다를경우 경고메시지 출력 회원가입 페이지로 리다이렉트
        if password!=check:
            flash("비밀번호가 다릅니다.",'danger')
            return render_template("register.html")
        # if len(userid)<4 or len(username)<4 or len(password)<4:
        #     flash("4글자 이상 입력해주세요","danger")
        #     return render_template("register.html")
        else:
            #회원가입 모든정보가 정삭적으로 입력될경우
            #회원가입정보 db에 저장
            cur=mysql.connection.cursor()
            cur.execute("INSERT INTO user (username,email,userid,password) VALUES (%s,%s,%s,%s)",(username,email,userid,hash_password))
            mysql.connection.commit()
            #성공메시지 출력
            flash("회원가입에 성공하셨습니다.","success")
            #홈으로 리다이렉트
            return  redirect(url_for('home'))
    else:
        return render_template("register.html",a=covid.check_data_li[0],b=covid.check_data_li[1],c=covid.check_data_li[2])

#내정보
@app.route("/profile")
def profile():
    if len(session)!=0:
        return render_template("profile.html")
    else:
        flash("로그인후 이용해주세요","danger")
        return redirect(url_for("home"))

#사진입력페이지
@app.route("/photo",methods=['GET','POST'])
def photo():
    global df
    #세션데이터에 로그인 기록이 있으면 photo 페이지로 이동
    if len(session)!=0:
        global num
        if request.method=='POST':
            file=request.files.get('test')
            #input태그에서 file 가져옴
            file.save(f"static/aa{num}.jpg")
            # userdata.csv 불러오기
            df = pd.read_csv("static/dataset/userdataset.csv")
            addli=pd.DataFrame({'user':[session['username']],
                                'id':[session['userid']]})
	        #유저 이름과 아이디 데이터프레임에 저장
            # 기존 데이터 프레임과 새로 생성된 데이터 프레임 concat
            df=pd.concat([df,addli],ignore_index=True)
	        #데이터 프레임 concat될때마다 unnamed 행 생기는 오류 방지위해
            #uname이 포함된 행 삭제
            df.drop(df.filter(regex="Unname"), axis=1, inplace=True)
            print(df)
            #데이터 프레임 저장
            df.to_csv("static/dataset/userdataset.csv")
            num+=1
            #결과 사진 보여줌
            return redirect(url_for("upload"))
        return render_template("photo.html")
    #세션데이터에 로그인 기록이 없다면 경고메시지
    else:
        flash("로그인후 이용해주세요","danger")
        return redirect(url_for("home"))

#업로드
@app.route('/upload',methods=['GET','POST'])
def upload():
    global num
    if request.method=='POST':
        return redirect(url_for("home"))
    else:
        #대기시간
        sleep(5)
        #판다스 데이터 불러옴
        maskdf=pd.read_csv("static/dataset/dataset.csv")
        print(maskdf)
        #판드스 데이테 인덱스를 기준으로 사진 인덱스 번호 선택
        pandanum=len(maskdf)-1
        #마스크 쓴 사람과 안쓴사람의 수 전달
        #서버로 전달
        maskd=maskdf['mask'][pandanum]
        nomaskd=maskdf['nomask'][pandanum]
        print(maskd,nomaskd)
        n=num-1
        #최종적으로 maskd와 nomaskd의 값을 html에 전달
        return render_template("upload.html",num=num-1,maskd=maskd,nomaskd=nomaskd)

#확진자 정보 데이터
@app.route('/covidgui')
def covidgui():
#해당값 그대로 전달
    return render_template("covid.html",loc=loc,glo=glo,acc=acc,check=check,\
                           jun=jun,dead=dead,qua=qua,nuj=nuj,iso=iso)

#깃허브 주소 연결
@app.route("/github")
def github():
    return url_for("https://github.com/devaspirant0510/")

if __name__=='__main__':
    app.secret_key="1234567890"
    app.run(debug=True)
