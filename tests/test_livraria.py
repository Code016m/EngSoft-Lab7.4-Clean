import unittest
import tempfile
import shutil
import json

from pathlib import Path

from app import create_app
from infrastructure.arquivo_txt_repository import ArquivoTxtRepository

class TestLivraria(unittest.TestCase):

    def setUp(self):
        """Prepara um arquivo TXT independente para cada teste."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.caminho_dados = Path(self.temp_dir.name) / "livros.txt"
        arquivo_original = (
                Path(__file__).resolve().parent.parent
                / "data"
                / "livros.txt"
        )
        shutil.copy(arquivo_original, self.caminho_dados)
        # Inicia cada teste com a lista de favoritos vazia.
        with open(self.caminho_dados, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
        dados["favoritos"] = []
        with open(self.caminho_dados, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=4)
        self.repository = ArquivoTxtRepository(self.caminho_dados)
        self.app = create_app(self.repository)
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

    def tearDown(self):
        """Remove os arquivos temporários após cada teste."""
        self.temp_dir.cleanup()

    # Testes de livros
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
        response = self.client.get(
            "/api/livros?q=Machado%20de%20Assis"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 2)

    def test_consultar_livro_existente(self):
        response = self.client.get("/api/livros/Dom%20Casmurro")
        self.assertEqual(response.status_code, 200)
        livro = response.get_json()
        self.assertEqual(livro["titulo"], "Dom Casmurro")
        self.assertEqual(livro["autor"], "Machado de Assis")
        self.assertEqual(livro["preco"], 30.0)

    def test_consultar_livro_inexistente(self):
        response = self.client.get(
            "/api/livros/Livro%20Inexistente"
        )

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
        self.assertTrue(len(response.get_json()) > 0)

    # Testes de favoritos
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
        favoritos = self.client.get("/api/favoritos").get_json()
        self.assertEqual(len(favoritos), 1)
        self.assertEqual(favoritos[0]["titulo"], "Dom Casmurro")

    def test_nao_adicionar_favorito_duplicado(self):
        self.client.post(
            "/api/favoritos",
            json={"titulo": "Dom Casmurro"}
        )
        self.client.post(
            "/api/favoritos",
            json={"titulo": "Dom Casmurro"}
        )
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

    # Teste de persistência
    def test_persistencia_dos_favoritos_em_arquivo_txt(self):
        self.repository.adicionar_favorito("Dom Casmurro")
        novo_repository = ArquivoTxtRepository(
            self.caminho_dados
        )
        favoritos = novo_repository.listar_favoritos()
        self.assertEqual(len(favoritos), 1)
        self.assertEqual(
            favoritos[0].titulo,
            "Dom Casmurro"
        )

if __name__ == "__main__":
    unittest.main(verbosity=2)
