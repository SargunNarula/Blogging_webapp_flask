from backend_code import create_app

app = create_app()

#To run this automatically in Debug mode
if __name__ == "__main__":
    app.run(debug=True)

