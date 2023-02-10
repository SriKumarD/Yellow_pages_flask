from flask import Flask, render_template, request,redirect,jsonify,url_for
import sqlite3 
import re

app = Flask(__name__)
@app.route("/")  
def index():
    return render_template("home.html",msg=["","","T"]); 
def check(obj):
    name=obj['name']
    email=obj['email']
    phone=obj['phonenumber']
    address=obj['address']
    if(not(re.match('^[a-z A-Z][a-z A-Z . \s]+$',name))):
        return "name"
    elif(not(re.match('^[0-9]{10}$',phone))):
        return "phone"
    elif(email == ""):
        return "email"
    elif(address == ""):
        return "address"
    else:
        return "true"

@app.route("/detailssaved",methods = ["POST"])  
def saveDetails(): 
    msg =[]
    error=check(request.form) 
    name=request.form['name']
    email=request.form['email']
    phone=request.form['phonenumber']
    address=request.form['address']
    if request.method == "POST":
        try:
            if(error == 'true'):
                with sqlite3.connect("data.db") as con:  
                    cur = con.cursor()  
                    cur.execute("INSERT into info (name,email,pnum,address) values (?,?,?,?)",(name,email,phone,address))
                    con.commit()     
                    msg.append("T")
                    msg.append("Record Added succesfully")
                    msg.append("T")
            else:
                msg.append("F")
                if(error == "name"):
                    msg.append('Please enter valid name')
                elif(error == "email"):
                    msg.append('Please enter valid email')
                elif(error == "phone"):
                    msg.append('Please enter 10 digits phone number')
                elif(error == "address"):
                    msg.append('Please enter valid address')
                else:
                    msg.append('Grade of student should be less or equal to 100')
                msg.append("T")            
        except:   
            msg.append("F")
            msg.append("User with phone number "+phone+" already exist.Try with another number")
            msg.append("T")
            con.rollback()  
        finally: 
            return render_template("home.html",msg=msg);  
            con.close()
@app.route("/updatedetails",methods = ["POST"])  
def updateDetails():
    msg=[]  
    phone =request.form["ph"]
    print(phone)
    if request.method == "POST":
        if(check_phone(int(phone))):
            try:
                con = sqlite3.connect("data.db")  
                con.row_factory = sqlite3.Row 
                cur = con.cursor()  
                cur.execute("select * from info where pnum="+str(phone))  
                rows = cur.fetchall()
                print(rows)
                return render_template("update.html",rows = rows,msg=["",""])
            except:   
                msg.append("F")
                msg.append("No Record Found With This Number"+str(phone))
                msg.append("U")
                con.rollback() 
                return render_template("home.html",msg=msg)  
            finally:
                con.close() 
        else:
            msg.append("F")
            msg.append("No Record Found With This Number "+str(phone))
            msg.append("U") 
            return render_template("home.html",msg=msg) 
               
         
@app.route("/view")  
def viewallgrades():  
    con = sqlite3.connect("data.db")  
    con.row_factory = sqlite3.Row 
    cur = con.cursor()  
    cur.execute("select * from info")  
    rows = cur.fetchall() 
    return render_template("results.html",rows = rows)   
@app.route("/search",methods = ["POST"])  
def viewpass():
    single_word=request.form['ss']
    regx = r"(" +re.escape(single_word) + r")"
    num_list=[]  
    con = sqlite3.connect("data.db")  
    con.row_factory = sqlite3.Row  
    cur = con.cursor()  
    cur.execute("select * from info")  
    rows = cur.fetchall()
    for row in rows:
        val=str(row["pnum"])
        if(re.search(regx,val)):
             num_list.append(row) 
    return render_template("results.html",rows = num_list)  

@app.route("/del")  
def inde():  
    return render_template("home.html",msg=["","","F"]) 

@app.route("/update")  
def updt():  
    return render_template("home.html",msg=["","","U"]) 
@app.route("/updatedata",methods = ["POST"])  
def updtdata():
    msg =[]
    error=check(request.form) 
    name=request.form['name']
    email=request.form['email']
    phone=request.form['phonenumber']
    address=request.form['address']
    row=datainfo(phone)
    if request.method == "POST":
        try:
            if(error == 'true'):
                with sqlite3.connect("data.db") as con:  
                    cur = con.cursor() 
                    cur.execute("""UPDATE info SET name = ? ,email = ?,address= ? WHERE pnum= ? """,(name,email,address,phone))
                    con.commit()     
                    msg.append("T")
                    msg.append("Record updated succesfully")
                    msg.append("U")
                    return render_template("home.html",msg=msg)
            else:
                msg.append("F")
                if(error == "name"):
                    msg.append('Please enter valid name')
                elif(error == "email"):
                    msg.append('Please enter valid email')
                elif(error == "phone"):
                    msg.append('Please enter 10 digits phone number')
                elif(error == "address"):
                    msg.append('Please enter valid address')
                else:
                    msg.append('Grade of student should be less or equal to 100')
                return render_template("update.html",rows=row,msg=msg)           
        except:   
            msg.append("F")
            msg.append("Cannot insert recored check your inputs") 
            return render_template("update.html",rows=row,msg=msg) 
        finally:
            con.close()
def datainfo(phn):
    con = sqlite3.connect("data.db")  
    con.row_factory = sqlite3.Row 
    cur = con.cursor()  
    cur.execute("select * from info where pnum="+str(phn))  
    rows = cur.fetchall()
    return rows
def check_phone(ph_num):
    num_list=[]
    con = sqlite3.connect("data.db")  
    con.row_factory = sqlite3.Row  
    cur = con.cursor()  
    cur.execute("select * from info")  
    rows = cur.fetchall()
    print(rows)
    for row in rows:
        num_list.append(row["pnum"])
    print(num_list)
    print(ph_num)
    if(ph_num in num_list):
        print('yes')
        return True
    else:
        return False
@app.route("/deleterecord",methods = ["POST"])  
def deleterecord():  
    phone =request.form["ph"]
    msg =list()
    with sqlite3.connect("data.db") as con:  
        try:
            if(check_phone(int(phone))):
                cur = con.cursor()
                cur.execute("delete from info where pnum="+str(phone))
                con.commit()
                msg.append("T")
                msg.append("Record successfully deleted")
                msg.append("F")
                return render_template("home.html",msg=msg)
            else:
                msg.append("F")
                msg.append("Record with Phone Number "+phone+" not found")
                msg.append("F")
                return render_template("home.html",msg=msg)
        except:
            msg.append("F")  
            msg.append("Can't be deleted")
            msg.append("F")
            con.close()
            return render_template("home.html",msg=msg)

if __name__ == '__main__':
   app.run(debug = True)