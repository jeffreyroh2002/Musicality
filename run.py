from WebApp import create_app, db

app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
