import os
from http.server import SimpleHTTPRequestHandler, HTTPServer

# Definindo uma classe personalizada para lidar com requisições HTTP
class MyHandle(SimpleHTTPRequestHandler):
    # Sobrescrevendo o método list_directory para servir um arquivo 'index.html'
    def list_directory(self, path):
        try:
            # Tenta abrir o arquivo 'index.html' no diretório solicitado
            f = open(os.path.join(path, 'index.html'), 'r', encoding="utf-8")

            self.send_response(200)  # Envia uma resposta HTTP 200 (OK)
            self.send_header("Content-type", "text/html")  # Define o tipo de conteúdo como HTML
            self.end_headers()  # Finaliza os cabeçalhos da resposta
            # Especificando a codificação como utf-8
            self.wfile.write(f.read().encode('utf-8'))  # Envia o conteúdo do arquivo
            f.close()  # Fecha o arquivo
            return None
        except FileNotFoundError:
            # Se não encontrar o arquivo, continua com o comportamento padrão
            pass
        return super().list_directory(path)  # Chama o método original se o arquivo não for encontrado
    
    # Sobrescrevendo o método do_GET para tratar requisições GET
    def do_GET(self):
        if self.path == "/login":
            try:
                # Tenta abrir o arquivo 'login.html'
                with open(os.path.join(os.getcwd(), "login.html"), 'r', encoding="utf-8") as login:
                    content = login.read()
                self.send_response(200)  # Envia uma resposta HTTP 200 (OK)
                self.send_header("Content-type", "text/html")  # Define o tipo de conteúdo como HTML
                self.end_headers()  # Finaliza os cabeçalhos da resposta
                self.wfile.write(content.encode('utf-8'))  # Envia o conteúdo do arquivo
            except FileNotFoundError:
                # Se o arquivo não for encontrado, envia erro 404
                self.send_error(404, "File Not Found")
        elif self.path == "/cadastro":
            try:
                # Tenta abrir o arquivo 'cadastro.html'
                with open(os.path.join(os.getcwd(), "cadastro.html"), 'r', encoding="utf-8") as cadastro:
                    content = cadastro.read()
                self.send_response(200)  # Envia uma resposta HTTP 200 (OK)
                self.send_header("Content-type", "text/html")  # Define o tipo de conteúdo como HTML
                self.end_headers()  # Finaliza os cabeçalhos da resposta
                self.wfile.write(content.encode('utf-8'))  # Envia o conteúdo do arquivo
            except FileNotFoundError:
                # Se o arquivo não for encontrado, envia erro 404
                self.send_error(404, "File Not Found")
        elif self.path == "/listar_filmes":
            try:
                # Tenta abrir o arquivo 'filmes.html'
                with open(os.path.join(os.getcwd(), "listar_filmes.html"), 'r', encoding="utf-8") as filmes:
                    content = filmes.read()
                self.send_response(200)  # Envia uma resposta HTTP 200 (OK)
                self.send_header("Content-type", "text/html")  # Define o tipo de conteúdo como HTML
                self.end_headers()  # Finaliza os cabeçalhos da resposta
                self.wfile.write(content.encode('utf-8'))  # Envia o conteúdo do arquivo
            except FileNotFoundError:
                # Se o arquivo não for encontrado, envia erro 404
                self.send_error(404, "File Not Found")          
        else:
            # Para outras requisições, chama o comportamento padrão
            super().do_GET()

# Função principal para iniciar o servidor
def main():
    server_address = ('', 8000)  # Define o endereço do servidor (localhost na porta 8000)
    httpd = HTTPServer(server_address, MyHandle)  # Cria o servidor HTTP
    print("Server Running in http://localhost:8000")  # Informa que o servidor está rodando
    httpd.serve_forever()  # Inicia o servidor e fica esperando requisições

main()  # Chama a função main para rodar o servidor
