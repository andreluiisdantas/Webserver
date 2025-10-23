import os
import json
import mysql.connector
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse, urlencode


DB_CONFIG = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'database': 'filmes'
}

DB_FILE = 'filmes.json'

# Funções auxiliares para carregar e salvar filmes localmente em JSON
def load_movies():
    if not os.path.exists(DB_FILE):
        return []
    try:
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_movies(movies):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(movies, f, indent=4)

# Conexão com o banco de dados MySQL
def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao DB: {err}")
        return None

# Classe principal que lida com as rotas e requisições HTTP
class MyHandle(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        return

    # Envia resposta JSON
    def _send_json_response(self, data, status_code=200):
        self.send_response(status_code)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data, default=str).encode('utf-8'))

    # Envia resposta de erro em texto simples
    def _send_error_response(self, message, status_code):
        self.send_response(status_code)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(message.encode('utf-8'))

    # Rota GET para listar filmes ou servir páginas HTML
    def do_GET(self):
        if self.path == '/api/filmes':
            conn = get_db_connection()
            if not conn:
                self._send_json_response({'error': 'Erro de conexão com o banco de dados'}, 500)
                return
            
            try:
                cursor = conn.cursor(dictionary=True)
                query = """
                    SELECT 
                        f.id_filme as id, 
                        f.titulo as nome, 
                        f.ano,
                        f.sinopse, 
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
        
        # Mapeia e serve arquivos HTML conforme a rota acessada
        elif self.path in ["/", "/index.html", "/login", "/login.html", 
                           "/cadastro", "/cadastro.html", "/listar_filmes", 
                           "/listar_filmes.html", "/sucesso", "/sucesso.html"]:
            path_map = {
                "/": "index.html",
                "/index.html": "index.html",
                "/login": "login.html",
                "/login.html": "login.html",
                "/cadastro": "cadastro.html",
                "/cadastro.html": "cadastro.html",
                "/listar_filmes": "listar_filmes.html",
                "/listar_filmes.html": "listar_filmes.html",
                "/sucesso": "sucesso.html",
                "/sucesso.html": "sucesso.html"
            }
            file_path = path_map.get(self.path.split('?')[0])
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
    
    # Rota POST para login e cadastro de filmes
    def do_POST(self):
        if self.path == '/send_login':
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

        # Cadastro de novo filme com inserções em várias tabelas relacionadas
        elif self.path == '/send_cadastro':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length).decode('utf-8')
            form_data = parse_qs(body, keep_blank_values=True)
            
            nome_filme = form_data.get('nome_filme', [''])[0]
            ano_str = form_data.get('ano', [''])[0]
            atores_str = form_data.get('atores', [''])[0]
            diretor_str = form_data.get('diretor', [''])[0]
            genero_str = form_data.get('genero', [''])[0]
            produtora_str = form_data.get('produtora', [''])[0]
            sinopse = form_data.get('sinopse', [''])[0]

            if not nome_filme or not ano_str:
                self._send_error_response("Nome do filme e Ano são obrigatórios.", 400)
                return
            try:
                ano = int(ano_str)
            except ValueError:
                self._send_error_response("O ano deve ser um número.", 400)
                return
            
            orcamento_default = 0.00
            tempo_duracao_default = '00:00:00'

            conn = get_db_connection()
            if not conn:
                self._send_error_response("Erro de conexão com o banco de dados.", 500)
                return
            
            cursor = conn.cursor(dictionary=True)

            try:
                conn.start_transaction()
                cursor.execute("SELECT id_filme FROM filme WHERE titulo = %s AND ano = %s", (nome_filme, ano))
                if cursor.fetchone():
                    self._send_error_response("Este filme já está cadastrado.", 409) 
                    conn.rollback()
                    return

                query_filme = """
                    INSERT INTO filme (titulo, orcamento, tempo_duracao, ano, sinopse) 
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(query_filme, (nome_filme, orcamento_default, tempo_duracao_default, ano, sinopse))
                new_movie_id = cursor.lastrowid

                # Inserção e associação de gêneros, produtoras, atores e diretores
                if genero_str:
                    for g in [g.strip() for g in genero_str.split(',') if g.strip()]:
                        cursor.execute("INSERT IGNORE INTO genero (genero) VALUES (%s)", (g,))
                        cursor.execute("SELECT id_genero FROM genero WHERE genero = %s", (g,))
                        id_genero = cursor.fetchone()['id_genero']
                        cursor.execute("INSERT INTO filme_genero (id_filme, id_genero) VALUES (%s, %s)", (new_movie_id, id_genero))

                if produtora_str:
                    for p in [p.strip() for p in produtora_str.split(',') if p.strip()]:
                        cursor.execute("INSERT IGNORE INTO produtora (produtora) VALUES (%s)", (p,))
                        cursor.execute("SELECT id_produtora FROM produtora WHERE produtora = %s", (p,))
                        id_produtora = cursor.fetchone()['id_produtora']
                        cursor.execute("INSERT INTO filme_produtora (id_filme, id_produtora) VALUES (%s, %s)", (new_movie_id, id_produtora))
                
                if atores_str:
                    for a_full in [a.strip() for a in atores_str.split(',') if a.strip()]:
                        parts = a_full.split(' ', 1)
                        a_nome = parts[0]
                        a_sobrenome = parts[1] if len(parts) > 1 else ''
                        
                        cursor.execute("SELECT id_ator FROM ator WHERE nome = %s AND sobrenome = %s", (a_nome, a_sobrenome))
                        result = cursor.fetchone()
                        if result:
                            id_ator = result['id_ator']
                        else:
                            cursor.execute("INSERT INTO ator (nome, sobrenome, genero) VALUES (%s, %s, %s)", (a_nome, a_sobrenome, 'Outro'))
                            id_ator = cursor.lastrowid
                        cursor.execute("INSERT INTO filme_ator (id_filme, id_ator) VALUES (%s, %s)", (new_movie_id, id_ator))

                if diretor_str:
                    for d_full in [d.strip() for d in diretor_str.split(',') if d.strip()]:
                        parts = d_full.split(' ', 1)
                        d_nome = parts[0]
                        d_sobrenome = parts[1] if len(parts) > 1 else ''
                        
                        cursor.execute("SELECT id_diretor FROM diretor WHERE nome = %s AND sobrenome = %s", (d_nome, d_sobrenome))
                        result = cursor.fetchone()
                        if result:
                            id_diretor = result['id_diretor']
                        else:
                            cursor.execute("INSERT INTO diretor (nome, sobrenome, genero) VALUES (%s, %s, %s)", (d_nome, d_sobrenome, 'Outro'))
                            id_diretor = cursor.lastrowid
                        cursor.execute("INSERT INTO filme_diretor (id_filme, id_diretor) VALUES (%s, %s)", (new_movie_id, id_diretor))

                conn.commit()
                
                params = urlencode(form_data, doseq=True)
                self.send_response(302)
                self.send_header('Location', f'/sucesso.html?{params}')
                self.end_headers()

            except mysql.connector.Error as err:
                conn.rollback() 
                print(f"Erro no DB: {err}")
                self._send_error_response(f"Erro no banco de dados: {err}", 500)
            except Exception as e:
                conn.rollback() 
                print(f"Erro inesperado: {e}")
                self._send_error_response(f"Erro interno do servidor: {e}", 500)
            finally:
                if conn.is_connected():
                    cursor.close()
                    conn.close()
        else:
            super(MyHandle, self).do_POST()

    # Atualiza filme em JSON local
    def do_PUT(self):
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

    # Deleta filme do arquivo JSON local
    def do_DELETE(self):
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

# Função principal que inicia o servidor e verifica a conexão com o banco
def main():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MyHandle)
    print("Servidor rodando em http://localhost:8000")
    load_movies()
    conn = get_db_connection()
    if conn:
        print(f"Conexão com o banco de dados '{DB_CONFIG['database']}' estabelecida com sucesso.")
        conn.close()
    else:
        print(f"ERRO: Falha ao conectar ao banco de dados '{DB_CONFIG['database']}'. Verifique as credenciais.")

    httpd.serve_forever()

if __name__ == '__main__':
    main()
