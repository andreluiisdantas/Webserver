import os
import json
import time
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

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

class MyHandle(SimpleHTTPRequestHandler):
    # Sobrescreve o método de log para um terminal mais limpo
    def log_message(self, format, *args):
        return

    def _send_json_response(self, data, status_code=200):
        self.send_response(status_code)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def do_GET(self):
        # Endpoint da API para listar filmes
        if self.path == '/api/filmes':
            movies = load_movies()
            self._send_json_response(movies)
        
        # Servir arquivos estáticos (HTML, CSS, etc.)
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
    
    # Lida com requisições POST (login e cadastro de filmes)
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
        # Rota para editar um filme: /api/filmes/{id}
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
                        movies[i]['id'] = movie_id # Garante que o ID não seja alterado
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
                    self.send_response(204) # No Content
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
    httpd.serve_forever()

if __name__ == '__main__':
    main()