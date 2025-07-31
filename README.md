# 🎮 ETE-FMC Gaming Bot

> **Criado durante o AWS Vibe Coding Dojo no HackTown 2025** 🚀

Chatbot de atendimento N1 para estudantes do ETE-FMC (Escola Técnica de Eletrônica Francisco Moreira da Costa) em Santa Rita do Sapucaí, com visual gamer e integração com Amazon Bedrock.

## 🏆 Sobre o Projeto

Este projeto foi desenvolvido durante o **AWS Vibe Coding Dojo** no **HackTown 2025**, demonstrando o poder da IA generativa com Amazon Bedrock para criar soluções educacionais inovadoras.

## 🚀 Funcionalidades

- **Interface web gamer** com tema futurístico e neon
- **Integração com Amazon Bedrock** (Claude 3 Sonnet)
- **Web scraping** do site oficial da escola para informações atualizadas
- **WebSocket** para comunicação em tempo real
- **Base de conhecimento dinâmica** sobre cursos, horários e contatos
- **Visual responsivo** para desktop e mobile
- **Easter eggs** e efeitos sonoros

## 📚 Informações da Escola

### Cursos Técnicos Oferecidos:
- 💻 **Técnico em Desenvolvimento de Sistemas**
- ⚡ **Técnico em Eletrônica**
- 📡 **Técnico em Telecomunicações**
- 🏭 **Técnico em Automação Industrial**
- 🏥 **Técnico em Equipamentos Biomédicos**

### Contato:
- 📞 **(35) 3473-3600**
- 📧 **ete@etefmc.com.br**
- 📍 **Santa Rita do Sapucaí - MG - CEP 37536-016**

## 📋 Pré-requisitos

1. **Python 3.8+**
2. **Credenciais AWS** configuradas nas variáveis de ambiente:
   ```bash
   export AWS_ACCESS_KEY_ID=your_access_key
   export AWS_SECRET_ACCESS_KEY=your_secret_key
   export AWS_REGION=us-east-1  # opcional, padrão us-east-1
   ```
3. **Acesso ao Amazon Bedrock** com modelo Claude 3 Sonnet habilitado

## ⚡ Instalação Rápida

```bash
# 1. Clone o repositório
git clone <repository-url>
cd bot-ete-fmc

# 2. Crie e ative o ambiente virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# 3. Instale dependências
pip install -r requirements.txt

# 4. Execute o chatbot
python app.py
```

## 🌐 Acesso

Após iniciar, acesse: **http://localhost:5000**

## 🏗️ Arquitetura

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Flask App     │    │  Amazon Bedrock │
│   (HTML/CSS/JS) │◄──►│   + WebSocket    │◄──►│   Claude 3      │
│   Gaming Theme  │    │   + Web Scraper  │    │   Sonnet        │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │   ETE-FMC Site   │
                       │  (Live Scraping) │
                       └──────────────────┘
```

## 📁 Estrutura do Projeto

```
bot-ete-fmc/
├── app.py                  # Aplicação Flask principal
├── etefmc_scraper.py      # Web scraper do site oficial
├── test_scraper.py        # Testes do scraper
├── requirements.txt       # Dependências Python
├── static/
│   └── css/
│       └── style.css      # Tema gamer com CSS customizado
├── templates/
│   └── index.html         # Interface web do chat
├── venv/                  # Ambiente virtual (ignorado no git)
└── README.md              # Este arquivo
```

## 🎨 Visual Gamer

O chatbot possui um tema visual inspirado em gaming com:
- 🌈 **Paleta neon** (verde, azul elétrico, rosa)
- ⚡ **Animações** e efeitos de glow
- 🎵 **Efeitos sonoros** para notificações
- 🎮 **Easter egg** com Konami Code (↑↑↓↓←→←→BA)
- 🤖 **Ícones** personalizados para bot e usuário

## 🔧 Configuração Avançada

### Modelos Bedrock Disponíveis
- `anthropic.claude-3-sonnet-20240229-v1:0` (padrão)
- `anthropic.claude-3-haiku-20240307-v1:0` (mais rápido)

Para alterar o modelo, edite a variável `MODEL_ID` no `app.py`.

### Atualização da Base de Conhecimento
O scraper atualiza automaticamente as informações do site a cada hora. Para forçar atualização:

```bash
curl -X POST http://localhost:5000/api/update-knowledge
```

## 🚀 Deploy para Produção

### AWS Lambda + API Gateway
```bash
pip install zappa
zappa init
zappa deploy production
```

### AWS EC2
```bash
pip install gunicorn
gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:5000 app:app
```

## 🔍 API Endpoints

- `GET /` - Interface principal do chat
- `POST /api/chat` - Endpoint REST para mensagens
- `POST /api/update-knowledge` - Força atualização da base de conhecimento
- `GET /api/knowledge-status` - Status da base de conhecimento

## 🛠️ Desenvolvimento

### Testando o Scraper
```bash
python test_scraper.py
```

### Adicionando Novas Funcionalidades
1. Edite `etefmc_scraper.py` para novos dados
2. Modifique o prompt do sistema em `query_bedrock()`
3. Atualize o CSS em `static/css/style.css` para mudanças visuais

## 🎯 HackTown 2025 - AWS Vibe Coding Dojo

Este projeto demonstra:
- **IA Generativa** com Amazon Bedrock
- **Web Scraping** inteligente para dados dinâmicos
- **Interface moderna** com tema gaming
- **Arquitetura serverless** pronta para produção
- **Integração AWS** com boas práticas

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Projeto educacional desenvolvido durante o HackTown 2025.

## 🏫 Sobre o ETE-FMC

O ETE-FMC (Escola Técnica de Eletrônica Francisco Moreira da Costa) é uma instituição de ensino técnico reconhecida em Santa Rita do Sapucaí, MG, conhecida como o "Vale da Eletrônica".

---

**Desenvolvido com ❤️ durante o AWS Vibe Coding Dojo no HackTown 2025** 🚀

**Santa Rita do Sapucaí - Vale da Eletrônica** 🏫⚡
