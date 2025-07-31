import os
import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import boto3
from botocore.exceptions import ClientError
import logging
from etefmc_scraper import scraper

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'ete-fmc-dev-key')
socketio = SocketIO(app, cors_allowed_origins="*")

# Cliente Bedrock usando credenciais das variáveis de ambiente
bedrock_client = boto3.client(
    'bedrock-runtime',
    region_name=os.environ.get('AWS_REGION', 'us-east-1')
)

# Configurações do modelo
MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"

def get_etefmc_context():
    """Obtém contexto atualizado do site ETE-FMC"""
    try:
        knowledge_base = scraper.get_knowledge_base()
        return json.dumps(knowledge_base, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Erro ao obter contexto do site: {e}")
        return json.dumps(scraper.get_fallback_data(), indent=2, ensure_ascii=False)

def query_bedrock(prompt, user_context=""):
    """Consulta o modelo Claude via Bedrock com informações do site ETE-FMC"""
    try:
        # Obtém informações atualizadas do site
        site_context = get_etefmc_context()
        
        # Busca informações específicas relacionadas à pergunta
        search_results = scraper.search_info(prompt)
        search_context = "\n".join(search_results) if search_results else ""
        
        # Prompt contextualizado para o ETE-FMC
        system_prompt = f"""
        Você é o assistente virtual oficial do ETE-FMC (Escola Técnica de Eletrônica Francisco Moreira da Costa) 
        em Santa Rita do Sapucaí, MG. Você tem acesso às informações mais atualizadas do site oficial da escola.
        
        INFORMAÇÕES ATUALIZADAS DO SITE ETE-FMC:
        {site_context}
        
        INFORMAÇÕES ESPECÍFICAS PARA ESTA PERGUNTA:
        {search_context}
        
        INSTRUÇÕES:
        - Use SEMPRE as informações do site oficial como fonte primária
        - Seja preciso e objetivo nas respostas
        - Mantenha um tom amigável e profissional
        - Se não souber algo específico, oriente o estudante a entrar em contato com a secretaria
        - Destaque informações importantes como cursos, horários e contatos
        - Use emojis moderadamente para tornar a conversa mais amigável
        
        CONTEXTO ADICIONAL:
        {user_context}
        """
        
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "system": system_prompt,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        
        response = bedrock_client.invoke_model(
            modelId=MODEL_ID,
            body=json.dumps(body)
        )
        
        response_body = json.loads(response['body'].read())
        return response_body['content'][0]['text']
        
    except ClientError as e:
        logger.error(f"Erro no Bedrock: {e}")
        return "Desculpe, estou com problemas técnicos. Tente novamente em alguns minutos ou entre em contato com a secretaria: (35) 3471-9200."
    except Exception as e:
        logger.error(f"Erro geral: {e}")
        return "Ocorreu um erro inesperado. Por favor, contate o suporte técnico ou a secretaria da escola."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat_api():
    """Endpoint REST para chat"""
    data = request.get_json()
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({'error': 'Mensagem não pode estar vazia'}), 400
    
    response = query_bedrock(user_message)
    return jsonify({
        'response': response,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/update-knowledge', methods=['POST'])
def update_knowledge():
    """Endpoint para forçar atualização da base de conhecimento"""
    try:
        knowledge_base = scraper.get_knowledge_base(force_update=True)
        return jsonify({
            'status': 'success',
            'message': 'Base de conhecimento atualizada',
            'last_update': scraper.last_update.isoformat() if scraper.last_update else None,
            'courses_count': len(knowledge_base.get('cursos', [])),
            'news_count': len(knowledge_base.get('noticias', []))
        })
    except Exception as e:
        logger.error(f"Erro ao atualizar base de conhecimento: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/knowledge-status')
def knowledge_status():
    """Endpoint para verificar status da base de conhecimento"""
    try:
        kb = scraper.knowledge_base
        return jsonify({
            'last_update': scraper.last_update.isoformat() if scraper.last_update else None,
            'courses_count': len(kb.get('cursos', [])),
            'news_count': len(kb.get('noticias', [])),
            'has_contact_info': bool(kb.get('contatos', {}).get('telefones')),
            'site_url': scraper.base_url
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@socketio.on('user_message')
def handle_message(data):
    """Handler WebSocket para chat em tempo real"""
    user_message = data.get('message', '')
    user_id = data.get('user_id', 'anonymous')
    
    logger.info(f"Mensagem recebida de {user_id}: {user_message}")
    
    # Processa a mensagem com contexto do site
    bot_response = query_bedrock(user_message)
    
    # Envia resposta de volta
    emit('bot_response', {
        'message': bot_response,
        'timestamp': datetime.now().isoformat(),
        'user_id': user_id
    })

@socketio.on('connect')
def handle_connect():
    logger.info('Cliente conectado')
    
    # Carrega informações básicas do site ao conectar
    try:
        scraper.get_knowledge_base()
        status_msg = f"🎮 Conectado ao ETE-FMC Gaming Bot! Informações atualizadas do site oficial."
    except:
        status_msg = "🎮 Conectado ao ETE-FMC Gaming Bot! (Modo offline)"
    
    emit('status', {'msg': status_msg})

@socketio.on('disconnect')
def handle_disconnect():
    logger.info('Cliente desconectado')

if __name__ == '__main__':
    # Verifica se as credenciais AWS estão configuradas
    try:
        sts = boto3.client('sts')
        identity = sts.get_caller_identity()
        logger.info(f"AWS configurado para: {identity.get('Arn', 'N/A')}")
    except Exception as e:
        logger.error(f"Erro na configuração AWS: {e}")
        logger.error("Verifique suas credenciais AWS nas variáveis de ambiente")
    
    # Carrega informações iniciais do site
    try:
        logger.info("Carregando informações do site ETE-FMC...")
        scraper.get_knowledge_base()
        logger.info("✅ Informações do site carregadas com sucesso!")
    except Exception as e:
        logger.warning(f"⚠️ Erro ao carregar site: {e}. Usando dados de fallback.")
    
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
