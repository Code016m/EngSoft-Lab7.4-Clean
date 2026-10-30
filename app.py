from flask import Flask, render_template

from infrastructure.arquivo_txt_repository import ArquivoTxtRepository
from use_cases.listar_livros import ListarLivros
from use_cases.gerenciar_favoritos import GerenciarFavoritos
from use_cases.consultar_informacoes import ConsultarInformacoes
from controllers.livraria_controller import criar_livraria_controller


def create_app(repository=None):
    """Cria e configura a aplicação Flask."""
    app = Flask(__name__)

    # Infraestrutura
    if repository is None:
        repository = ArquivoTxtRepository()

    # Casos de uso
    listar_livros_uc = ListarLivros(repository)
    favoritos_uc = GerenciarFavoritos(repository)
    informacoes_uc = ConsultarInformacoes()

    # Controller
    livraria_bp = criar_livraria_controller(
        listar_livros_uc,
        favoritos_uc,
        informacoes_uc
    )

    app.register_blueprint(livraria_bp)

    @app.route("/")
    def pagina_inicial():
        return render_template("index.html")
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)