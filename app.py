from flask import Flask,render_template,request
import mysql.connector as py 

app = Flask(__name__)
mydb = py.connect(
    # host="sql7.freesqldatabase.com",
    host="di.c04skukvkgsx.eu-west-2.rds.amazonaws.com",
    user="admin",
    passwd="coding123-",
    database = "di",
)
mycursor = mydb.cursor()
def insertcontact (name , email , phone , message):
    # print(name , email , phone , message)
    dataa= (
        name , email , phone , message
    )
    mycursor.execute("INSERT INTO contact (name,email,phone,message) VALUES (%s,%s,%s,%s)",dataa)
    mydb.commit()
contactdetlist = []
def fetchall():
    contactdetlist.clear()
    mycursor.execute("SELECT * FROM contact")
    myresult = mycursor.fetchall()
    # print(myresult)
    contactdetlist.append(myresult)
@app.route("/")
def home():
    # mycursor.execute("")
    mycursor.execute("SELECT * FROM posts")
    myresult = mycursor.fetchall()
    return render_template('index.html',posts = myresult)
@app.route("/contactdet")
def contactdet():
    fetchall()
    return render_template('ContactDet.html',mylist = contactdetlist[0])
@app.route("/about")
def about():
    return render_template('about.html')
@app.route("/contact")
def contact():
    return render_template('contact.html', ins = insertcontact)
@app.route("/post/<string:post_key>" , methods= ["GET"])
def post(post_key):
    mycursor.execute(f"select * from posts where keyauto = '{post_key}'")
    myresult =  mycursor.fetchall()
    
    return render_template('post.html',post = myresult[0], datee = myresult[0][9])
@app.route("/addblog")
def addform():
    return render_template('AddForm.html')

@app.route('/result',methods=['post', 'GET'])
def result():
    output = request.form.to_dict()
    # print(",   ",request.form.to_dict())
    # name = output["name"]
    insertcontact(output["name"],output["email"],output["phone"],output["message"])
    return render_template("Thanku.html")
addphone = []
addname = []
@app.route('/otp',methods=['post', 'GET'])
def otp():
    output = request.form.to_dict()
    # print()
    
    import pywhatkit
    import datetime
    a = datetime.datetime.now()
    # print(a)
    import random
    OTP1 = random.randint(0,9999)
    message =  f'HI {output["name"]}, \nyour otp is {OTP1} '
    # print(message)


    # name = output["name"]
    # insertcontact(output["name"],output["email"],output["phone"],output["message"])
    # insertcontact
    addphone.append(output['phone'])
    addname.append(output['name'])
    # pywhatkit.sendwhatmsg("+91"+output["phone"] , message, int(a.strftime("%H")),int(a.strftime("%M"))+1,15, True, 2)
    return (render_template("Otp.html",OTP = OTP1))

@app.route("/addyourblog" , methods=['post','get'])
def blogadd():
    return render_template('finalAdd.html')
@app.route("/resultpost" , methods=['post','get'])
def resultpost():
    
    output = request.form.to_dict()
    title = output["title"]
    subtitle = output["subtitle"]
    # description = output["description"]
    import datetime
    import secrets
    keykey = secrets.token_hex(2)
    # print()
    x = datetime.datetime.now()
    datee = f'{x.strftime("%d")}-{x.strftime("%B")}-{x.strftime("%Y")}, {x.strftime("%a")}'
    data1 = (title,subtitle,output["Fsubheading"],output["Fdescription"],output["Ssubheading"],output["Sdescription"],output["Tsubheading"],output["Tdescription"],addphone[0],datee,keykey,addname[0])
    mycursor.execute('INSERT INTO posts (title,subtitle,Ftitle,Fdesc,Ssubheading,Sdesc,Tsubheading,Tdesc,userphone,dateT,keyauto,nameAuthor) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',data1)
    mydb.commit()
    addphone.clear()
    addname.clear()
    return render_template('Thanku.html')

@app.route('/searchresult',methods=['post', 'GET'])
def searchresult():
    output = request.form.to_dict()
    print(output)
    command = f"SELECT * FROM posts WHERE title LIKE %s"
    mycursor.execute(command,[output['searchh']])
    myresult = mycursor.fetchall()
    print(myresult)
    # name = output["name"]
    # insertcontact(output["name"],output["email"],output["phone"],output["message"])
    # return render_template("Thanku.html")
    return render_template('index.html',posts = myresult)
app.run(debug=True)

