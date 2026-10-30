from dataclasses import dataclass, field

@dataclass
class Livro:
    """Representa um livro do catálogo da livraria."""
    titulo: str
    autor: str
    preco: float
    disponivel: bool
    lojas: list[str] = field(default_factory=list)

    def to_dict(self):
        """Converte o livro para um dicionário."""
        return {
            "titulo": self.titulo,
            "autor": self.autor,
            "preco": self.preco,
            "disponivel": self.disponivel,
            "lojas": self.lojas
        }

    @classmethod
    def from_dict(cls, dados):
        """Cria um livro a partir de um dicionário."""
        return cls(
            titulo=dados["titulo"],
            autor=dados["autor"],
            preco=float(dados["preco"]),
            disponivel=dados["disponivel"],
            lojas=dados.get("lojas", [])
        )