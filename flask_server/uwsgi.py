from flask_server.application import create_app


app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0')
