from flask import (
    render_template,
    g,
    redirect,
    url_for
)

from src import app

@app.route("/")
def main():
    if g.user:
        return redirect(url_for('home.main'))
    return render_template('main.html')


if __name__ == '__main__':
    app.run()
