import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

# Lista para armazenar os filmes cadastrados em memória
filmes_cadastrados = []

class MyHandle(SimpleHTTPRequestHandler):
    def list_directory(self, path):
        try:
            with open(os.path.join(path, 'index.html'), 'r', encoding="utf-8") as f:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(f.read().encode('utf-8'))
            return None
        except FileNotFoundError:
            pass
        return super().list_directory(path)

    # Lida com requisições GET (rotas /login, /cadastro, /listar_filmes, etc.)
    def do_GET(self):
        if self.path == "/login":
            try:
                with open(os.path.join(os.getcwd(), "login.html"), 'r', encoding="utf-8") as login_file:
                    content = login_file.read()
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
            except FileNotFoundError:
                self.send_error(404, "File Not Found")

        elif self.path == "/cadastro":
            try:
                with open(os.path.join(os.getcwd(), "cadastro.html"), 'r', encoding="utf-8") as cadastro_file:
                    content = cadastro_file.read()
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
            except FileNotFoundError:
                self.send_error(404, "File Not Found")

        elif self.path == "/listar_filmes":
            try:
                with open(os.path.join(os.getcwd(), "listar_filmes.html"), 'r', encoding="utf-8") as f:
                    content_template = f.read()

                # Monta HTML com os filmes cadastrados
                filmes_html = ""
                if not filmes_cadastrados:
                    filmes_html = "<h2>Nenhum filme cadastrado ainda.</h2>"
                else:
                    for filme in filmes_cadastrados:
                        filmes_html += f"""
                            <div class='filme-item'>
                                <h2>{filme.get('nome', 'Não informado')}</h2>
                                <p><strong>Atores:</strong> {filme.get('atores', 'Não informado')}</p>
                                <p><strong>Diretor:</strong> {filme.get('diretor', 'Não informado')}</p>
                                <p><strong>Ano:</strong> {filme.get('ano', 'Não informado')}</p>
                                <p><strong>Gênero:</strong> {filme.get('genero', 'Não informado')}</p>
                                <p><strong>Produtora:</strong> {filme.get('produtora', 'Não informado')}</p>
                                <p><strong>Sinopse:</strong> {filme.get('sinopse', 'Não informado')}</p>
                            </div>
                        """
                
                # CORREÇÃO: substitui marcador {{filmes}} no HTML em vez de string vazia
                final_content = content_template.replace("{{filmes}}", filmes_html)

                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(final_content.encode('utf-8'))
            except FileNotFoundError:
                self.send_error(404, "File Not Found")
        else:
            super().do_GET()

    # Função simples para validar login
    def account_user(self, login, password):
        loga = "andre@gmail.com"
        senha = "123456"
        return login == loga and senha == password

    # Lida com requisições POST (login e cadastro de filmes)
    def do_POST(self):
        if self.path == '/send_login':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length).decode('utf-8')
            form_data = parse_qs(body, keep_blank_values=True)

            login = form_data.get('usuario', [""])[0]
            password = form_data.get('senha', [""])[0]

            # Redireciona se login válido
            if self.account_user(login, password):
                self.send_response(302)
                self.send_header('Location', '/index.html')
                self.end_headers()
            else:
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write("Usuário ou senha inválido.".encode("utf-8"))

        elif self.path == '/send_cadastro':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length).decode('utf-8')
            form_data = parse_qs(body, keep_blank_values=True)

            # Cria novo filme a partir do formulário
            novo_filme = {
                'nome': form_data.get('nome_filme', [''])[0],
                'atores': form_data.get('atores', [''])[0],
                'diretor': form_data.get('diretor', [''])[0],
                'ano': form_data.get('ano', [''])[0],
                'genero': form_data.get('genero', [''])[0],
                'produtora': form_data.get('produtora', [''])[0],
                'sinopse': form_data.get('sinopse', [''])[0],
            }
            
            # Evita filmes duplicados
            if novo_filme not in filmes_cadastrados:
                filmes_cadastrados.append(novo_filme)
                print(f"Filme '{novo_filme['nome']}' adicionado com sucesso!")
            else:
                print(f"Filme '{novo_filme['nome']}' já existe. Não foi adicionado novamente.")
            
            print("Lista de filmes atual:", filmes_cadastrados)
            
            # Redireciona para listagem
            self.send_response(302)
            self.send_header('Location', '/listar_filmes')
            self.end_headers()
        else:
            super(MyHandle, self).do_POST()

# Inicializa o servidor
def main():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MyHandle)
    print("Server Running in http://localhost:8000")
    httpd.serve_forever()

if __name__ == '__main__':
    main()
