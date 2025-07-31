#!/bin/bash

echo "🚀 Iniciando Chatbot ETE-FMC"
echo "=================================="

# Ativa ambiente virtual
source venv/bin/activate

# Verifica credenciais AWS
if [ -z "$AWS_ACCESS_KEY_ID" ] || [ -z "$AWS_SECRET_ACCESS_KEY" ]; then
    echo "❌ Credenciais AWS não configuradas!"
    echo "Configure as variáveis de ambiente:"
    echo "export AWS_ACCESS_KEY_ID=your_key"
    echo "export AWS_SECRET_ACCESS_KEY=your_secret"
    exit 1
fi

echo "✅ Credenciais AWS configuradas"
echo "✅ Ambiente virtual ativo"

echo ""
echo "🎓 Chatbot ETE-FMC iniciando..."
echo "📍 Acesse: http://localhost:5000"
echo "🛑 Para parar: Ctrl+C"
echo "=================================="

# Inicia a aplicação
python app.py
