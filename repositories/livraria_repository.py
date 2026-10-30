"""Camada de acesso aos dados da livraria."""

LIVROS = [
    {
        "titulo": "Dom Casmurro",
        "autor": "Machado de Assis",
        "preco": 30.0,
        "disponivel": True,
        "lojas": ["Loja Centro"],
    },
    {
        "titulo": "O Cortiço",
        "autor": "Aluísio Azevedo",
        "preco": 35.0,
        "disponivel": True,
        "lojas": ["Loja Centro"],
    },
    {
        "titulo": "Memórias Póstumas de Brás Cubas",
        "autor": "Machado de Assis",
        "preco": 32.0,
        "disponivel": True,
        "lojas": ["Loja Centro"],
    },
    {
        "titulo": "Grande Sertão: Veredas",
        "autor": "João Guimarães Rosa",
        "preco": 45.0,
        "disponivel": True,
        "lojas": ["Loja Centro"],
    },
    {
        "titulo": "Capitães da Areia",
        "autor": "Jorge Amado",
        "preco": 38.0,
        "disponivel": True,
        "lojas": ["Loja Centro"],
    },
    {
        "titulo": "A Hora da Estrela",
        "autor": "Clarice Lispector",
        "preco": 28.0,
        "disponivel": True,
        "lojas": ["Loja Centro"],
    },
    {
        "titulo": "Vidas Secas",
        "autor": "Graciliano Ramos",
        "preco": 34.0,
        "disponivel": False,
        "lojas": [],
    },
]

HORARIO_FUNCIONAMENTO = "Não informado."
LOCALIZACAO = "Não informada."

# Armazenamento temporário dos favoritos.
FAVORITOS = []


def listar_livros():
    """Retorna todos os livros cadastrados."""
    return [livro.copy() for livro in LIVROS]


def buscar_livros(termo):
    """Busca livros por título ou autor."""
    termo = termo.casefold().strip()

    if not termo:
        return listar_livros()

    return [
        livro.copy()
        for livro in LIVROS
        if termo in livro["titulo"].casefold()
        or termo in livro["autor"].casefold()
    ]


def buscar_livro_exato(titulo):
    """Busca um livro pelo título exato."""
    titulo = titulo.strip().casefold()

    return next(
        (
            livro.copy()
            for livro in LIVROS
            if livro["titulo"].casefold() == titulo
        ),
        None
    )


def obter_horario():
    """Retorna o horário de funcionamento da livraria."""
    return HORARIO_FUNCIONAMENTO


def obter_localizacao():
    """Retorna a localização da livraria."""
    return LOCALIZACAO


def listar_favoritos():
    """Retorna os livros marcados como favoritos."""
    return [
        livro.copy()
        for livro in LIVROS
        if livro["titulo"] in FAVORITOS
    ]


def adicionar_favorito(titulo):
    """Adiciona um livro aos favoritos se ele existir."""
    livro = buscar_livro_exato(titulo)

    if livro is None:
        return False

    if livro["titulo"] not in FAVORITOS:
        FAVORITOS.append(livro["titulo"])

    return True


def remover_favorito(titulo):
    """Remove um livro da lista de favoritos."""
    livro = buscar_livro_exato(titulo)

    if livro is None or livro["titulo"] not in FAVORITOS:
        return False

    FAVORITOS.remove(livro["titulo"])
    return True
