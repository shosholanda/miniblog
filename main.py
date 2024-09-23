from src import app
# refresh the frontend
# from livereload import Server 
from flask import (
    render_template,
    g,
    redirect,
    url_for
)

@app.route("/help")
def help():
    return render_template('blog/help.html')

@app.route("/")
def main():
    if g.user:
        return redirect(url_for('home.main'))
    return render_template('main.html')

if __name__ == '__main__':
    # app.debug = True
    # server = Server(app.wsgi_app)
    # server.serve(port=5000)
    app.run(debug = True)
