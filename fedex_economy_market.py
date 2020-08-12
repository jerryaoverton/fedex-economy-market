import requests
import os 
import json

from flask import Flask, render_template, request
app = Flask(__name__)

ctx = {'user_id':'',
       'drone_started': False,
       'next_action': None,
       'current_job': '',
       'max_total_jobs': 50,
       'max_consecutive_jobs': 3,
       'total_jobs': 0,
       'total_wait_cycles': 0,
       'max_wait_cycles': 50,
       'jobs_since_maintenance': 0,
       'current_battery_usage':0,
       'current_fexcoins':0,
       'max_weight':5}

smart_contract = os.environ['SMART_CONTRACT']
# smart_contract = 'https://fedex-economy-smartcontract.herokuapp.com/'
# smart_contract = 'http://127.0.0.1:5000/'
user_profile = {'' }

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/servicesoffer')
def servicesoffer():
    return render_template('services-offer.html')
   

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/wallet')
def wallet():
    user_id = request.args['user_id']
    svc = '/user_profile'
    params = '?user_id=' + user_id
    url = smart_contract + svc + params
    # Todo : redirect to register if no profile is there
    profile = requests.get(url).content

    svc = '/user_balance'
    params = '?user_id=' + user_id
    url = smart_contract + svc + params
    # Todo : redirect to register if no profile is there
    user_balance = requests.get(url).content

    return render_template('wallet.html',email=user_id, profile=json.loads(profile.decode('utf-8')), user_balance=user_balance.decode('utf-8'),sc=smart_contract)

@app.route('/signIn')
def signIn():
    return render_template('signIn.html')

@app.route('/signUp')
def signUp():
    return render_template('signUp.html')

@app.route('/dashboard')
def dashboard():
    user_id = request.args['user_id']
    ctx['user_id'] = user_id
    svc = '/user_profile'
    params = '?user_id=' + user_id
    url = smart_contract + svc + params
    # Todo : redirect to register if no profile is there
    profile = requests.get(url).content

    # get user_balance
    svc = '/user_balance'
    params = '?user_id=' + user_id
    url = smart_contract + svc + params
    # Todo : redirect to register if no profile is there
    user_balance = requests.get(url).content

    return render_template('dashboard.html', email=user_id, profile=json.loads(profile.decode('utf-8')), user_balance=user_balance.decode('utf-8'),sc=smart_contract)

@app.route('/logIn',  methods = ['POST'])
def logIn():
    user_id = request.form['username']
    svc = '/user_profile'
    params = '?user_id=' + user_id
    url = smart_contract + svc + params
    # Todo : redirect to register if no profile is there
    profile = requests.get(url).content

    # get user_balance
    svc = '/user_balance'
    params = '?user_id=' + user_id
    url = smart_contract + svc + params
    # Todo : redirect to register if no profile is there
    user_balance = requests.get(url).content

    return render_template('dashboard.html', email=user_id, profile=json.loads(profile.decode('utf-8')),user_balance=user_balance.decode('utf-8'),sc=smart_contract)

@app.route('/register',  methods = ['POST'])
def register():
    print(request)
    print(request.form)
    user_id = request.form['email']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    RegistrationType = request.form['RegistrationType']
    area_code = request.form['area_code']
    phone = request.form['phone']
    street = request.form['street']
    city = request.form['city']
    stateorprovince = request.form['stateorprovince']
    postalcode= request.form['postalcode']
    countrycode = request.form['countrycode']
    BusinessType = request.form.get('BusinessType', '')
    ServiceType = request.form.get('ServiceType', '')
    ServiceFee = request.form.get('ServiceFee','')

    

    profiledata = {"first_name":first_name,"last_name":last_name,"RegistrationType": RegistrationType,"area_code":area_code,"BusinessType":BusinessType,"street": street, "phone": phone , "city" :city , "stateorprovince" :stateorprovince , "postalcode" : postalcode , "countrycode" :countrycode,
                        "ServiceType":ServiceType, "ServiceFee": ServiceFee, "properties":"type:Quadcopter,capacity:2kgs,flyduration:10mins"}
    
    data = {"id":user_id,"token":0,"profile": profiledata}
    

    # register user with the smart contract
    svc = '/register_user'
    params = '?user_id=' + user_id
    url = smart_contract + svc + params
    _msg = requests.get(url).content

    user_send_payment('fedex',user_id,'100')
    # update profile
    print("profile")
    print(json.dumps(profiledata))

    svc = '/update_profile'
    params = '?user_id=' + user_id + "&profile="+ str(profiledata) 
    url = smart_contract + svc + params
    _status = requests.get(url).content
    print(_status)
    # req = requests.post(smart_contract + svc, json=data)

    return render_template('dashboard.html',email=user_id, profile=profiledata,sc=smart_contract)
    # return render_template('dashboard.html', email='s@s.com',first_name ='s' , last_name ='a')

@app.route('/profile')
def profile():
    user_id = request.args['user_id']
    #Todo: get user data from sc
    svc = '/user_profile'
    params = '?user_id=' + user_id
    url = smart_contract + svc + params
    # Todo : redirect to register if no profile is there
    profile = requests.get(url).content
    print('below profile')
    print((json.loads(profile.decode('utf-8'))))
    # profiledata = {"image_url":'https://via.placeholder.com/270x270' ,"first_name": 's', "last_name": 'a', "description": 'this is a text', "tag":'p , g' , "rating" :4 , "area_code":6 , "phone":67868698 ,"RegistrationType":'Individual' , "status":'Active' }
    # _msg = "The profile for " + user_id

    return render_template('profile.html', profile=json.loads(profile.decode('utf-8')), email = user_id, sc=smart_contract)


@app.route('/updateProfile')
def updateProfile():
    user_id = request.args['user_id']
    svc = '/user_profile'
    params = '?user_id=' + user_id
    url = smart_contract + svc + params
    # Todo : redirect to register if no profile is there
    profile = requests.get(url).content
    # profiledata = {"image_url":'https://via.placeholder.com/270x270' ,"first_name": 's', "last_name": 'a', "description": 'this is a text', "tag":'p , g' , "rating" :4 , "status":'Active' ,"area_code":6 , "phone":67868698}
    # _msg = "The profile for " + user_id

    return render_template('update_profile.html',email=user_id, profile=json.loads(profile.decode('utf-8')), sc=smart_contract)

@app.route('/myBusiness')
def myBusiness():
    _content = "Here is my business"
    user_id = request.args['user_id']
    svc = '/user_profile'
    params = '?user_id=' + user_id
    url = smart_contract + svc + params
    profile = requests.get(url).content

    svc = '/list_orders_by_supplier'
    params = '?supplier=' + user_id
    url = smart_contract + svc + params
    orders = requests.get(url).content
    print('orders', (orders.decode('utf-8')))
    print('orders eval', eval(orders.decode('utf-8')))

    return render_template('business_review_order.html', content=_content , orders =eval(orders.decode('utf-8')), email=user_id, sc=smart_contract,profile=json.loads(profile.decode('utf-8')))


@app.route('/dronedelivery', methods=["POST"])
def dronedelivery():
    print(request.form)
    order = eval(request.form['order'])
    print(order)
    user_id = order['customer']
    business_id = order['supplier']

    svc = '/user_profile'
    params = '?user_id=' + business_id
    url = smart_contract + svc + params
    business_profile = requests.get(url).content

    svc = '/user_profile'
    params = '?user_id=' + user_id
    url = smart_contract + svc + params
    user_profile = requests.get(url).content
    print(str(order))
    return render_template('droneOrder.html', order=(order), sc=smart_contract , email=business_id, business_id = user_id, price=8, user_profile=json.loads(user_profile.decode('utf-8')),business_profile=json.loads(business_profile.decode('utf-8')))

    


@app.route('/shop')
def shop():
    user_id = request.args['user_id']
    svc = '/user_profile'
    params = '?user_id=' + user_id
    url = smart_contract + svc + params
    profile = requests.get(url).content

    # get shops data
    svc = '/list_users'
    url = smart_contract + svc
    all_users = requests.get(url).content
   

    all_users_json = eval(all_users.decode('utf-8'))
    print('json print')
    # print(all_users_json)
    # print(json.loads(all_users_json))
    shops = []

    for user in all_users_json:
        for key,value in user.items():
            if key =='profile':
                try:
                    if value['RegistrationType'] == 'Business':
                        shops.append(user)
                except Exception:
                    continue

    # shops.append({"user_id": 'b@gmail.com', "profile":{"first_name":'ann b', "last_name":'pizza', "description":'i m a pizza shop'} })
    print(str(shops))    

    return render_template('shop.html', email=user_id, profile=json.loads(profile.decode('utf-8')), shops=shops, sc=smart_contract)

@app.route('/order' ,  methods = ['POST'])
def order():
    print(request.form)
    user_id = request.form['user_id']
    business_id = request.form['business_id']
    price = request.form['price']

    svc = '/user_profile'
    params = '?user_id=' + business_id
    url = smart_contract + svc + params
    business_profile = requests.get(url).content

    svc = '/user_profile'
    params = '?user_id=' + user_id
    url = smart_contract + svc + params
    user_profile = requests.get(url).content

    return render_template('order.html',sc=smart_contract , email=user_id, business_id = business_id, price=price, user_profile=json.loads(user_profile.decode('utf-8')),business_profile=json.loads(business_profile.decode('utf-8')))

@app.route('/pay')
def pay():
    _msg = "This is where you pay $$$"
    return render_template('pay.html', msg=_msg, sc=smart_contract)


@app.route('/update_order')
def update_order():
    _msg = "create or update your order here"
    return render_template('update_order.html', msg=_msg, sc=smart_contract)


@app.route('/review_orders')
def review_orders():
    _msg = "See updated orders here"
    return render_template('review_orders.html', msg=_msg, sc=smart_contract)


@app.route('/balance')
def balance():
    user_id = request.args['user_id']

    # get the user's balance from the smart contract
    svc = '/user_balance'
    params = '?user_id=' + user_id
    url = smart_contract + svc + params
    _balance = requests.get(url).content

    _msg = "The balance of " + user_id + " is " + str(_balance)
    return render_template('balance.html', msg=_msg)

def user_send_payment(sender,receiver,amount):
    print('sending payment')
    svc = '/pay'
    params = '?sender='+sender+'&receiver='+receiver+'&amount='+amount
    url = smart_contract + svc + params
    _msg = requests.get(url).content
    

if __name__ == '__main__':
    app.run(debug=True, port=5002)