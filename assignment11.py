from flask import Flask, render_template, request, session
from markupsafe import escape

app=Flask(__name__)

app.secret_key = b'\x7f\x92?\xddk*=\xfc\xc4\x02\xa3&\xee\x1f\x1b\xe1'

@app.route('/')
@app.route('/assignment11.html', methods=['GET', 'POST'])
def landing_page():
    method = request.method
    username = None
    password = None
    fname = None
    lname = None

    # First Visit / No Cookies
    if method == 'GET' and len(request.args) == 0 and len(session) == 0:
        return render_template('assignment11.html')
    
    # Logout request
    elif method == 'GET' and 'logout' in request.args:
        print("Logged out")
        session.clear()
        return render_template('assignment11.html')    
    
    # Login Request
    elif method == 'GET' and 'login' in request.args:
        username = request.args.get('username')
        password = request.args.get('password')        
        
        # Load login information
        f = open("assignment11-account-info.txt", "r+")
        file = f.read(-1)
        file = file.replace("\n", "")
        user_data = file.split(";")
        f.close()
        
        # Search for user
        # Mem-efficient array search for usernames
        for i in range(0, len(user_data), 7):
            if user_data[i] == username and user_data[i + 1] == password:
                # Bake cookies
                # User info == user_data[user_num + data index]
                session['username'] = user_data[i + 0]
                session['fname'] = user_data[i + 2]
                session['lname'] = user_data[i + 3]
                session['title'] = user_data[i + 4]
                session['bkcolor'] = user_data[i + 5]
                session['imgurl'] = user_data[i + 6]
                
                # Serve the Homepage
                return render_template('userhome.html',
                                       username=session['username'],
                                       fname=session['fname'],
                                       lname=session['lname'],
                                       title=session['title'],
                                       bkcolor=session['bkcolor'],
                                       imgurl=session['imgurl']
                )
            elif user_data[i] == username and user_data[i + 1] != password:
                return render_template('assignment11.html', invalid='invalid', username=username)
        return render_template('assignment11.html', nouser='no_user', username=username)
    
    # Sign Up Request
    elif method == 'GET' and 'signup' in request.args:
        username = request.args.get('username')
        password = request.args.get('password')
        fname = request.args.get('fname')
        lname = request.args.get('lname')
        
        # Make sure user is uniqe
        # Load login information
        f = open("assignment11-account-info.txt", "r+")
        file = f.read(-1)
        file = file.replace("\n", "")
        user_data = file.split(";")
        f.close()
        
        # Find matching user
        # Mem-efficient array search for usernames
        for i in range(0, len(user_data), 7):
            if user_data[i] == username:
                return render_template('assignment11.html', nonuniqe='non_uniqe', username=username)
        
        # Append to file
        f = open("assignment11-account-info.txt", "a+")
        f.write(username + ";")
        f.write(password + ";")
        f.write(fname + ";")
        f.write(lname + ";")
        f.write("Welcome to Robert Bell's Assignment 11 web site!" + ";")
        f.write("white" + ";")
        f.write("https://upload.wikimedia.org/wikipedia/commons/thumb/9/94/Stick_Figure.svg/1200px-Stick_Figure.svg.png" + ";" + "\n")
        f.close()
        
        # Create Cookies
        session['username'] = username
        session['fname'] = fname
        session['lname'] = lname
        session['title'] = "Welcome to Robert Bell's Assignment 11 web site!"
        session['bkcolor'] = 'white'
        session['imgurl'] = "https://upload.wikimedia.org/wikipedia/commons/thumb/9/94/Stick_Figure.svg/1200px-Stick_Figure.svg.png"
        
        # Serve the Homepage
        return render_template('userhome.html',
                               username=session['username'],
                               fname=session['fname'],
                               lname=session['lname'],
                               title=session['title'],
                               bkcolor=session['bkcolor'],
                               imgurl=session['imgurl']
        )
    
    # Edit request
    elif method == 'GET' and 'update' in request.args:
        fname = request.args.get('fname')
        lname = request.args.get('lname')
        title = request.args.get('title')
        bkcolor = request.args.get('bkcolor')
        imgurl = request.args.get('imgurl')
        
        # Load login information
        f = open("assignment11-account-info.txt", "r+")
        file = f.read(-1)
        f.close()
        
        # Replace bad data
        usr_info = None
        lines = file.splitlines(True)
        for i in range(0, len(lines)):
            if session['username'] in lines[i]:
                usr_info = lines.pop(i)
                
                usr_info = usr_info.replace(session['fname'], fname, 1)
                usr_info = usr_info.replace(session['lname'], lname, 1)
                usr_info = usr_info.replace(session['title'], title, 1)
                usr_info = usr_info.replace(session['bkcolor'], bkcolor, 1)
                usr_info = usr_info.replace(session['imgurl'], imgurl, 1)
                
                lines.insert(i, usr_info)
                break
        
        file = ''.join(lines)
        
        # Rewrite good data
        f = open("assignment11-account-info.txt", "w+")
        f.write(file)
        f.close()
        
        # Create Cookies
        session['fname'] = fname
        session['lname'] = lname
        session['title'] = title
        session['bkcolor'] = bkcolor
        session['imgurl'] = imgurl
        
        # Serve the Homepage
        return render_template('userhome.html',
                               username=session['username'],
                               fname=session['fname'],
                               lname=session['lname'],
                               title=session['title'],
                               bkcolor=session['bkcolor'],
                               imgurl=session['imgurl']
        )        
        
    # Current session login
    elif method == 'GET' and 'username' in session:
        # Serve the Homepage
        return render_template('userhome.html',
                               username=session['username'],
                               fname=session['fname'],
                               lname=session['lname'],
                               title=session['title'],
                               bkcolor=session['bkcolor'],
                               imgurl=session['imgurl']
        )
    