from bottle import *

cookie_visited = "visited"


@route('/auth')
def auth():
    if request.get_cookie(cookie_visited) == "True":
        redirect('/')
    else:
        return '''
        <form action="/auth" method="post">
            Username: <input name="username" type="text" />
            Password: <input name="password" type="password" />
            <input value="auth" type="submit" />
        </form>
    '''


def check_login(username, password):
    return True if username == "admin" and password == 'admin' else False


@post('/auth')
def post_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
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
        return "OK"
    else:
        wrong_auth()


def wrong_auth():
    redirect('/auth')


run(host='localhost', port=8080, debug=True)
