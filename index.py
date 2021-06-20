import time
from datetime import datetime, timezone
from flask import Flask, request, Response, jsonify, render_template

app = Flask(__name__)

accs = 1

accounts = [
    {'name': "Admin", 'mail': "lifechat.of@gmail.com", 'password': "Admin", 'id': 0},
    {'name': "Maxus", 'mail': "maximponomarenko627@gmail.com", 'password': "maxuspresents", 'id': 1}
]

messages = [
     
]
ids = 0
@app.route("/reg", methods=['POST'])
def register():
   name = request.json.get('name')
   text = request.json.get('text')
   password = request.json.get('word')
   id = request.json.get('id')
   if not (name and isinstance(name, str) and
         text and isinstance(text, str) and
         password and isinstance (password, str)):
       return Response(status=400)

   newacc = {'name': name, 'mail': text, 'password': password, 'id': id}
   accounts.append(newacc)
   global accs
   accs += 1
   return Response(status=200)

@app.route("/accounts")
#def debug():
#    return str(accounts)

def acc_view():
    after = float(request.args['after'])
    filtered = filter_by_key(messages, key='id', threshold=after)
    return {'accounts': filtered}

@app.route("/ids")
def give_ids():
    return str(accs)
def find_by_key(iterable, key, value):
    for index, dict_ in enumerate(iterable):
        if key in dict_ and dict_[key] == value:
            return [True, (index, dict_)]
        else:
            return "Bad"
def password_check(password, index):
    global accounts
    account = accounts[index]
    if password == account['password']:
        return jsonify(account['id'])
    else:
        return Response(status=400)

@app.route("/login", methods=['POST'])
def log_in():
    mail = request.json.get('name')
    word = request.json.get('text')
    if not (mail and isinstance(mail, str) and
            word and isinstance(word, str)):
        return Response(status=400)
    try:
        global accounts
        arg = find_by_key(accounts, 'mail', mail,)
        if arg[0] == True:
            password_check(word, arg[1])
        else:
            return Response(status=404)
    except Exception as e:
        print(e)
        return Response(status=500)

    
@app.route("/send", methods=['POST'])
def send():
    id = request.json.get('name')
    acc = accounts[id]
    name = acc['name']
    print(name)
    text = request.json.get('text')
    if not (name and isinstance(name, str) and
            text and isinstance(text, str)):
        return Response(status=400)

    message = {'name': name, 'time': time.time(), 'text': text}
    messages.append(message)
    return Response(status=200)


def filter_by_key(elements, key, threshold):
    filtered_elements = []

    for element in elements:
        if element[key] > threshold:
            filtered_elements.append(element)

    return filtered_elements


@app.route("/messages")
def messages_view():
    try:
        after = float(request.args['after'])
    except:
        return Response(status=400)

    filtered = filter_by_key(messages, key='time', threshold=after)
    return {'messages': filtered}


@app.route("/")
def hello(name=None):
    return render_template('index.html')
#def hello():
    #return " Привет, ты на главной странице LC! <a href='/status'>Статус</a>"


@app.route("/status")
def status():
    return {
        'status': True,
        'name': 'LC',
        'time': time.time(),
        'time1': time.asctime(),
        'time2': datetime.now(),
        'time3': datetime.now().isoformat(),
        'time4': datetime.now(tz=timezone.utc).isoformat(),
        'time5': datetime.now().strftime('%H:%M:%S %Y/%m/%d !'),
    }


app.run()