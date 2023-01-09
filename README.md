## MACC

*Descrição teórica*:

O MACC (Machado de Assis – Corpus & Catálogo) é fruto de um projeto de mestrado da discente Ursula Puello Sydio, pelo Programa de Pós-Graduação em Letras Estrangeiras e Tradução do Departamento de Letras Modernas da Faculdade de Filosofia, Letras e Ciências Humanas, da Universidade de São Paulo, sob a supervisão da Orientadora: Profa. Dra. Luciana Carvalho Fonseca. É um website dedicado a criar uma ferramenta para auxiliar a comunidade de pesquisadores e profissionais das áreas de tradução, literatura e linguística.
 
O Catálogo reúne as traduções publicadas em língua inglesa do autor Machado de Assis em um catálogo atualizado e com informações relevantes como ano de publicação e tradutores da obra.

O Corpus paralelo permite que tradutores e pesquisadores comparem como diferentes versões traduziram termos e trechos específicos da obra machadiana. É um corpus paralelo de porte médio-grande com 2.105.695 palavras. Mais especificamente, dentro do corpus do MACC, o subcorpus de romances tem 1.150.161 palavras e o subcorpus de contos tem 955.534.  


*Descrição do website*:

Um website desenvolvido em Django com duas aplicações escritas em python 3.10 que rodam busca em um banco de dados em PostgreSQL.
A primeira aplicação realiza buscas no catálogo de traduções de Machado de Assis.
A segunda realiza buscas por termos no corpus paralelo. 


### Funcionalidades


-   **1- Funcionalidades do Catálogo do MACC**

- `Funcionalidade 1`: 
Uma lista cronológica das obras, ao clicar em um item, o usuário acessa uma página com uma descrição da obra.

- `Funcionalidade 2`: 
Realizar busca (por título ou gênero literário) no catálogo de traduções a partir das obras em português.

- `Funcionalidade 3`: 
Realizar busca (por título, ano, gênero literário ou país) no catálogo de traduções a partir das obras em inglês.


-   **2- Funcionalidades do Corpus do MACC**

- `Funcionalidade`: 

Busca de termo no corpus de acordo com os parâmetros:
- idioma (português ou inglês) 
- Busca ampla (contendo parte do termo);Busca exata (igual a); Início (começando com); Final(terminando com)

-   **3- Funcionalidades de Cadastro**
Realizar cadastro dos usuários para acessar o Corpus
    

Deploy:

    cp .pg.env.sample .pg.env
    cp .env.sample .env
    python manage.py collectstatic
    python manage.py migrate
    python manage.py runserver

Generate secret key:

    python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

Create a first user:

    python manage.py createsuperuser
