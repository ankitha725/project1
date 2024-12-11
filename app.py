from flask import Flask,render_template,request,redirect
from pymongo import MongoClient

app=Flask(__name__)
myclient=MongoClient("localhost",27017)
mydb=myclient["calci"]
results=mydb["results"]
isloggedin=False
credentials={"steeve@gmail.com":"steeve123","tony@gmail.com":"tony123"}

@app.route("/",methods=["GET","POST"])
def home():
    global isloggedin
    if request.method=="POST":
        mail=request.form["mail"]
        pwd=request.form["pwd"]
        if (mail in credentials) and (credentials[mail]==pwd):
            isloggedin=True
            return redirect("/calci")
        else:
            return redirect("/")
    else:
        return render_template("login.html")
@app.route("/calci",methods=["GET","POST"])
def calculator():
    if isloggedin==True:
        if request.method=="POST":
            n1=int(request.form["num1"])
            op=request.form["opr"]
            n2=int(request.form["num2"])
            if op=="add":
                res=f"{n1}+{n2} is {n1+n2}"
                results.insert_one({
                    "num1":n1,"operator":op,"num2":n2,"result":res
                })
                return render_template("index.html",output=res)
            elif op=="sub":
                res=f"{n1}-{n2} is {n1-n2}"
                results.insert_one({
                    "num1":n1,"operator":op,"num2":n2,"result":res
                })
                return render_template("index.html",output=res)
            elif op=="mul":
                res=f"{n1}x{n2} is {n1*n2}"
                results.insert_one({
                    "num1":n1,"operator":op,"num2":n2,"result":res
                })
                return render_template("index.html",output=res)
            elif op=="div":
                try: 
                    res=f"{n1}/{n2} is {n1/n2}"
                    results.insert_one({
                    "num1":n1,"operator":op,"num2":n2,"result":res
                    })
                    return render_template("index.html",output=res)
                except Exception as e:
                    return render_template("index.html",output="please change num2")
                    
        else:
            return render_template("index.html")
    else:
        return redirect("/")
app.run(debug=True)