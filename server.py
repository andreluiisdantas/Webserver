import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

# Definindo uma classe personalizada para lidar com requisições HTTP
class MyHandle(SimpleHTTPRequestHandler):
    def list_directory(self, path):
        try:
            f = open(os.path.join(path, 'index.html'), 'r', encoding="utf-8")

            self.send_response(200)  
            self.send_header("Content-type", "text/html")  
            self.end_headers()  
            self.wfile.write(f.read().encode('utf-8')) 
            f.close()  
            return None
        except FileNotFoundError:
            pass
        return super().list_directory(path) 
    
    # Sobrescrevendo o método do_GET para tratar requisições GET
    def do_GET(self):
        if self.path == "/login":
            try:
                # Tenta abrir o arquivo 'login.html'
                with open(os.path.join(os.getcwd(), "login.html"), 'r', encoding="utf-8") as login:
                    content = login.read()
                self.send_response(200) 
                self.send_header("Content-type", "text/html")  
                self.end_headers()  
                self.wfile.write(content.encode('utf-8'))  
            except FileNotFoundError:
                self.send_error(404, "File Not Found")
        elif self.path == "/cadastro":
            try:
                with open(os.path.join(os.getcwd(), "cadastro.html"), 'r', encoding="utf-8") as cadastro:
                    content = cadastro.read()
                self.send_response(200) 
                self.send_header("Content-type", "text/html")  
                self.wfile.write(content.encode('utf-8')) 
            except FileNotFoundError:
                
                self.send_error(404, "File Not Found")
        elif self.path == "/listar_filmes":
            try:
                with open(os.path.join(os.getcwd(), "listar_filmes.html"), 'r', encoding="utf-8") as filmes:
                    content = filmes.read()
                self.send_response(200)
                self.send_header("Content-type", "text/html")  
                self.end_headers()  
                self.wfile.write(content.encode('utf-8'))  
            except FileNotFoundError:       
                self.send_error(404, "File Not Found")          
        else:
            super().do_GET()


    def accont_user(self, login, password):
        loga = "andre@gmail.com"
        senha = "123456"

        if login == loga and senha == password:
            return "Usuário Logado"
        else:
            return "Usuário não existe"
            
    def do_POST(self):
        if self.path == '/send_login':
            content_length = int(self.headers['Content-length'])
            body = self.rfile.read(content_length).decode('utf-8')
            form_data = parse_qs(body)

            login = form_data.get('usuario', [""])[0]
            password = form_data.get('senha', [""])[0]

            logou = self.accont_user(login, password)

            print("Data Form:")
            print("Usuario: ", login)        
            print("Password: ", password)    

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(logou.encode("utf-8"))
        else:
            super(MyHandle, self).do_POST()

# Função principal para iniciar o servidor
def main():
    server_address = ('', 8000)  
    httpd = HTTPServer(server_address, MyHandle) 
    print("Server Running in http://localhost:8000") 
    httpd.serve_forever() 

main() 
