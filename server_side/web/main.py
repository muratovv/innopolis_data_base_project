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
items = {'req': [('id', 'title', 'year', 'venue'), (42, 'Overview of the Iris DBMS.', 1989, 'Modern Database Systems'),
                 (43, 'Features of the ORION Object-Oriented Database System.', 1989,
                  'Object-Oriented Concepts, Databases, and Applications'),
                 (44, 'Indexing Techniques for Object-Oriented Databases.', 1989, 'The INGRES Papers'),
                 (45, 'My Cat Is Object-Oriented.', 1989, 'Temporal Databases'),
                 (46, 'Making Database Systems Fast Enough for CAD Applications.', 1989, 'Reihe Informatik'),
                 (47, 'Optimizing Smalltalk Message Performance.', 1989, 'The Compiler Design Handbook'), (
                     48, 'The Common List Object-Oriented Programming Language Standard.', 1989,
                     'The Industrial Information Technology Handbook'), (
                     49, 'Object Orientation as Catalyst for Language-Database Inegration.', 1989,
                     'The Computer Science and Engineering Handbook'),
                 (50, 'A Survey of Object-Oriented Concepts.', 1989, 'CSLI Lecture Notes'),
                 (51, 'Integrated Office Systems.', 1989, 'On the Construction of Programs'), (
                     52, 'Proteus: A Frame-Based Nonmonotonic Inference System.', 1989,
                     'Cambridge Tracts in Theoretical Computer Science'), (
                     53, 'Concurrency Control and Object-Oriented Databases.', 1989,
                     'Web Engineering: Systematische Entwicklung von Web-Anwendungen'),
                 (54, 'A Shared View of Sharing: The Treaty of Orlando.', 1989, 'Web & Datenbanken'),
                 (55, 'Pogo: A Declarative Representation System for Graphics.', 1989, 'Implementations of Prolog'),
                 (56, 'Concurrent Object-Oriented Programming Languages.', 1989, 'Prolog and Databases'),
                 (57, 'Directions in Object-Oriented Research.', 1989, 'Handbook of Automated Reasoning'), (
                     58, 'A Proposal for a Formal Model of Objects.', 1989,
                     'Computer-Aided Database Design: the DATAID approach'), (
                     59, 'OZ+: An Object-Oriented Database System.', 1989,
                     'Logic Programming: Formal Methods and Practical Applications'),
                 (60, 'The Commercial INGRES Epilogue.', 1986, 'Methodology and Tools for Data Base Design'), (
                     61, 'Design of Relational Systems (Introduction to Section 1).', 1986,
                     'Handbook of Theoretical Computer Science, Volume A: Algorithms and Complexity (A)')]}

@route('/test')
def jsontest():
    return template('ajax_test')


@post('/getallitems.json')
def shop_aj_getallitems():
    for item in request.query:
        print(item, request.query[item])
    return items


#####

if __name__ == '__main__':
    TEMPLATE_PATH.append(front_end_path)
    run(host='localhost', port=8081, debug=True)
