import requests
import os 
import json

from flask import Flask, render_template, request
app = Flask(__name__)

# smart_contract = os.environ['SMART_CONTRACT']
smart_contract = 'https://fedex-economy-smartcontract.herokuapp.com/'

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
    servicesoffer

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/wallet')
def wallet():
    return render_template('wallet.html')

@app.route('/signIn')
def signIn():
    return render_template('signIn.html')

@app.route('/signUp')
def signUp():
    return render_template('signUp.html')

@app.route('/dashboard')
def dashboard():
    # fetch userdata
    return render_template('dashboard.html', email='s@s.com')

@app.route('/myBusiness')
def myBusiness():
    _content = "Here is some stuff you can buy"
    return render_template('myBusiness.html', content=_content , sc=smart_contract)

@app.route('/logIn',  methods = ['POST'])
def logIn():
    user_id = request.form['username']
    svc = '/user_profile'
    params = '?user_id=' + user_id
    url = smart_contract + svc + params
    # Todo : redirect to register if no profile is there
    profile = requests.get(url).content
    return render_template('dashboard.html', email=user_id, profile=profile)

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
    BusinessType = request.form.get('BusinessType', None)
    AddressLine1 = request.form['AddressLine1']
    AddressLine2 = request.form['AddressLine2']
    profiledata = {"first_name":first_name,"last_name":last_name,"RegistrationType": RegistrationType,
                        "area_code":area_code,"BusinessType":BusinessType,"BusinessAddress": AddressLine1 + " " + AddressLine2,}
    data = {"id":user_id,"token":0,"profile": profiledata}
    
    print(data)

    # register user with the smart contract
    svc = '/register_user'
    params = '?user_id=' + user_id
    url = smart_contract + svc + params
    _msg = requests.get(url).content
    # req = requests.post(smart_contract + svc, json=data)

    return render_template('dashboard.html',email=user_id, profile=profiledata)
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
    print((profile.decode('utf-8')))
    profiledata = {"image_url":'https://via.placeholder.com/270x270' ,"first_name": 's', "last_name": 'a', "description": 'this is a text', "tag":'p , g' , "rating" :4 , "area_code":6 , "phone":67868698 ,"RegistrationType":'Individual' , "status":'Active' }
    # _msg = "The profile for " + user_id

    return render_template('profile.html', profile=profiledata, email = user_id, sc=smart_contract)


@app.route('/updateProfile')
def updateProfile():
    user_id = request.args['user_id']
    svc = '/user_profile'
    params = '?user_id=' + user_id
    url = smart_contract + svc + params
    # Todo : redirect to register if no profile is there
    profile = requests.get(url).content
    profiledata = {"image_url":'https://via.placeholder.com/270x270' ,"first_name": 's', "last_name": 'a', "description": 'this is a text', "tag":'p , g' , "rating" :4 , "status":'Active' ,"area_code":6 , "phone":67868698}
    # _msg = "The profile for " + user_id

    return render_template('update_profile.html',email=user_id, profile=profiledata, sc=smart_contract)


@app.route('/shop')
def shop():
    _content = "Here is some stuff you can buy"
    return render_template('shop.html', content=_content , sc=smart_contract)


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



if __name__ == '__main__':
    app.run(debug=True, port=1000)