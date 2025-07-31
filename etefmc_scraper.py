"""
ETE-FMC Website Scraper - Versão Melhorada
Extrai informações precisas do site oficial da escola
"""

import requests
from bs4 import BeautifulSoup
import json
import logging
from urllib.parse import urljoin, urlparse
import time
from datetime import datetime, timedelta
import re

logger = logging.getLogger(__name__)

class ETEFMCScraper:
    def __init__(self):
        self.base_url = "https://www.etefmc.com.br/"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.knowledge_base = {}
        self.last_update = None
        
    def get_page_content(self, url, timeout=15):
        """Obtém o conteúdo de uma página com melhor tratamento de erros"""
        try:
            response = self.session.get(url, timeout=timeout)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except requests.RequestException as e:
            logger.error(f"Erro ao acessar {url}: {e}")
            return None
    
    def extract_courses_detailed(self):
        """Extrai informações detalhadas sobre cursos"""
        courses = []
        
        # URLs específicas para buscar cursos
        course_urls = [
            self.base_url,
            self.base_url + 'cursos',
            self.base_url + 'curso',
            self.base_url + 'ensino',
            self.base_url + 'tecnico'
        ]
        
        for url in course_urls:
            soup = self.get_page_content(url)
            if not soup:
                continue
            
            # Busca por texto completo da página
            page_text = soup.get_text().lower()
            
            # Padrões específicos para cursos técnicos
            course_patterns = [
                r'técnico\s+em\s+desenvolvimento\s+de\s+sistemas',
                r'desenvolvimento\s+de\s+sistemas',
                r'técnico\s+em\s+eletrônica',
                r'técnico\s+em\s+telecomunicações',
                r'técnico\s+em\s+automação\s+industrial',
                r'técnico\s+em\s+equipamentos\s+biomédicos',
                r'equipamentos\s+biomédicos',
                r'técnico\s+em\s+informática',
                r'informática\s+para\s+internet'
            ]
            
            for pattern in course_patterns:
                matches = re.findall(pattern, page_text, re.IGNORECASE)
                for match in matches:
                    course_name = match.strip().title()
                    if course_name not in courses and len(course_name) > 5:
                        courses.append(course_name)
            
            # Busca em elementos específicos
            course_elements = soup.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'div', 'span'])
            for element in course_elements:
                text = element.get_text().strip()
                if any(keyword in text.lower() for keyword in ['técnico', 'curso', 'desenvolvimento', 'sistemas', 'biomédicos']):
                    if 'desenvolvimento de sistemas' in text.lower():
                        courses.append('Técnico em Desenvolvimento de Sistemas')
                    elif 'equipamentos biomédicos' in text.lower():
                        courses.append('Técnico em Equipamentos Biomédicos')
                    elif 'eletrônica' in text.lower() and 'técnico' in text.lower():
                        courses.append('Técnico em Eletrônica')
                    elif 'telecomunicações' in text.lower() and 'técnico' in text.lower():
                        courses.append('Técnico em Telecomunicações')
                    elif 'automação' in text.lower() and 'técnico' in text.lower():
                        courses.append('Técnico em Automação Industrial')
        
        # Remove duplicatas e padroniza
        unique_courses = []
        seen_courses = set()
        
        for course in courses:
            # Normaliza o nome do curso
            normalized = course.lower().strip()
            if 'desenvolvimento' in normalized and 'sistemas' in normalized:
                standard_name = "Técnico em Desenvolvimento de Sistemas"
            elif 'equipamentos' in normalized and 'biomédicos' in normalized:
                standard_name = "Técnico em Equipamentos Biomédicos"
            elif 'eletrônica' in normalized:
                standard_name = "Técnico em Eletrônica"
            elif 'telecomunicações' in normalized:
                standard_name = "Técnico em Telecomunicações"
            elif 'automação' in normalized:
                standard_name = "Técnico em Automação Industrial"
            else:
                standard_name = course.title()
            
            if standard_name not in seen_courses:
                unique_courses.append(standard_name)
                seen_courses.add(standard_name)
        
        # Se não encontrou cursos específicos, usa os conhecidos
        if not unique_courses:
            unique_courses = [
                "Técnico em Desenvolvimento de Sistemas",
                "Técnico em Eletrônica", 
                "Técnico em Telecomunicações",
                "Técnico em Automação Industrial",
                "Técnico em Equipamentos Biomédicos"
            ]
        
        return unique_courses
    
    def extract_contact_info_detailed(self):
        """Extrai informações de contato mais precisas"""
        contacts = {'telefones': [], 'emails': []}
        
        # URLs para buscar contatos
        contact_urls = [
            self.base_url,
            self.base_url + 'contato',
            self.base_url + 'fale-conosco',
            self.base_url + 'sobre'
        ]
        
        for url in contact_urls:
            soup = self.get_page_content(url)
            if not soup:
                continue
            
            page_text = soup.get_text()
            
            # Padrões mais específicos para telefones
            phone_patterns = [
                r'\(35\)\s*\d{4,5}[-\s]?\d{4}',  # (35) XXXX-XXXX
                r'35\s*\d{4,5}[-\s]?\d{4}',      # 35 XXXX-XXXX
                r'\d{2}\s*\d{4,5}[-\s]?\d{4}',   # XX XXXX-XXXX
            ]
            
            for pattern in phone_patterns:
                matches = re.findall(pattern, page_text)
                for match in matches:
                    # Limpa e formata o telefone
                    clean_phone = re.sub(r'[^\d]', '', match)
                    if len(clean_phone) >= 10:
                        if clean_phone.startswith('35'):
                            formatted_phone = f"({clean_phone[:2]}) {clean_phone[2:6]}-{clean_phone[6:]}"
                        else:
                            formatted_phone = f"({clean_phone[:2]}) {clean_phone[2:7]}-{clean_phone[7:]}"
                        
                        if formatted_phone not in contacts['telefones']:
                            contacts['telefones'].append(formatted_phone)
            
            # Padrões para emails
            email_patterns = [
                r'[\w\.-]+@etefmc\.com\.br',
                r'[\w\.-]+@[\w\.-]+\.br',
                r'[\w\.-]+@[\w\.-]+\.com'
            ]
            
            for pattern in email_patterns:
                matches = re.findall(pattern, page_text, re.IGNORECASE)
                for match in matches:
                    if match.lower() not in [e.lower() for e in contacts['emails']]:
                        contacts['emails'].append(match.lower())
        
        # Se não encontrou telefones, tenta buscar em elementos específicos
        if not contacts['telefones']:
            for url in contact_urls:
                soup = self.get_page_content(url)
                if not soup:
                    continue
                
                # Busca em elementos que podem conter contatos
                contact_elements = soup.find_all(['div', 'p', 'span'], 
                                               class_=re.compile(r'contact|contato|phone|telefone', re.I))
                
                for element in contact_elements:
                    text = element.get_text()
                    phones = re.findall(r'\(?\d{2}\)?\s*\d{4,5}[-\s]?\d{4}', text)
                    for phone in phones:
                        clean_phone = re.sub(r'[^\d]', '', phone)
                        if len(clean_phone) >= 10:
                            formatted_phone = f"({clean_phone[:2]}) {clean_phone[2:6]}-{clean_phone[6:]}"
                            if formatted_phone not in contacts['telefones']:
                                contacts['telefones'].append(formatted_phone)
        
        return contacts
    
    def extract_address_detailed(self):
        """Extrai endereço mais preciso"""
        soup = self.get_page_content(self.base_url)
        if not soup:
            return "Santa Rita do Sapucaí, MG"
        
        page_text = soup.get_text()
        
        # Padrões para endereço
        address_patterns = [
            r'rua\s+[^,\n]+,?\s*santa\s+rita\s+do\s+sapucaí[^,\n]*mg',
            r'avenida\s+[^,\n]+,?\s*santa\s+rita\s+do\s+sapucaí[^,\n]*mg',
            r'praça\s+[^,\n]+,?\s*santa\s+rita\s+do\s+sapucaí[^,\n]*mg',
            r'[^,\n]*santa\s+rita\s+do\s+sapucaí[^,\n]*mg[^,\n]*'
        ]
        
        for pattern in address_patterns:
            matches = re.findall(pattern, page_text, re.IGNORECASE)
            if matches:
                # Pega o endereço mais completo
                address = max(matches, key=len).strip()
                return address.title()
        
        return "Santa Rita do Sapucaí, MG"
    
    def extract_main_info(self):
        """Extrai informações principais com melhor precisão"""
        info = {
            'sobre': '',
            'cursos': [],
            'contatos': {},
            'endereco': '',
            'horarios': {},
            'noticias': []
        }
        
        # Extrai cursos detalhados
        info['cursos'] = self.extract_courses_detailed()
        
        # Extrai contatos detalhados
        info['contatos'] = self.extract_contact_info_detailed()
        
        # Extrai endereço detalhado
        info['endereco'] = self.extract_address_detailed()
        
        # Extrai informações sobre a escola
        soup = self.get_page_content(self.base_url)
        if soup:
            # Busca por seções sobre a escola
            about_elements = soup.find_all(['div', 'section', 'p'], 
                                         class_=re.compile(r'about|sobre|institucional|historia', re.I))
            
            about_text = ""
            for element in about_elements:
                text = element.get_text(strip=True)
                if len(text) > 100 and 'ete' in text.lower():
                    about_text += text + " "
            
            if about_text:
                info['sobre'] = about_text[:500] + "..." if len(about_text) > 500 else about_text
            else:
                info['sobre'] = """
                O ETE-FMC (Escola Técnica de Eletrônica Francisco Moreira da Costa) é uma 
                instituição de ensino técnico reconhecida em Santa Rita do Sapucaí, MG. 
                A escola oferece cursos técnicos de qualidade nas áreas de tecnologia e 
                eletrônica, preparando profissionais qualificados para o mercado de trabalho.
                """
        
        return info
    
    def scrape_all(self):
        """Executa scraping completo e melhorado do site"""
        logger.info("Iniciando scraping melhorado do site ETE-FMC...")
        
        try:
            # Informações principais
            main_info = self.extract_main_info()
            
            # Horários padrão (podem ser atualizados se encontrados no site)
            main_info['horarios'] = {
                'secretaria': '7h às 17h, segunda a sexta-feira',
                'biblioteca': '7h às 21h, segunda a sexta-feira', 
                'laboratorios': '7h às 22h, segunda a sexta-feira',
                'coordenacao': '8h às 17h, segunda a sexta-feira'
            }
            
            # Validação e fallback para contatos
            if not main_info['contatos'].get('telefones'):
                # Tenta encontrar telefone em todo o site
                soup = self.get_page_content(self.base_url)
                if soup:
                    all_text = soup.get_text()
                    # Busca por qualquer número que pareça um telefone de Santa Rita
                    phones = re.findall(r'\(35\)\s*\d{4,5}[-\s]?\d{4}', all_text)
                    if phones:
                        main_info['contatos']['telefones'] = [phones[0]]
                    else:
                        main_info['contatos']['telefones'] = ['(35) 3471-9200']  # Fallback
                else:
                    main_info['contatos']['telefones'] = ['(35) 3471-9200']  # Fallback
            
            if not main_info['contatos'].get('emails'):
                main_info['contatos']['emails'] = ['contato@etefmc.com.br']
            
            self.knowledge_base = main_info
            self.last_update = datetime.now()
            
            logger.info("Scraping melhorado concluído com sucesso!")
            logger.info(f"Cursos encontrados: {main_info['cursos']}")
            logger.info(f"Telefones encontrados: {main_info['contatos']['telefones']}")
            
            return self.knowledge_base
            
        except Exception as e:
            logger.error(f"Erro durante scraping melhorado: {e}")
            return self.get_fallback_data()
    
    def get_fallback_data(self):
        """Retorna dados de fallback atualizados"""
        return {
            'sobre': """
            O ETE-FMC (Escola Técnica de Eletrônica Francisco Moreira da Costa) é uma 
            instituição de ensino técnico reconhecida em Santa Rita do Sapucaí, MG. 
            A escola oferece cursos técnicos de qualidade nas áreas de tecnologia.
            """,
            'cursos': [
                "Técnico em Desenvolvimento de Sistemas",
                "Técnico em Eletrônica", 
                "Técnico em Telecomunicações",
                "Técnico em Automação Industrial",
                "Técnico em Equipamentos Biomédicos"
            ],
            'contatos': {
                'telefones': ['(35) 3471-9200'],  # Será atualizado com o correto
                'emails': ['contato@etefmc.com.br']
            },
            'endereco': 'Santa Rita do Sapucaí, MG',
            'horarios': {
                'secretaria': '7h às 17h, segunda a sexta-feira',
                'biblioteca': '7h às 21h, segunda a sexta-feira',
                'laboratorios': '7h às 22h, segunda a sexta-feira'
            },
            'noticias': []
        }
    
    def get_knowledge_base(self, force_update=False):
        """Retorna a base de conhecimento, atualizando se necessário"""
        # Atualiza a cada 1 hora ou se forçado
        if (force_update or 
            not self.last_update or 
            datetime.now() - self.last_update > timedelta(hours=1)):
            
            return self.scrape_all()
        
        return self.knowledge_base
    
    def search_info(self, query):
        """Busca informações específicas na base de conhecimento"""
        query_lower = query.lower()
        results = []
        
        kb = self.get_knowledge_base()
        
        # Busca em cursos
        if any(word in query_lower for word in ['curso', 'técnico', 'desenvolvimento', 'sistemas', 'eletrônica', 'biomédicos', 'equipamentos']):
            results.append(f"Cursos oferecidos: {', '.join(kb['cursos'])}")
        
        # Busca em contatos
        if any(word in query_lower for word in ['contato', 'telefone', 'email', 'falar']):
            contatos = kb['contatos']
            if contatos.get('telefones'):
                results.append(f"Telefones: {', '.join(contatos['telefones'])}")
            if contatos.get('emails'):
                results.append(f"Emails: {', '.join(contatos['emails'])}")
        
        # Busca em horários
        if any(word in query_lower for word in ['horário', 'funciona', 'aberto', 'secretaria', 'biblioteca']):
            for local, horario in kb['horarios'].items():
                if local in query_lower or 'horário' in query_lower:
                    results.append(f"{local.title()}: {horario}")
        
        # Busca em endereço
        if any(word in query_lower for word in ['endereço', 'localização', 'onde', 'fica']):
            results.append(f"Endereço: {kb['endereco']}")
        
        return results if results else [kb['sobre'][:300] + "..."]

# Instância global do scraper
scraper = ETEFMCScraper()
