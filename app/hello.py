from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup_post():
    print(dir(request))    
    email = request.form.get('email')
    print(email)
    name = request.form.get('name')
    print(name)
    password = request.form.get('password')
    print(password)
    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)
