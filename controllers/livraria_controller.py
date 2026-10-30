from flask import Blueprint, jsonify, request

def criar_livraria_controller(
    listar_livros_uc,
    favoritos_uc,
    informacoes_uc
):
    """Cria as rotas da livraria utilizando os casos de uso."""
    livraria_bp = Blueprint("livraria", __name__)

    @livraria_bp.route("/api/livros", methods=["GET"])
    def listar_livros():
        termo = request.args.get("q", "")
        livros = listar_livros_uc.pesquisar(termo)
        return jsonify([livro.to_dict() for livro in livros])

    @livraria_bp.route("/api/livros/<path:titulo>", methods=["GET"])
    def consultar_livro(titulo):
        livro = listar_livros_uc.consultar(titulo)
        if livro is None:
            return jsonify({"erro": "Livro não encontrado"}), 404
        return jsonify(livro.to_dict())

    @livraria_bp.route(
        "/api/livros/<path:titulo>/disponibilidade",
        methods=["GET"]
    )
    def consultar_disponibilidade(titulo):
        disponibilidade = listar_livros_uc.consultar_disponibilidade(
            titulo
        )
        if disponibilidade is None:
            return jsonify({"erro": "Livro não encontrado"}), 404
        return jsonify({"disponivel": disponibilidade})

    @livraria_bp.route("/api/horario", methods=["GET"])
    def consultar_horario():
        return jsonify({
            "horario": informacoes_uc.consultar_horario()
        })

    @livraria_bp.route("/api/localizacao", methods=["GET"])
    def consultar_localizacao():
        return jsonify({
            "localizacao": informacoes_uc.consultar_localizacao()
        })

    @livraria_bp.route("/api/recomendacoes", methods=["GET"])
    def recomendar_livros():
        termo = request.args.get("q", "")
        livros = listar_livros_uc.recomendar(termo)
        return jsonify([livro.to_dict() for livro in livros])

    @livraria_bp.route("/api/favoritos", methods=["GET"])
    def listar_favoritos():
        livros = favoritos_uc.listar()
        return jsonify([livro.to_dict() for livro in livros])

    @livraria_bp.route("/api/favoritos", methods=["POST"])
    def adicionar_favorito():
        dados = request.get_json(silent=True) or {}
        titulo = dados.get("titulo", "")
        if not favoritos_uc.adicionar(titulo):
            return jsonify({"erro": "Livro não encontrado"}), 404
        return jsonify({
            "mensagem": "Livro adicionado aos favoritos"
        }), 201

    @livraria_bp.route(
        "/api/favoritos/<path:titulo>",
        methods=["DELETE"]
    )
    def remover_favorito(titulo):
        if not favoritos_uc.remover(titulo):
            return jsonify({
                "erro": "Livro não encontrado nos favoritos"
            }), 404
        return jsonify({
            "mensagem": "Livro removido dos favoritos"
        })

    return livraria_bp
