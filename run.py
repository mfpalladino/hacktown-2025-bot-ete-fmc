#!/usr/bin/env python3
"""
Script de inicialização do Chatbot ETE-FMC
"""

import os
import sys
import subprocess

def check_requirements():
    """Verifica se as dependências estão instaladas"""
    try:
        import flask
        import flask_socketio
        import boto3
        print("✅ Dependências instaladas")
        return True
    except ImportError as e:
        print(f"❌ Dependência faltando: {e}")
        return False

def check_aws_credentials():
    """Verifica se as credenciais AWS estão configuradas"""
    aws_keys = ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY']
    missing_keys = [key for key in aws_keys if not os.environ.get(key)]
    
    if missing_keys:
        print(f"❌ Credenciais AWS faltando: {', '.join(missing_keys)}")
        print("Configure as variáveis de ambiente:")
        for key in missing_keys:
            print(f"export {key}=your_value_here")
        return False
    
    print("✅ Credenciais AWS configuradas")
    return True

def install_requirements():
    """Instala as dependências"""
    print("📦 Instalando dependências...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependências instaladas com sucesso")
        return True
    except subprocess.CalledProcessError:
        print("❌ Erro ao instalar dependências")
        return False

def main():
    print("🚀 Iniciando Chatbot ETE-FMC")
    print("=" * 50)
    
    # Verifica dependências
    if not check_requirements():
        if input("Instalar dependências? (y/n): ").lower() == 'y':
            if not install_requirements():
                sys.exit(1)
        else:
            sys.exit(1)
    
    # Verifica credenciais AWS
    if not check_aws_credentials():
        sys.exit(1)
    
    print("\n🎓 Chatbot ETE-FMC iniciando...")
    print("📍 Acesse: http://localhost:5000")
    print("🛑 Para parar: Ctrl+C")
    print("=" * 50)
    
    # Inicia a aplicação
    from app import socketio, app
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)

if __name__ == "__main__":
    main()
