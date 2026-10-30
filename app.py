"""Aplicação principal da livraria no padrão MVC."""

from flask import Flask, render_template
from controllers.livraria_controller import livraria_bp

def create_app():
    """Cria e configura a aplicação Flask."""
    app = Flask(__name__)
    app.register_blueprint(livraria_bp)

    @app.get("/")
    def pagina_inicial():
        return render_template("index.html")
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
