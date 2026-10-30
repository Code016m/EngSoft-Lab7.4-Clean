"""Camada de aplicação responsável pelas rotas da livraria."""

from flask import Blueprint, jsonify, request
from services import livraria_service as service

livraria_bp = Blueprint("livraria", __name__)

@livraria_bp.route("/api/livros", methods=["GET"])
def listar_livros():
    """Lista todos os livros ou pesquisa por título e autor."""
    termo = request.args.get("q", "")
    livros = service.pesquisar_livros(termo)
    return jsonify(livros)

@livraria_bp.route("/api/livros/<path:titulo>", methods=["GET"])
def consultar_livro(titulo):
    """Consulta os dados de um livro."""
    livro = service.consultar_livro(titulo)

    if livro is None:
        return jsonify({"erro": "Livro não encontrado"}), 404
    return jsonify(livro)

@livraria_bp.route(
    "/api/livros/<path:titulo>/disponibilidade",
    methods=["GET"]
)
def consultar_disponibilidade(titulo):
    """Consulta a disponibilidade de um livro."""
    disponibilidade = service.consultar_disponibilidade(titulo)

    if disponibilidade is None:
        return jsonify({"erro": "Livro não encontrado"}), 404
    return jsonify({"disponivel": disponibilidade})

@livraria_bp.route("/api/horario", methods=["GET"])
def consultar_horario():
    """Retorna o horário da livraria."""
    return jsonify({"horario": service.consultar_horario()})

@livraria_bp.route("/api/localizacao", methods=["GET"])
def consultar_localizacao():
    """Retorna a localização da livraria."""
    return jsonify({"localizacao": service.consultar_localizacao()})

@livraria_bp.route("/api/recomendacoes", methods=["GET"])
def recomendar_livros():
    """Retorna recomendações de livros."""
    termo = request.args.get("q", "")
    return jsonify(service.recomendar_livros(termo))

@livraria_bp.route("/api/favoritos", methods=["GET"])
def listar_favoritos():
    """Lista os livros favoritos."""
    return jsonify(service.listar_favoritos())

@livraria_bp.route("/api/favoritos", methods=["POST"])
def adicionar_favorito():
    """Adiciona um livro aos favoritos."""
    dados = request.get_json(silent=True) or {}
    titulo = dados.get("titulo", "")

    if not service.adicionar_favorito(titulo):
        return jsonify({"erro": "Livro não encontrado"}), 404
    return jsonify({"mensagem": "Livro adicionado aos favoritos"}), 201

@livraria_bp.route(
    "/api/favoritos/<path:titulo>",
    methods=["DELETE"]
)
def remover_favorito(titulo):
    """Remove um livro dos favoritos."""
    if not service.remover_favorito(titulo):
        return jsonify({
            "erro": "Livro não encontrado nos favoritos"
        }), 404
    return jsonify({"mensagem": "Livro removido dos favoritos"})
