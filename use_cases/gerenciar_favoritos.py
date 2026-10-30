class GerenciarFavoritos:
    """Casos de uso relacionados aos livros favoritos."""

    def __init__(self, repository):
        self.repository = repository

    def listar(self):
        return self.repository.listar_favoritos()

    def adicionar(self, titulo):
        return self.repository.adicionar_favorito(titulo)

    def remover(self, titulo):
        return self.repository.remover_favorito(titulo)