#!/usr/bin/env python3
"""
Teste rápido do servidor Flask
"""

import os
import sys

# Adiciona o diretório atual ao path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from app import app, socketio
    print("✅ Aplicação importada com sucesso!")
    print("🎮 Iniciando ETE-FMC Gaming Bot...")
    print("📍 Acesse: http://localhost:5000")
    print("🛑 Para parar: Ctrl+C")
    
    # Inicia o servidor
    socketio.run(app, debug=False, host='127.0.0.1', port=5000, allow_unsafe_werkzeug=True)
    
except ImportError as e:
    print(f"❌ Erro de importação: {e}")
    print("Verifique se está no ambiente virtual correto")
except Exception as e:
    print(f"❌ Erro geral: {e}")
