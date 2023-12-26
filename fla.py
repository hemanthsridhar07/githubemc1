from flask import Flask,redirect,url_for

app=Flask(__name__)
@app.route('/')
def home():
    return "hello world"

@app.route('/<name>')
def info(name):
    return f"im {name}"

@app.route('/admin')
def admin():
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)