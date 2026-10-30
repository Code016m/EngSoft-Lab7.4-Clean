"""Camada de negócio da aplicação."""

from repositories import livraria_repository as repository

def listar_livros():
    """Retorna todos os livros disponíveis no catálogo."""
    return repository.listar_livros()

def pesquisar_livros(termo):
    """Pesquisa livros por título ou autor."""
    return repository.buscar_livros(termo)

def consultar_livro(titulo):
    """Consulta um livro pelo título exato."""
    return repository.buscar_livro_exato(titulo)

def consultar_disponibilidade(titulo):
    """Verifica se um livro existe e está disponível."""
    livro = consultar_livro(titulo)

    if livro is None:
        return None

    return livro["disponivel"]

def consultar_disponibilidade_loja(titulo, loja):
    """Verifica se um livro está disponível em determinada loja."""
    livro = consultar_livro(titulo)

    if livro is None:
        return None

    return loja.casefold() in [
        nome.casefold() for nome in livro["lojas"]
    ]

def consultar_preco(titulo):
    """Consulta o preço de um livro."""
    livro = consultar_livro(titulo)

    if livro is None:
        return None

    return livro["preco"]

def consultar_horario():
    """Consulta o horário de funcionamento."""
    return repository.obter_horario()

def consultar_localizacao():
    """Consulta a localização da livraria."""
    return repository.obter_localizacao()

def recomendar_livros(termo=""):
    """Recomenda livros com base em um termo de pesquisa."""
    livros = pesquisar_livros(termo)

    if not livros:
        return []

    return sorted(
        livros,
        key=lambda livro: (
            not livro["disponivel"],
            livro["titulo"]
        )
    )

def listar_favoritos():
    """Retorna os livros favoritos."""
    return repository.listar_favoritos()

def adicionar_favorito(titulo):
    """Adiciona um livro aos favoritos."""
    return repository.adicionar_favorito(titulo)

def remover_favorito(titulo):
    """Remove um livro dos favoritos."""
    return repository.remover_favorito(titulo)
