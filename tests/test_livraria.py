"""Testes das funcionalidades da livraria e da arquitetura multicamadas."""

import unittest

from app import create_app
from repositories import livraria_repository as repository

class TestLivraria(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Cria a aplicação para os testes."""
        cls.app = create_app()
        cls.app.config["TESTING"] = True
        cls.client = cls.app.test_client()

    def setUp(self):
        """Limpa os favoritos antes de cada teste."""
        repository.FAVORITOS.clear()

    # Testes das funcionalidades antigas

    def test_listar_livros(self):
        response = self.client.get("/api/livros")
        self.assertEqual(response.status_code, 200)
        livros = response.get_json()
        self.assertEqual(len(livros), 7)
        self.assertTrue(
            any(livro["titulo"] == "Dom Casmurro" for livro in livros)
        )

    def test_pesquisar_livros_por_titulo(self):
        response = self.client.get("/api/livros?q=Dom%20Casmurro")
        self.assertEqual(response.status_code, 200)
        livros = response.get_json()
        self.assertEqual(len(livros), 1)
        self.assertEqual(livros[0]["titulo"], "Dom Casmurro")

    def test_pesquisar_livros_por_autor(self):
        response = self.client.get("/api/livros?q=Machado%20de%20Assis")
        self.assertEqual(response.status_code, 200)
        livros = response.get_json()
        self.assertEqual(len(livros), 2)

    def test_consultar_livro_existente(self):
        response = self.client.get("/api/livros/Dom%20Casmurro")
        self.assertEqual(response.status_code, 200)
        livro = response.get_json()
        self.assertEqual(livro["titulo"], "Dom Casmurro")
        self.assertEqual(livro["autor"], "Machado de Assis")
        self.assertEqual(livro["preco"], 30.0)

    def test_consultar_livro_inexistente(self):
        response = self.client.get("/api/livros/Livro%20Inexistente")
        self.assertEqual(response.status_code, 404)
        self.assertIn("erro", response.get_json())

    def test_consultar_disponibilidade_de_livro_disponivel(self):
        response = self.client.get(
            "/api/livros/Dom%20Casmurro/disponibilidade"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.get_json()["disponivel"])

    def test_consultar_disponibilidade_de_livro_indisponivel(self):
        response = self.client.get(
            "/api/livros/Vidas%20Secas/disponibilidade"
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.get_json()["disponivel"])

    def test_consultar_disponibilidade_de_livro_inexistente(self):
        response = self.client.get(
            "/api/livros/Livro%20Inexistente/disponibilidade"
        )
        self.assertEqual(response.status_code, 404)

    def test_consultar_horario(self):
        response = self.client.get("/api/horario")
        self.assertEqual(response.status_code, 200)
        self.assertIn("horario", response.get_json())

    def test_consultar_localizacao(self):
        response = self.client.get("/api/localizacao")
        self.assertEqual(response.status_code, 200)
        self.assertIn("localizacao", response.get_json())

    def test_obter_recomendacoes(self):
        response = self.client.get("/api/recomendacoes")
        self.assertEqual(response.status_code, 200)
        livros = response.get_json()
        self.assertTrue(len(livros) > 0)

    # Testes da nova funcionalidade de favoritos

    def test_listar_favoritos_vazios(self):
        response = self.client.get("/api/favoritos")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [])

    def test_adicionar_livro_aos_favoritos(self):
        response = self.client.post(
            "/api/favoritos",
            json={"titulo": "Dom Casmurro"}
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("mensagem", response.get_json())
        favoritos = self.client.get("/api/favoritos").get_json()
        self.assertEqual(len(favoritos), 1)
        self.assertEqual(favoritos[0]["titulo"], "Dom Casmurro")

    def test_nao_adicionar_favorito_duplicado(self):
        self.client.post(
            "/api/favoritos",
            json={"titulo": "Dom Casmurro"}
        )
        response = self.client.post(
            "/api/favoritos",
            json={"titulo": "Dom Casmurro"}
        )
        self.assertEqual(response.status_code, 201)
        favoritos = self.client.get("/api/favoritos").get_json()
        self.assertEqual(len(favoritos), 1)

    def test_adicionar_livro_inexistente_aos_favoritos(self):
        response = self.client.post(
            "/api/favoritos",
            json={"titulo": "Livro Inexistente"}
        )
        self.assertEqual(response.status_code, 404)

    def test_remover_livro_dos_favoritos(self):
        self.client.post(
            "/api/favoritos",
            json={"titulo": "Dom Casmurro"}
        )
        response = self.client.delete(
            "/api/favoritos/Dom%20Casmurro"
        )
        self.assertEqual(response.status_code, 200)
        favoritos = self.client.get("/api/favoritos").get_json()
        self.assertEqual(favoritos, [])

    def test_remover_livro_que_nao_e_favorito(self):
        response = self.client.delete(
            "/api/favoritos/Dom%20Casmurro"
        )
        self.assertEqual(response.status_code, 404)

    def test_adicionar_dois_favoritos_diferentes(self):
        self.client.post(
            "/api/favoritos",
            json={"titulo": "Dom Casmurro"}
        )
        self.client.post(
            "/api/favoritos",
            json={"titulo": "O Cortiço"}
        )
        favoritos = self.client.get("/api/favoritos").get_json()
        titulos = [livro["titulo"] for livro in favoritos]
        self.assertEqual(len(favoritos), 2)
        self.assertIn("Dom Casmurro", titulos)
        self.assertIn("O Cortiço", titulos)

if __name__ == "__main__":
    unittest.main(verbosity=2)
