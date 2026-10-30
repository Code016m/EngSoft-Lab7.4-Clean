class ListarLivros:
    """Casos de uso relacionados à consulta de livros."""

    def __init__(self, repository):
        self.repository = repository

    def executar(self):
        return self.repository.listar_livros()

    def pesquisar(self, termo=""):
        livros = self.repository.listar_livros()

        if not termo:
            return livros

        termo = termo.casefold()

        return [
            livro for livro in livros
            if termo in livro.titulo.casefold()
            or termo in livro.autor.casefold()
        ]

    def consultar(self, titulo):
        return self.repository.buscar_livro(titulo)

    def consultar_disponibilidade(self, titulo):
        livro = self.consultar(titulo)

        if livro is None:
            return None

        return livro.disponivel

    def consultar_disponibilidade_loja(self, titulo, loja):
        livro = self.consultar(titulo)

        if livro is None:
            return None

        return loja.casefold() in [
            nome.casefold() for nome in livro.lojas
        ]

    def consultar_preco(self, titulo):
        livro = self.consultar(titulo)

        if livro is None:
            return None

        return livro.preco

    def recomendar(self, termo=""):
        livros = self.pesquisar(termo)

        return sorted(
            livros,
            key=lambda livro: (
                not livro.disponivel,
                livro.titulo
            )
        )