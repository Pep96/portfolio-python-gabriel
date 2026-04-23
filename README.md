# Portfolio com CV em Python

Portfolio profissional com CV integrado e tres demos interativas em Flask:

- AI Code Review Sandbox
- Python Challenge Generator
- Remote Productivity Portal

## Como executar

1. Crie um ambiente virtual:

```powershell
python -m venv .venv
```

2. Ative o ambiente virtual:

```powershell
.venv\Scripts\Activate.ps1
```

3. Instale as dependencias:

```powershell
pip install -r requirements.txt
```

4. Execute a aplicacao:

```powershell
python app.py
```

5. Abra no navegador:

```text
http://127.0.0.1:5000
```

## Estrutura

- `app.py`: servidor Flask e rotas das demos
- `data/profile.py`: dados do portfolio, CV e projetos
- `templates/`: layout principal e paginas de projeto
- `static/css/style.css`: identidade visual e animacoes
- `static/js/app.js`: animacoes de entrada e fundo em canvas

## Publicar no GitHub

Se quiser subir este projeto para o seu GitHub, o caminho mais simples e seguro e criar um repositorio novo so para ele.

1. No GitHub, crie um repositorio vazio.
2. Copie esta pasta para um diretorio fora de qualquer outro repositorio Git.
3. Rode estes comandos dentro da pasta do projeto:

```powershell
git init
git add .
git commit -m "Initial portfolio"
git branch -M main
git remote add origin https://github.com/Pep96/NOME-DO-REPOSITORIO.git
git push -u origin main
```

## Personalizacao

Os dados principais ficam em `data/profile.py`.
O menu e a base das paginas ficam em `templates/base.html`.
O visual esta em `static/css/style.css`.
