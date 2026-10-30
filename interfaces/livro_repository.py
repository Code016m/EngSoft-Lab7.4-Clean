from abc import ABC, abstractmethod

class LivroRepository(ABC):

    @abstractmethod
    def listar_livros(self):
        pass

    @abstractmethod
    def buscar_livro(self, titulo):
        pass

    @abstractmethod
    def salvar_livros(self, livros):
        pass

    @abstractmethod
    def listar_favoritos(self):
        pass

    @abstractmethod
    def adicionar_favorito(self, titulo):
        pass

    @abstractmethod
    def remover_favorito(self, titulo):
        pass

    @abstractmethod
    def obter_horario(self):
        pass

    @abstractmethod
    def obter_localizacao(self):
        pass