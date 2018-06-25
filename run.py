from app import create_app

if __name__ == '__main__':
    print("This works")
    app = create_app()
    app.run()