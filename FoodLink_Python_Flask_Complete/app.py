from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import os, json, uuid

app = Flask(__name__)
app.secret_key = "foodlink-demo-secret"
UPLOAD_FOLDER = os.path.join("static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
DATA_FILE = "foodlink_data.json"

DEMO_USERS = [
    {"id":"u1","name":"Demo Donor","email":"donor@foodlink.demo","password":"donor123","role":"Donor"},
    {"id":"u2","name":"Helping Hands NGO","email":"ngo@foodlink.demo","password":"ngo123","role":"NGO"},
    {"id":"u3","name":"Demo Volunteer","email":"volunteer@foodlink.demo","password":"volunteer123","role":"Volunteer"},
    {"id":"u4","name":"FoodLink Admin","email":"admin@foodlink.demo","password":"admin123","role":"Admin"},
]

def seed():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE,"r",encoding="utf-8") as f: return json.load(f)
        except: pass
    now=datetime.now()
    donations=[
      {"id":"FL-1001","donor":"Green Leaf Restaurant","food":"Vegetable Biryani","category":"Cooked Meals","type":"Vegetarian","quantity":25,"unit":"kg","servings":100,"city":"Vijayawada","address":"MG Road, Vijayawada","status":"Available","expiry":(now+timedelta(hours=8)).isoformat(),"score":94},
      {"id":"FL-1002","donor":"Sunrise Bakery","food":"Fresh Bread & Buns","category":"Bakery","type":"Vegetarian","quantity":12,"unit":"kg","servings":70,"city":"Vijayawada","address":"Benz Circle, Vijayawada","status":"Available","expiry":(now+timedelta(hours=14)).isoformat(),"score":91},
      {"id":"FL-1003","donor":"City Caterers","food":"Rice & Dal","category":"Cooked Meals","type":"Vegetarian","quantity":35,"unit":"kg","servings":140,"city":"Guntur","address":"Lakshmipuram, Guntur","status":"Requested","expiry":(now+timedelta(hours=6)).isoformat(),"score":88},
      {"id":"FL-1004","donor":"FreshMart Supermarket","food":"Mixed Fruits","category":"Fruits","type":"Vegan","quantity":30,"unit":"kg","servings":120,"city":"Vijayawada","address":"Patamata, Vijayawada","status":"Available","expiry":(now+timedelta(days=1)).isoformat(),"score":86},
      {"id":"FL-1005","donor":"Hotel Grand Feast","food":"Chapati & Vegetable Curry","category":"Cooked Meals","type":"Vegetarian","quantity":18,"unit":"kg","servings":90,"city":"Hyderabad","address":"Banjara Hills, Hyderabad","status":"Accepted","expiry":(now+timedelta(hours=10)).isoformat(),"score":82},
      {"id":"FL-1006","donor":"Daily Dairy","food":"Milk Packets","category":"Dairy","type":"Vegetarian","quantity":20,"unit":"litre","servings":80,"city":"Vijayawada","address":"Auto Nagar, Vijayawada","status":"Available","expiry":(now+timedelta(hours=20)).isoformat(),"score":80},
      {"id":"FL-1007","donor":"Green Basket","food":"Fresh Vegetables","category":"Vegetables","type":"Vegan","quantity":45,"unit":"kg","servings":180,"city":"Guntur","address":"Arundelpet, Guntur","status":"Picked Up","expiry":(now+timedelta(days=1)).isoformat(),"score":77},
      {"id":"FL-1008","donor":"Campus Kitchen","food":"Curd Rice","category":"Cooked Meals","type":"Vegetarian","quantity":15,"unit":"kg","servings":60,"city":"Vijayawada","address":"University Road, Vijayawada","status":"Delivered","expiry":(now+timedelta(hours=4)).isoformat(),"score":75},
      {"id":"FL-1009","donor":"Care Cafe","food":"Veg Meals","category":"Cooked Meals","type":"Vegetarian","quantity":22,"unit":"kg","servings":88,"city":"Vijayawada","address":"Ramachandra Nagar, Vijayawada","status":"Available","expiry":(now+timedelta(hours=12)).isoformat(),"score":73},
      {"id":"FL-1010","donor":"Smart Grocers","food":"Packaged Snacks","category":"Packaged Food","type":"Vegetarian","quantity":10,"unit":"kg","servings":100,"city":"Hyderabad","address":"Kukatpally, Hyderabad","status":"Available","expiry":(now+timedelta(days=5)).isoformat(),"score":70}
    ]
    data={"donations":donations,"notifications":[
      {"text":"Your donation was accepted.","time":"Today"},
      {"text":"A volunteer has been assigned.","time":"Today"},
      {"text":"Your donation expires soon.","time":"Today"},
      {"text":"Food delivery completed.","time":"Yesterday"}],
      "ratings":[]}
    with open(DATA_FILE,"w",encoding="utf-8") as f: json.dump(data,f,indent=2)
    return data

def get_data(): return seed()
def save_data(d):
    with open(DATA_FILE,"w",encoding="utf-8") as f: json.dump(d,f,indent=2)

def current_user():
    email=session.get("email")
    return next((u for u in DEMO_USERS if u["email"]==email),None)

@app.context_processor
def common():
    d=get_data()
    available=sum(1 for x in d["donations"] if x["status"]=="Available")
    meals=sum(x.get("servings",0) for x in d["donations"] if x["status"] in ["Delivered","Picked Up","Accepted"])
    kg=sum(x.get("quantity",0) for x in d["donations"] if x["status"] in ["Delivered","Picked Up","Accepted"])
    return {"user":current_user(),"available_count":available,"meals":meals,"kg":kg,"notifications":d["notifications"]}

@app.route("/")
def home(): return render_template("home.html")
@app.route("/donate", methods=["GET","POST"])
def donate():
    if request.method=="POST":
        f=request.files.get("food_image")
        image=""
        if f and f.filename:
            name=secure_filename(f.filename)
            f.save(os.path.join(app.config["UPLOAD_FOLDER"],name))
            image=url_for("static",filename="uploads/"+name)
        try: qty=float(request.form.get("quantity",0))
        except: qty=0
        try: servings=int(request.form.get("servings",0))
        except: servings=0
        d=get_data()
        item={"id":"FL-"+str(uuid.uuid4())[:8].upper(),"donor":request.form.get("organization") or request.form.get("donor_name"),
        "food":request.form.get("food_name"),"category":request.form.get("category"),"type":request.form.get("food_type"),
        "quantity":qty,"unit":request.form.get("unit"),"servings":servings,"city":request.form.get("city"),
        "address":request.form.get("address"),"status":"Available","expiry":request.form.get("expiry") or (datetime.now()+timedelta(days=1)).isoformat(),"score":95,"image":image}
        d["donations"].insert(0,item); d["notifications"].insert(0,{"text":f"Donation {item['id']} was successfully listed.","time":"Just now"}); save_data(d)
        flash(f"Your donation has been successfully listed. Donation ID: {item['id']}","success")
        return redirect(url_for("dashboard"))
    return render_template("donate.html")

@app.route("/find")
def find():
    d=get_data(); q=request.args.get("q","").lower(); cat=request.args.get("category",""); typ=request.args.get("type",""); city=request.args.get("city","")
    rows=[x for x in d["donations"] if x["status"]=="Available"]
    if q: rows=[x for x in rows if q in (x["food"]+" "+x["donor"]+" "+x["city"]).lower()]
    if cat: rows=[x for x in rows if x["category"]==cat]
    if typ: rows=[x for x in rows if x["type"]==typ]
    if city: rows=[x for x in rows if x["city"]==city]
    rows.sort(key=lambda x:x.get("score",0),reverse=True)
    return render_template("find.html",donations=rows)

@app.route("/donation/<did>")
def details(did):
    item=next((x for x in get_data()["donations"] if x["id"]==did),None)
    if not item: return redirect(url_for("find"))
    return render_template("details.html",d=item)

@app.post("/request/<did>")
def request_donation(did):
    d=get_data()
    for x in d["donations"]:
        if x["id"]==did and x["status"]=="Available":
            x["status"]="Requested"; d["notifications"].insert(0,{"text":f"Donation {did} request submitted.","time":"Just now"}); break
    save_data(d); flash("Donation request submitted successfully.","success"); return redirect(url_for("find"))

@app.post("/status/<did>/<newstatus>")
def status(did,newstatus):
    allowed=["Available","Requested","Accepted","Picked Up","Delivered","Expired"]
    if newstatus not in allowed: return redirect(url_for("dashboard"))
    d=get_data()
    for x in d["donations"]:
        if x["id"]==did: x["status"]=newstatus; d["notifications"].insert(0,{"text":f"Donation {did} status changed to {newstatus}.","time":"Just now"}); break
    save_data(d); flash("Donation status updated.","success"); return redirect(url_for("dashboard"))

@app.route("/how-it-works")
def how(): return render_template("how.html")
@app.route("/impact")
def impact():
    d=get_data(); delivered=[x for x in d["donations"] if x["status"]=="Delivered"]
    return render_template("impact.html",donations=d["donations"],delivered=delivered)
@app.route("/about")
def about(): return render_template("about.html")

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        u=next((x for x in DEMO_USERS if x["email"].lower()==request.form["email"].lower() and x["password"]==request.form["password"]),None)
        if u: session["email"]=u["email"]; return redirect(url_for("dashboard"))
        flash("Invalid demo credentials.","error")
    return render_template("login.html")

@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="POST":
        session["email"]=request.form["email"]
        flash("Demo account created successfully.","success")
        return redirect(url_for("dashboard"))
    return render_template("register.html")

@app.route("/logout")
def logout(): session.clear(); return redirect(url_for("home"))

@app.route("/dashboard")
def dashboard():
    u=current_user()
    if not u: return redirect(url_for("login"))
    d=get_data()
    if u["role"]=="Donor": return render_template("donor_dashboard.html",donations=d["donations"])
    if u["role"]=="NGO": return render_template("ngo_dashboard.html",donations=d["donations"])
    if u["role"]=="Volunteer": return render_template("volunteer_dashboard.html",donations=d["donations"])
    return render_template("admin_dashboard.html",donations=d["donations"],users=DEMO_USERS)

@app.post("/rate")
def rate():
    d=get_data(); d["ratings"].append({"stars":int(request.form["stars"]),"comment":request.form.get("comment","")}); save_data(d)
    flash("Thank you for your feedback!","success"); return redirect(url_for("dashboard"))

@app.route("/api/stats")
def stats():
    d=get_data()
    delivered=[x for x in d["donations"] if x["status"]=="Delivered"]
    return jsonify({"donations":len(d["donations"]),"meals":sum(x["servings"] for x in delivered),
                    "food_saved":sum(x["quantity"] for x in delivered),"deliveries":len(delivered)})

if __name__=="__main__":
    seed()
    app.run(debug=True)
