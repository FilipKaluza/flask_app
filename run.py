from mdblog.app import flask_app

if __name__ == "__main__":
    debug = False
    host = "0.0.0.0"
    flask_app.run(host, debug = True)