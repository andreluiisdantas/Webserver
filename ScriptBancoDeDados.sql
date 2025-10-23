CREATE DATABASE filmes;
USE filmes;

CREATE TABLE filme(
	id_filme INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    orcamento DECIMAL(5,2) NOT NULL,
    tempo_duracao TIME NOT NULL,
    ano INT NOT NULL
);

CREATE TABLE linguagem(
	id_linguagem INT AUTO_INCREMENT PRIMARY KEY,
    linguagem VARCHAR(255) NOT NULL
);

CREATE TABLE filme_linguagem(
	id_filme_linguagem INT AUTO_INCREMENT PRIMARY KEY,
    id_filme INT NOT NULL,
    FOREIGN KEY (id_filme) REFERENCES filme(id_filme),
    id_linguagem INT NOT NULL,
    FOREIGN KEY (id_linguagem) REFERENCES linguagem(id_linguagem)
);

CREATE TABLE genero(
	id_genero INT AUTO_INCREMENT PRIMARY KEY,
    genero VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE filme_genero(
	id_filme_genero INT AUTO_INCREMENT PRIMARY KEY,
    id_filme INT NOT NULL,
    FOREIGN KEY (id_filme) REFERENCES filme(id_filme),
    id_genero INT NOT NULL,
    FOREIGN KEY (id_genero) REFERENCES genero(id_genero)
);

CREATE TABLE produtora(
	id_produtora INT AUTO_INCREMENT PRIMARY KEY,
    produtora VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE filme_produtora(
	id_filme_produtora INT AUTO_INCREMENT PRIMARY KEY,
    id_filme INT NOT NULL,
    FOREIGN KEY (id_filme) REFERENCES filme(id_filme),
    id_produtora INT NOT NULL,
    FOREIGN KEY (id_produtora) REFERENCES produtora(id_produtora)
);

CREATE TABLE pais(
	id_pais INT AUTO_INCREMENT PRIMARY KEY,
    pais VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE filme_pais(
	id_filme_pais INT AUTO_INCREMENT PRIMARY KEY,
    id_filme INT NOT NULL,
    FOREIGN KEY (id_filme) REFERENCES filme(id_filme),
    id_pais INT NOT NULL,
    FOREIGN KEY (id_pais) REFERENCES pais(id_pais)
);

CREATE TABLE nacionalidade(
	id_nacionalidade INT AUTO_INCREMENT PRIMARY KEY,
    nacionalidade VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE diretor(
	id_diretor INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    sobrenome VARCHAR(255) NOT NULL,
    genero ENUM("Masculino", "Feminino", "Outro") NOT NULL
);

CREATE TABLE filme_diretor(
	id_filme_diretor INT AUTO_INCREMENT PRIMARY KEY,
    id_filme INT NOT NULL,
    FOREIGN KEY (id_filme) REFERENCES filme(id_filme),
    id_diretor INT NOT NULL,
    FOREIGN KEY (id_diretor) REFERENCES diretor(id_diretor)
);

CREATE TABLE diretor_nacionalidade(
	id_diretor_nacionalidade INT AUTO_INCREMENT PRIMARY KEY,
    id_nacionalidade INT NOT NULL,
    FOREIGN KEY (id_nacionalidade) REFERENCES nacionalidade(id_nacionalidade),
    id_diretor INT NOT NULL,
    FOREIGN KEY (id_diretor) REFERENCES diretor(id_diretor)
);

CREATE TABLE ator(
	id_ator INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    sobrenome VARCHAR(255) NOT NULL,
    genero ENUM("Masculino", "Feminino", "Outro") NOT NULL
);

CREATE TABLE filme_ator(
	id_filme_ator INT AUTO_INCREMENT PRIMARY KEY,
    id_filme INT NOT NULL,
    FOREIGN KEY (id_filme) REFERENCES filme(id_filme),
    id_ator INT NOT NULL,
    FOREIGN KEY (id_ator) REFERENCES ator(id_ator)
);

CREATE TABLE ator_nacionalidade(
	id_ator_nacionalidade INT AUTO_INCREMENT PRIMARY KEY,
    id_nacionalidade INT NOT NULL,
    FOREIGN KEY (id_nacionalidade) REFERENCES nacionalidade(id_nacionalidade),
    id_ator INT NOT NULL,
    FOREIGN KEY (id_ator) REFERENCES ator(id_ator)
);

INSERT INTO linguagem (linguagem) VALUES
("Inglês"), ("Espanhol"), ("Francês"), ("Alemão"), ("Mandarim"),
("Japonês"), ("Russo"), ("Português"), ("Coreano"), ("Italiano"),
("Hindi"), ("Árabe"), ("Holandês"), ("Sueco"), ("Turco"),
("Polonês"), ("Vietnamita"), ("Tailandês"), ("Hebraico"), ("Grego");

INSERT INTO genero (genero) VALUES
("Ação"), ("Aventura"), ("Ficção Científica"), ("Suspense"), ("Crime"),
("Drama"), ("Comédia"), ("Fantasia"), ("Romance"), ("Animação"),
("Terror"), ("Mistério"), ("Guerra"), ("Faroeste"), ("Musical"),
("Histórico"), ("Biografia"), ("Família"), ("Esporte"), ("Documentário");

INSERT INTO produtora (produtora) VALUES
("Warner Bros."), ("Legendary Pictures"), ("Syncopy"), ("DC Comics"), ("Miramax"),
("A Band Apart"), ("Paramount Pictures"), ("Amblin Entertainment"), ("20th Century Fox"), ("Lightstorm Entertainment"),
("WingNut Films"), ("Lucasfilm"), ("Universal Pictures"), ("American Zoetrope"), ("Regency Enterprises"),
("New Line Cinema"), ("Studio Ghibli"), ("O2 Filmes"), ("Walt Disney Pictures"), ("Marvel Studios"),
("Columbia Pictures"), ("TriStar Pictures"), ("Focus Features");

INSERT INTO pais (pais) VALUES
("EUA"), ("Reino Unido"), ("Nova Zelândia"), ("Japão"), ("Coreia do Sul"),
("Brasil"), ("Canadá"), ("Austrália"), ("Alemanha"), ("França"),
("Itália"), ("Espanha"), ("China"), ("Índia"), ("México"),
("Rússia"), ("Suécia"), ("Irlanda"), ("Dinamarca"), ("Polônia");

INSERT INTO nacionalidade (nacionalidade) VALUES
("Americano"), ("Britânico"), ("Neozelandês"), ("Japonês"), ("Sul-coreano"),
("Brasileiro"), ("Canadense"), ("Australiano"), ("Alemão"), ("Francês"),
("Italiano"), ("Espanhol"), ("Chinês"), ("Indiano"), ("Mexicano"),
("Russo"), ("Sueco"), ("Irlandês"), ("Dinamarquês"), ("Polonês");

INSERT INTO diretor (id_diretor, nome, sobrenome, genero) VALUES
(1, "Christopher", "Nolan", "Masculino"),
(2, "Quentin", "Tarantino", "Masculino"),
(3, "Robert", "Zemeckis", "Masculino"),
(4, "Lana", "Wachowski", "Feminino"),
(5, "Lilly", "Wachowski", "Feminino"),
(6, "Peter", "Jackson", "Masculino"),
(7, "George", "Lucas", "Masculino"),
(8, "Steven", "Spielberg", "Masculino"),
(9, "James", "Cameron", "Masculino"),
(10, "Francis Ford", "Coppola", "Masculino"),
(11, "David", "Fincher", "Masculino"),
(12, "Martin", "Scorsese", "Masculino"),
(13, "Bong", "Joon-ho", "Masculino"),
(14, "Hayao", "Miyazaki", "Masculino"),
(15, "Fernando", "Meirelles", "Masculino"),
(16, "Jon", "Favreau", "Masculino"),
(17, "Greta", "Gerwig", "Feminino"),
(18, "Denis", "Villeneuve", "Masculino"),
(19, "Jordan", "Peele", "Masculino"),
(20, "Kathryn", "Bigelow", "Feminino"),
(21, "Guillermo", "del Toro", "Masculino"),
(22, "Sofia", "Coppola", "Feminino");

INSERT INTO ator (id_ator, nome, sobrenome, genero) VALUES
(1, "Leonardo", "DiCaprio", "Masculino"),
(2, "Joseph", "Gordon-Levitt", "Masculino"),
(3, "Christian", "Bale", "Masculino"),
(4, "Heath", "Ledger", "Masculino"),
(5, "John", "Travolta", "Masculino"),
(6, "Samuel L.", "Jackson", "Masculino"),
(7, "Tom", "Hanks", "Masculino"),
(8, "Keanu", "Reeves", "Masculino"),
(9, "Elijah", "Wood", "Masculino"),
(10, "Ian", "McKellen", "Masculino"),
(11, "Mark", "Hamill", "Masculino"),
(12, "Harrison", "Ford", "Masculino"),
(13, "Sam", "Neill", "Masculino"),
(14, "Jeff", "Goldblum", "Masculino"),
(15, "Kate", "Winslet", "Feminino"),
(16, "Sam", "Worthington", "Masculino"),
(17, "Zoe", "Saldana", "Feminino"),
(18, "Marlon", "Brando", "Masculino"),
(19, "Al", "Pacino", "Masculino"),
(20, "Liam", "Neeson", "Masculino"),
(21, "Brad", "Pitt", "Masculino"),
(22, "Edward", "Norton", "Masculino"),
(23, "Tim", "Robbins", "Masculino"),
(24, "Morgan", "Freeman", "Masculino"),
(25, "Robert", "De Niro", "Masculino"),
(26, "Song", "Kang-ho", "Masculino"),
(27, "Alexandre", "Rodrigues", "Masculino"),
(28, "Matthew", "McConaughey", "Masculino"),
(29, "Anne", "Hathaway", "Feminino"),
(30, "Scarlett", "Johansson", "Feminino");

INSERT INTO filme (id_filme, titulo, orcamento, tempo_duracao, ano) VALUES
(1, "A Origem", 160.00, "02:28:00", 2010),
(2, "Batman: O Cavaleiro das Trevas", 185.00, "02:32:00", 2008),
(3, "Pulp Fiction: Tempo de Violência", 8.50, "02:34:00", 1994),
(4, "Forrest Gump: O Contador de Histórias", 55.00, "02:22:00", 1994),
(5, "Matrix", 63.00, "02:16:00", 1999),
(6, "O Senhor dos Anéis: A Sociedade do Anel", 93.00, "02:58:00", 2001),
(7, "Star Wars: Episódio IV – Uma Nova Esperança", 11.00, "02:01:00", 1977),
(8, "Jurassic Park: O Parque dos Dinossauros", 63.00, "02:07:00", 1993),
(9, "Titanic", 200.00, "03:14:00", 1997),
(10, "Avatar", 237.00, "02:42:00", 2009),
(11, "O Poderoso Chefão", 6.50, "02:55:00", 1972),
(12, "A Lista de Schindler", 22.00, "03:15:00", 1993),
(13, "Clube da Luta", 63.00, "02:19:00", 1999),
(14, "Um Sonho de Liberdade", 25.00, "02:22:00", 1994),
(15, "Os Bons Companheiros", 25.00, "02:26:00", 1990),
(16, "Parasita", 11.40, "02:12:00", 2019),
(17, "A Viagem de Chihiro", 19.00, "02:05:00", 2001),
(18, "Cidade de Deus", 3.30, "02:10:00", 2002),
(19, "Interestelar", 165.00, "02:49:00", 2014),
(20, "O Rei Leão", 45.00, "01:28:00", 1994),
(21, "Seven: Os Sete Crimes Capitais", 33.00, "02:07:00", 1995),
(22, "Os Vingadores", 220.00, "02:23:00", 2012);

INSERT INTO filme_linguagem (id_filme, id_linguagem) VALUES
(1, 1), (1, 6), (2, 1), (3, 1), (3, 3), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1), (9, 1),
(10, 1), (11, 1), (11, 10), (12, 1), (12, 4), (13, 1), (14, 1), (15, 1), (16, 9), (17, 6),
(18, 8), (19, 1), (20, 1), (21, 1), (22, 1);

INSERT INTO filme_genero (id_filme, id_genero) VALUES
(1, 1), (1, 3), (1, 4), (2, 1), (2, 5), (2, 6), (3, 5), (3, 6), (4, 6), (4, 9), (5, 1), (5, 3),
(6, 2), (6, 6), (6, 8), (7, 1), (7, 2), (7, 8), (8, 2), (8, 3), (9, 6), (9, 9), (10, 1), (10, 2),
(10, 3), (11, 5), (11, 6), (12, 17), (12, 6), (12, 16), (13, 6), (14, 6), (15, 17), (15, 5),
(16, 6), (16, 4), (17, 10), (17, 2), (18, 5), (18, 6), (19, 2), (19, 6), (19, 3),
(20, 10), (20, 18), (21, 5), (21, 12), (22, 1), (22, 3);

INSERT INTO filme_produtora (id_filme, id_produtora) VALUES
(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 4), (3, 5), (3, 6), (4, 7), (5, 1), (6, 11),
(6, 16), (7, 12), (8, 13), (8, 8), (9, 7), (9, 9), (9, 10), (10, 9), (10, 10), (11, 14),
(12, 13), (13, 9), (13, 15), (14, 21), (15, 1), (16, 1), (17, 17), (18, 18), (19, 7), (19, 2), (19, 3),
(20, 19), (21, 16), (22, 20);

INSERT INTO filme_pais (id_filme, id_pais) VALUES
(1, 1), (1, 2), (2, 1), (2, 2), (3, 1), (4, 1), (5, 1), (6, 3), (6, 1), (7, 1), (8, 1), (9, 1),
(10, 1), (11, 1), (12, 1), (13, 1), (13, 9), (14, 1), (15, 1), (16, 5), (17, 4), (18, 6),
(19, 1), (19, 2), (20, 1), (21, 1), (22, 1);

INSERT INTO filme_diretor (id_filme, id_diretor) VALUES
(1, 1), (2, 1), (3, 2), (4, 3), (5, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 9),
(11, 10), (12, 8), (13, 11), (14, 21), (15, 12), (16, 13), (17, 14), (18, 15),
(19, 1), (20, 16), (21, 11), (22, 16);

INSERT INTO filme_ator (id_filme, id_ator) VALUES
(1, 1), (1, 2), (2, 3), (2, 4), (3, 5), (3, 6), (4, 7), (5, 8), (6, 9), (6, 10), (7, 11),
(7, 12), (8, 13), (8, 14), (9, 1), (9, 15), (10, 16), (10, 17), (11, 18), (11, 19), (12, 20),
(13, 21), (13, 22), (14, 23), (14, 24), (15, 25), (16, 26), (18, 27), (19, 28), (19, 29),
(20, 28), (21, 21), (21, 24), (22, 6), (22, 30);

INSERT INTO diretor_nacionalidade (id_diretor, id_nacionalidade) VALUES
(1, 2), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 3), (7, 1), (8, 1), (9, 7), (10, 1),
(11, 1), (12, 1), (13, 5), (14, 4), (15, 6), (16, 1), (17, 1), (18, 7), (19, 1),
(20, 1), (21, 15), (22, 1);

INSERT INTO ator_nacionalidade (id_ator, id_nacionalidade) VALUES
(1, 1), (2, 1), (3, 2), (4, 8), (5, 1), (6, 1), (7, 1), (8, 7), (9, 1), (10, 2), (11, 1),
(12, 1), (13, 3), (14, 1), (15, 2), (16, 8), (17, 1), (18, 1), (19, 1), (20, 18),
(21, 1), (22, 1), (23, 1), (24, 1), (25, 1), (26, 5), (27, 6), (28, 1), (29, 1), (30, 1);

ALTER TABLE filme ADD COLUMN sinopse TEXT;

USE filmes;

UPDATE filme SET sinopse = 'Dom Cobb é um ladrão que usa uma tecnologia de compartilhamento de sonhos para invadir o subconsciente de seus alvos e roubar informações. Impedido de voltar para casa, Cobb recebe uma oferta para ter sua ficha limpa: em vez de roubar, ele deve plantar uma ideia na mente de um alvo.' WHERE id_filme = 1;
UPDATE filme SET sinopse = 'Com a ajuda do Tenente Jim Gordon e do Promotor Harvey Dent, Batman consolida sua luta contra o crime em Gotham. No entanto, eles se deparam com um reino de caos desencadeado por um novo e genial criminoso conhecido como Coringa, que mergulha a cidade na anarquia.' WHERE id_filme = 2;
UPDATE filme SET sinopse = 'As vidas de dois assassinos de aluguel (John Travolta e Samuel L. Jackson), um boxeador e a esposa de um gângster se entrelaçam em quatro histórias de violência e redenção. Vincent Vega e Jules Winnfield trabalham para o mafioso Marsellus Wallace, enquanto o boxeador Butch Coolidge é pago para perder uma luta.' WHERE id_filme = 3;
UPDATE filme SET sinopse = 'Mesmo com um Q.I. abaixo da média, Forrest Gump (Tom Hanks) percorre três décadas da história americana, tornando-se uma testemunha e participante improvável de grandes eventos. Da Guerra do Vietnã a Watergate, ele influencia a cultura popular, tudo enquanto anseia por seu amor de infância, Jenny.' WHERE id_filme = 4;
UPDATE filme SET sinopse = 'Thomas Anderson (Keanu Reeves), um programador, descobre que o mundo em que vive é uma simulação de realidade virtual controlada por máquinas, chamada Matrix. Ele se junta a Morpheus (Laurence Fishburne) e Trinity (Carrie-Anne Moss) em uma rebelião para libertar a humanidade.' WHERE id_filme = 5;
UPDATE filme SET sinopse = 'Na Terra-média, o hobbit Frodo Bolseiro herda o Um Anel, um artefato de poder criado pelo Lorde das Trevas Sauron. Com a orientação do mago Gandalf, Frodo inicia uma perigosa jornada até a Montanha da Perdição para destruir o anel, acompanhado pela Sociedade do Anel.' WHERE id_filme = 6;
UPDATE filme SET sinopse = 'O jovem fazendeiro Luke Skywalker encontra um robô com uma mensagem de socorro da Princesa Leia. Ele se junta ao Cavaleiro Jedi Obi-Wan Kenobi e ao contrabandista Han Solo para resgatar a princesa e se unir à Aliança Rebelde na luta para destruir a Estrela da Morte, a poderosa arma do Império Galático.' WHERE id_filme = 7;
UPDATE filme SET sinopse = 'O bilionário John Hammond cria um parque temático em uma ilha remota habitado por dinossauros recriados geneticamente. Ele convida um grupo de cientistas e seus netos para uma visita, mas quando a energia falha, as criaturas pré-históricas escapam, e os visitantes precisam lutar por suas vidas.' WHERE id_filme = 8;
UPDATE filme SET sinopse = 'O artista pobre Jack (Leonardo DiCaprio) e a jovem rica Rose (Kate Winslet) se conhecem e se apaixonam durante a fatídica viagem inaugural do RMS Titanic em 1912. Eles lutam contra as convenções sociais, mas o romance é interrompido quando o navio colide com um iceberg.' WHERE id_filme = 9;
UPDATE filme SET sinopse = 'No futuro, o ex-fuzileiro naval paraplégico Jake Sully é enviado ao planeta Pandora. Usando um "avatar" (um corpo híbrido de humano e Na\'vi), ele se infiltra na raça nativa para ajudar na mineração de um mineral valioso, mas acaba se apaixonando pela cultura local e luta para protegê-la.' WHERE id_filme = 10;
UPDATE filme SET sinopse = 'Don Vito Corleone (Marlon Brando), patriarca de uma poderosa família da máfia ítalo-americana, decide transferir o controle de seu império. Uma guerra entre famílias eclode, forçando seu filho mais novo, Michael (Al Pacino), um herói de guerra, a assumir a liderança e se tornar um chefe implacável.' WHERE id_filme = 11;
UPDATE filme SET sinopse = 'Oskar Schindler (Liam Neeson), um empresário alemão membro do Partido Nazista, usa trabalhadores judeus em sua fábrica para lucrar durante a Segunda Guerra Mundial. Ao testemunhar a brutalidade do Holocausto, ele transforma sua fábrica em um refúgio, salvando mais de mil judeus dos campos de concentração.' WHERE id_filme = 12;
UPDATE filme SET sinopse = 'Um executivo deprimido (Edward Norton) e com insônia conhece Tyler Durden (Brad Pitt), um vendedor de sabão carismático. Juntos, eles criam um "clube da luta" clandestino como uma forma de terapia radical, que logo evolui para uma organização subversiva que visa destruir a sociedade de consumo.' WHERE id_filme = 13;
UPDATE filme SET sinopse = 'Andy Dufresne (Tim Robbins), um banqueiro, é condenado injustamente a duas prisões perpétuas pelo assassinato de sua esposa. Na Penitenciária de Shawshank, ele forma uma forte amizade com Red (Morgan Freeman) e usa sua inteligência e esperança para sobreviver e planejar uma fuga espetacular.' WHERE id_filme = 14;
UPDATE filme SET sinopse = 'Narra a ascensão e queda do gângster Henry Hill (Ray Liotta) na máfia de Nova York. Ao lado de seus companheiros Jimmy (Robert De Niro) e Tommy (Joe Pesci), ele se envolve no mundo do crime, mas a paranoia, as drogas e as traições eventualmente levam ao colapso de sua vida.' WHERE id_filme = 15;
UPDATE filme SET sinopse = 'A família Ki-taek, totalmente desempregada, bola um plano para se infiltrar na vida da rica família Park. Um a um, eles conseguem empregos na casa luxuosa, mas a relação simbiótica entre as duas famílias rapidamente se transforma em uma batalha selvagem pela sobrevivência.' WHERE id_filme = 16;
UPDATE filme SET sinopse = 'Chihiro, uma garota de 10 anos, descobre um mundo secreto de espíritos e deuses. Quando seus pais são misteriosamente transformados em porcos pela feiticeira Yubaba, ela deve trabalhar em uma casa de banhos mágicos para sobreviver e encontrar uma maneira de libertar seus pais.' WHERE id_filme = 17;
UPDATE filme SET sinopse = 'Contada sob a perspectiva de Buscapé, a história retrata o crescimento do crime organizado na favela Cidade de Deus, no Rio de Janeiro, dos anos 60 aos 80. Enquanto Buscapé sonha em ser fotógrafo, seu amigo Zé Pequeno se torna um dos traficantes mais temidos da região.' WHERE id_filme = 18;
UPDATE filme SET sinopse = 'Com a Terra devastada por pragas, a humanidade corre risco de extinção. Cooper (Matthew McConaughey), um ex-piloto da NASA, é recrutado para uma missão desesperada: viajar através de um buraco de minhoca recém-descoberto em busca de um novo planeta habitável.' WHERE id_filme = 19;
UPDATE filme SET sinopse = 'Simba, um jovem filhote de leão, está destinado a ser rei. No entanto, seu tio invejoso, Scar, arma uma armadilha que resulta na morte do rei Mufasa e força Simba ao exílio. Anos depois, ele deve retornar para reivindicar seu lugar de direito no trono.' WHERE id_filme = 20;
UPDATE filme SET sinopse = 'Dois detetives, o veterano Somerset (Morgan Freeman) e o impetuoso Mills (Brad Pitt), caçam um serial killer metódico que baseia seus crimes nos sete pecados capitais (Gula, Avareza, Preguiça, Luxúria, Orgulho, Inveja e Ira), criando cenas de crime macabras.' WHERE id_filme = 21;
UPDATE filme SET sinopse = 'Loki (Tom Hiddleston) rouba o Tesseract e planeja escravizar a Terra com um exército alienígena. Nick Fury (Samuel L. Jackson), diretor da S.H.I.E.L.D., reúne um time de super-heróis — Homem de Ferro, Capitão América, Thor, Hulk, Viúva Negra e Gavião Arqueiro — para salvar o mundo.' WHERE id_filme = 22;

SELECT * FROM filme;
SELECT * FROM linguagem;
SELECT * FROM filme_linguagem;
SELECT * FROM genero;
SELECT * FROM filme_genero;
SELECT * FROM produtora;
SELECT * FROM filme_produtora;
SELECT * FROM pais;
SELECT * FROM filme_pais;
SELECT * FROM nacionalidade;
SELECT * FROM diretor;
SELECT * FROM filme_diretor;
SELECT * FROM diretor_nacionalidade;
SELECT * FROM ator;
SELECT * FROM filme_ator;
SELECT * FROM ator_nacionalidade;