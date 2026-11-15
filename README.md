# Spotify Charts Brasil – Time Machine Playlist

Um projeto desenvolvido em **Python** que permite viajar no tempo através da música brasileira e internacional mais ouvida no Brasil. Informe uma data e o programa buscará o ranking diário do Spotify Brasil, criando automaticamente uma playlist privada na sua conta do Spotify com as músicas daquele período.

## 🎯 Sobre o projeto

A proposta é permitir que o usuário relembre os sucessos musicais de uma data específica, transformando rankings históricos do Spotify Brasil em playlists personalizadas.

O programa utiliza o ranking diário **Top Songs Brazil** para recuperar as músicas mais ouvidas no país e, em seguida, utiliza a integração com o Spotify para criar uma playlist com os resultados.

## ✨ Funcionalidades

- 📅 Escolher uma data específica no formato `YYYY-MM-DD`.
- 🇧🇷 Consultar o ranking diário do Spotify Brasil.
- 🎵 Recuperar até 200 músicas do ranking.
- 🔎 Pesquisar músicas no catálogo do Spotify quando necessário.
- 🔗 Obter os URIs das faixas para adicioná-las à playlist.
- 📂 Criar automaticamente uma playlist privada.
- 📊 Preservar a ordem de classificação do ranking.
- ⚠️ Informar quais músicas não foram encontradas.

## 🛠️ Tecnologias utilizadas

- **Python** – Linguagem de programação.
- **Requests** – Realização de requisições HTTP.
- **Spotipy** – Integração com a API do Spotify.
- **Python-dotenv** – Gerenciamento de variáveis de ambiente.
- **Spotify Charts** – Fonte dos rankings musicais.

## 📋 Pré-requisitos

Antes de executar o projeto, você precisará de:

- Python 3 instalado.
- Uma conta no Spotify.
- Uma aplicação cadastrada no [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/).
- Credenciais de acesso da aplicação (Client ID e Client Secret).

## 📦 Instalação

Clone este repositório:

```bash
git clone https://github.com/SEU-USUARIO/spotify-charts-brasil.git
```

Entre na pasta do projeto:

```bash
cd spotify-charts-brasil
```

Instale as dependências:

```bash
pip install requests python-dotenv spotipy
```

## 🔐 Configuração das credenciais

Crie um arquivo chamado `.env` na raiz do projeto:

```env
SPOTIFY_CLIENT_ID=seu_client_id
SPOTIFY_CLIENT_SECRET=seu_client_secret
SPOTIFY_REDIRECT_URI=http://127.0.0.1:8888/callback
SPOTIFY_BEARER=seu_token_do_spotify_charts
```

Substitua os valores de exemplo pelas suas próprias credenciais.

### Como obter as credenciais?

**1. Spotify Developer Dashboard**

Acesse o [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/), crie uma aplicação e obtenha:

- Client ID
- Client Secret

Configure também o Redirect URI utilizado pelo projeto nas configurações da aplicação.

**2. Spotify Charts Bearer Token**

O projeto utiliza um endpoint interno do Spotify Charts para consultar rankings históricos.

Para obter o token, entre no Spotify Charts com sua conta, abra as ferramentas de desenvolvedor do navegador (`F12`) e utilize a aba Network para localizar a requisição do ranking diário do Brasil.

Nos cabeçalhos da requisição, procure `Authorization` e copie o valor que aparece depois de `Bearer`.

**Importante:** esse token pode expirar e o endpoint utilizado não é uma API pública oficialmente documentada. Pode ser necessário atualizar o token ou adaptar o código caso o Spotify altere o serviço.

## ▶️ Como executar

Depois de configurar as credenciais, execute:

```bash
python main.py
```

O programa solicitará uma data:

```text
Para qual data você quer viajar no tempo?
Digite YYYY-MM-DD: 2024-01-01
```

Em seguida, buscará as músicas correspondentes ao ranking brasileiro daquela data.

Após a pesquisa, criará uma playlist privada na sua conta do Spotify.

## 🎧 Resultado esperado

A playlist será criada automaticamente com o seguinte padrão de nome:

```text
Brasil - 2024-01-01
```

O programa também exibirá o link da playlist no terminal para facilitar o acesso.

## 🔒 Segurança

As credenciais e os tokens de autenticação devem permanecer protegidos.

Não compartilhe o arquivo `.env` nem publique seus tokens no GitHub.

Recomenda-se adicionar o seguinte conteúdo ao arquivo `.gitignore`:

```gitignore
.env
.spotify_cache
__pycache__/
*.pyc
```

## 🚀 Possíveis melhorias futuras

- Permitir a criação de playlists com rankings de diferentes países.
- Adicionar rankings semanais.
- Implementar filtros por artistas brasileiros.
- Criar uma interface gráfica para facilitar a utilização.
- Permitir escolher a quantidade de músicas da playlist.
- Melhorar o tratamento de erros e a renovação de tokens.