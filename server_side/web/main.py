from bottle import *

front_end_path = '../../front_end/'

cookie_visited = "visited"


@route('/static/:filename#.*#')
def server_static(filename):
    print(filename)
    return static_file(filename, root=front_end_path)


@route('/auth')
def auth():
    if request.get_cookie(cookie_visited) == "True":
        redirect('/')
    else:
        return static_file('signin.html', root=front_end_path)


def check_login(username, password):
    return True if username == "admin" and password == 'admin' else False


@post('/auth')
def post_login():
    username = request.forms.get('login')
    password = request.forms.get('password')
    if check_login(username, password):
        response.set_cookie(cookie_visited, "True")
        return redirect('/')
    else:
        return redirect('/auth')


@route('/')
@route('/index')
def base():
    print("QUERY")
    for item in request.query:
        print(item)
    if request.get_cookie(cookie_visited):
        # response.delete_cookie(cookie_visited)
        return template('dashboard.html')
    else:
        wrong_auth()


def wrong_auth():
    redirect('/auth')


#####
json_response = {"req": [['a'], ['b'], ['c']]}


@route('/test')
def jsontest():
    return template('ajax_test')


@post('/getallitems.json')
def shop_aj_getallitems():
    req = prepare_request(request.query)
    print(req)
    return parse_request(req)


def parse_request(request_dict=None):
    if not request_dict:
        request_dict = {}
    try:
        if request_dict.get('fromname', None):
            return table_request(request_dict)
        elif request_dict.get('code', None):
            return console_request(request_dict)
        else:
            return message_request(request_dict, 'Wrong request')
    except Exception as ex:
        return message_request(request_dict, str(ex))


def table_request(request_dict=None):
    if not request_dict:
        request_dict = {}
    table_operation = request_dict.get('fromname').split('_')
    table_name = table_operation[0]
    operation_name = table_operation[1]


def console_request(request_dict=None):
    if not request_dict:
        request_dict = {}
    return {}


def message_request(request_string, message):
    return {'message': message}


def prepare_request(request_dict=None):
    if not request_dict:
        request_dict = {}
    new_dict = {}
    for key, item in request_dict:
        new_dict[key.lower()] = item.lower()
        try:
            value = int(item)
            request_dict[key] = value
        except ValueError:
            pass
    return request_dict


#####

if __name__ == '__main__':
    TEMPLATE_PATH.append(front_end_path)
    run(host='localhost', port=8080, debug=True)
