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
    print(username, password)
    if check_login(username, password):
        response.set_cookie(cookie_visited, "True")
        return redirect('/')
    else:
        return redirect('/auth')


@route('/')
@route('/index')
def base():
    if request.get_cookie(cookie_visited):
        response.delete_cookie(cookie_visited)
        return template('dashboard.html')
    else:
        wrong_auth()


def wrong_auth():
    redirect('/auth')


if __name__ == '__main__':
    TEMPLATE_PATH.append(front_end_path)
    run(host='localhost', port=8080, debug=True)
