from waitress import serve
from hotrocks import create_app

if __name__ == "__main__":
    app = create_app()
    serve(app, listen="*:80")
