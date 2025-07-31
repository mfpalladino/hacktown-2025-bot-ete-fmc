#!/usr/bin/env python3
"""
Teste do scraper do site ETE-FMC
"""

import sys
import json
from etefmc_scraper import scraper

def test_scraper():
    print("🔍 Testando scraper do site ETE-FMC...")
    print("=" * 50)
    
    try:
        # Testa scraping completo
        print("📡 Fazendo scraping do site https://www.etefmc.com.br/...")
        knowledge_base = scraper.scrape_all()
        
        print("\n✅ Scraping concluído!")
        print(f"📊 Dados coletados:")
        print(f"   - Cursos: {len(knowledge_base.get('cursos', []))}")
        print(f"   - Telefones: {len(knowledge_base.get('contatos', {}).get('telefones', []))}")
        print(f"   - Emails: {len(knowledge_base.get('contatos', {}).get('emails', []))}")
        print(f"   - Notícias: {len(knowledge_base.get('noticias', []))}")
        
        print("\n📋 Informações extraídas:")
        print("-" * 30)
        
        # Mostra cursos
        if knowledge_base.get('cursos'):
            print("🎓 CURSOS:")
            for curso in knowledge_base['cursos']:
                print(f"   • {curso}")
        
        # Mostra contatos
        contatos = knowledge_base.get('contatos', {})
        if contatos.get('telefones'):
            print("\n📞 TELEFONES:")
            for tel in contatos['telefones']:
                print(f"   • {tel}")
        
        if contatos.get('emails'):
            print("\n📧 EMAILS:")
            for email in contatos['emails']:
                print(f"   • {email}")
        
        # Mostra endereço
        if knowledge_base.get('endereco'):
            print(f"\n📍 ENDEREÇO:")
            print(f"   {knowledge_base['endereco']}")
        
        # Mostra horários
        if knowledge_base.get('horarios'):
            print(f"\n⏰ HORÁRIOS:")
            for local, horario in knowledge_base['horarios'].items():
                print(f"   • {local.title()}: {horario}")
        
        # Mostra notícias
        if knowledge_base.get('noticias'):
            print(f"\n📰 NOTÍCIAS RECENTES:")
            for noticia in knowledge_base['noticias'][:3]:
                print(f"   • {noticia['titulo']}")
                print(f"     {noticia['resumo'][:100]}...")
        
        # Mostra sobre
        if knowledge_base.get('sobre'):
            print(f"\n📖 SOBRE A ESCOLA:")
            print(f"   {knowledge_base['sobre'][:200]}...")
        
        print("\n" + "=" * 50)
        print("✅ Teste do scraper concluído com sucesso!")
        
        # Testa busca
        print("\n🔍 Testando busca de informações...")
        test_queries = [
            "Quais cursos vocês oferecem?",
            "Qual o telefone da secretaria?",
            "Qual o horário de funcionamento?",
            "Onde fica a escola?"
        ]
        
        for query in test_queries:
            print(f"\n❓ Pergunta: {query}")
            results = scraper.search_info(query)
            for result in results:
                print(f"   💬 {result}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        print("\n🔄 Testando dados de fallback...")
        fallback_data = scraper.get_fallback_data()
        print(f"✅ Dados de fallback carregados: {len(fallback_data)} seções")
        return False

if __name__ == "__main__":
    success = test_scraper()
    sys.exit(0 if success else 1)
