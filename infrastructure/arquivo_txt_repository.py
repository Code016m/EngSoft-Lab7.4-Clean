import json
from pathlib import Path

from entities.livro import Livro
from interfaces.livro_repository import LivroRepository


class ArquivoTxtRepository(LivroRepository):
    """Implementa o armazenamento de livros em arquivo TXT."""

    def __init__(self, caminho=None):
        if caminho is None:
            caminho = (
                Path(__file__).resolve().parent.parent
                / "data"
                / "livros.txt"
            )

        self.caminho = Path(caminho)
        self.caminho.parent.mkdir(parents=True, exist_ok=True)

        if not self.caminho.exists():
            self._salvar_dados({
                "livros": [],
                "favoritos": [],
                "horario": "Não informado.",
                "localizacao": "Não informada."
            })

    def _ler_dados(self):
        with open(self.caminho, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)

    def _salvar_dados(self, dados):
        with open(self.caminho, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=4)

    def listar_livros(self):
        dados = self._ler_dados()

        return [
            Livro.from_dict(livro)
            for livro in dados["livros"]
        ]

    def buscar_livro(self, titulo):
        titulo = titulo.strip().casefold()

        for livro in self.listar_livros():
            if livro.titulo.casefold() == titulo:
                return livro

        return None

    def salvar_livros(self, livros):
        dados = self._ler_dados()
        dados["livros"] = [
            livro.to_dict() for livro in livros
        ]
        self._salvar_dados(dados)

    def listar_favoritos(self):
        dados = self._ler_dados()
        favoritos = dados["favoritos"]

        return [
            Livro.from_dict(livro)
            for livro in dados["livros"]
            if livro["titulo"] in favoritos
        ]

    def adicionar_favorito(self, titulo):
        livro = self.buscar_livro(titulo)

        if livro is None:
            return False

        dados = self._ler_dados()

        if livro.titulo not in dados["favoritos"]:
            dados["favoritos"].append(livro.titulo)
            self._salvar_dados(dados)

        return True

    def remover_favorito(self, titulo):
        livro = self.buscar_livro(titulo)

        if livro is None:
            return False

        dados = self._ler_dados()

        if livro.titulo not in dados["favoritos"]:
            return False

        dados["favoritos"].remove(livro.titulo)
        self._salvar_dados(dados)

        return True

    def obter_horario(self):
        dados = self._ler_dados()
        return dados.get("horario", "Não informado.")

    def obter_localizacao(self):
        dados = self._ler_dados()
        return dados.get("localizacao", "Não informada.")
