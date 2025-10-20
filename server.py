import os
import json
import mysql.connector # Adicionado para conexão com o banco
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse


# --- Configuração do Banco de Dados ---
DB_CONFIG = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'database': 'filmes'
}

# Nome do arquivo para persistir os dados
DB_FILE = 'filmes.json'

# Função para carregar filmes do arquivo JSON
def load_movies():
    if not os.path.exists(DB_FILE):
        return []
    try:
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

# Função para salvar filmes no arquivo JSON
def save_movies(movies):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(movies, f, indent=4)

# Função para obter conexão com o banco de dados
def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao DB: {err}")
        return None

class MyHandle(SimpleHTTPRequestHandler):
    # Sobrescreve o método de log para um terminal mais limpo
    def log_message(self, format, *args):
        return

    def _send_json_response(self, data, status_code=200):
        self.send_response(status_code)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        # default=str lida com tipos de dados não serializáveis como TIME do banco
        self.wfile.write(json.dumps(data, default=str).encode('utf-8'))

    def do_GET(self):
        # Endpoint da API para listar filmes (MODIFICADO PARA USAR O BANCO DE DADOS)
        if self.path == '/api/filmes':
            conn = get_db_connection()
            if not conn:
                self._send_json_response({'error': 'Erro de conexão com o banco de dados'}, 500)
                return
            
            try:
                cursor = conn.cursor(dictionary=True)
                # Query complexa que junta várias tabelas para montar o resultado
                query = """
                    SELECT 
                        f.id_filme as id, 
                        f.titulo as nome, 
                        f.ano,
                        GROUP_CONCAT(DISTINCT a.nome, ' ', a.sobrenome SEPARATOR ', ') as atores,
                        GROUP_CONCAT(DISTINCT d.nome, ' ', d.sobrenome SEPARATOR ', ') as diretor,
                        GROUP_CONCAT(DISTINCT g.genero SEPARATOR ', ') as genero,
                        GROUP_CONCAT(DISTINCT p.produtora SEPARATOR ', ') as produtora
                    FROM filme f
                    LEFT JOIN filme_ator fa ON f.id_filme = fa.id_filme
                    LEFT JOIN ator a ON fa.id_ator = a.id_ator
                    LEFT JOIN filme_diretor fd ON f.id_filme = fd.id_filme
                    LEFT JOIN diretor d ON fd.id_diretor = d.id_diretor
                    LEFT JOIN filme_genero fg ON f.id_filme = fg.id_filme
                    LEFT JOIN genero g ON fg.id_genero = g.id_genero
                    LEFT JOIN filme_produtora fp ON f.id_filme = fp.id_filme
                    LEFT JOIN produtora p ON fp.id_produtora = p.id_produtora
                    GROUP BY f.id_filme;
                """
                cursor.execute(query)
                movies_from_db = cursor.fetchall()
                self._send_json_response(movies_from_db)

            except mysql.connector.Error as err:
                self._send_json_response({'error': f'Erro no banco de dados: {err}'}, 500)
            finally:
                if conn.is_connected():
                    cursor.close()
                    conn.close()
        
        # Servir arquivos estáticos (HTML, CSS, etc.) - SEM ALTERAÇÕES
        elif self.path in ["/", "/index.html", "/login", "/login.html", "/cadastro", "/cadastro.html", "/listar_filmes", "/listar_filmes.html"]:
            path_map = {
                "/": "index.html",
                "/index.html": "index.html",
                "/login": "login.html",
                "/login.html": "login.html",
                "/cadastro": "cadastro.html",
                "/cadastro.html": "cadastro.html",
                "/listar_filmes": "listar_filmes.html",
                "/listar_filmes.html": "listar_filmes.html"
            }
            file_path = path_map.get(self.path)
            if file_path:
                try:
                    with open(os.path.join(os.getcwd(), file_path), 'r', encoding="utf-8") as f:
                        content = f.read()
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    self.wfile.write(content.encode('utf-8'))
                except FileNotFoundError:
                    self.send_error(404, "File Not Found")
            else:
                super().do_GET()
        else:
            super().do_GET()
    
    # Lida com requisições POST (login e cadastro de filmes) - SEM ALTERAÇÕES
    def do_POST(self):
        if self.path == '/send_login':
            # (Lógica de login permanece a mesma)
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length).decode('utf-8')
            form_data = parse_qs(body, keep_blank_values=True)
            login = form_data.get('usuario', [""])[0]
            password = form_data.get('senha', [""])[0]

            if login == "andre@gmail.com" and password == "123456":
                self.send_response(302)
                self.send_header('Location', '/index.html')
                self.end_headers()
            else:
                self.send_response(401)
                self.end_headers()
                self.wfile.write("Usuário ou senha inválido.".encode("utf-8"))

        elif self.path == '/send_cadastro':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length).decode('utf-8')
            form_data = parse_qs(body, keep_blank_values=True)
            
            movies = load_movies()

            # Lógica para gerar o novo ID auto-incrementado
            if movies:
                # Encontra o ID máximo existente e adiciona 1
                new_id = max(movie.get('id', 0) for movie in movies) + 1
            else:
                # Se não houver filmes, o primeiro ID é 1
                new_id = 1

            novo_filme = {
                'id': new_id,
                'nome': form_data.get('nome_filme', [''])[0],
                'atores': form_data.get('atores', [''])[0],
                'diretor': form_data.get('diretor', [''])[0],
                'ano': form_data.get('ano', [''])[0],
                'genero': form_data.get('genero', [''])[0],
                'produtora': form_data.get('produtora', [''])[0],
                'sinopse': form_data.get('sinopse', [''])[0],
            }
            
            movies.append(novo_filme)
            save_movies(movies)
            
            self.send_response(302)
            self.send_header('Location', '/listar_filmes')
            self.end_headers()
        else:
            super(MyHandle, self).do_POST()

    def do_PUT(self):
        # Rota para editar um filme: /api/filmes/{id} - SEM ALTERAÇÕES
        parsed_path = urlparse(self.path)
        path_parts = parsed_path.path.strip('/').split('/')

        if len(path_parts) == 3 and path_parts[0] == 'api' and path_parts[1] == 'filmes':
            try:
                movie_id = int(path_parts[2])
                content_length = int(self.headers['Content-Length'])
                body = self.rfile.read(content_length)
                updated_data = json.loads(body)

                movies = load_movies()
                movie_found = False
                for i, movie in enumerate(movies):
                    if movie.get('id') == movie_id:
                        movies[i] = updated_data
                        movies[i]['id'] = movie_id 
                        movie_found = True
                        break
                
                if movie_found:
                    save_movies(movies)
                    self._send_json_response(movies[i])
                else:
                    self._send_json_response({'error': 'Filme não encontrado'}, 404)
            except (ValueError, json.JSONDecodeError):
                self._send_json_response({'error': 'Dados inválidos'}, 400)
        else:
            self.send_error(404, "Endpoint não encontrado")

    def do_DELETE(self):
        # Rota para deletar um filme: /api/filmes/{id}
        parsed_path = urlparse(self.path)
        path_parts = parsed_path.path.strip('/').split('/')

        if len(path_parts) == 3 and path_parts[0] == 'api' and path_parts[1] == 'filmes':
            try:
                movie_id = int(path_parts[2])
                movies = load_movies()
                
                initial_len = len(movies)
                movies_updated = [movie for movie in movies if movie.get('id') != movie_id]

                if len(movies_updated) < initial_len:
                    save_movies(movies_updated)
                    self.send_response(204)
                    self.end_headers()
                else:
                    self._send_json_response({'error': 'Filme não encontrado'}, 404)
            except ValueError:
                 self._send_json_response({'error': 'ID inválido'}, 400)
        else:
            self.send_error(404, "Endpoint não encontrado")

def main():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MyHandle)
    print("Servidor rodando em http://localhost:8000")
    # Garante que o arquivo de filmes exista
    load_movies()
    # Adicionada verificação de conexão com o banco ao iniciar
    conn = get_db_connection()
    if conn:
        print(f"Conexão com o banco de dados '{DB_CONFIG['database']}' estabelecida com sucesso.")
        conn.close()
    else:
        print(f"ERRO: Falha ao conectar ao banco de dados '{DB_CONFIG['database']}'. Verifique as credenciais.")

    httpd.serve_forever()

if __name__ == '__main__':
    main()