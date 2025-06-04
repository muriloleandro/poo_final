from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json
import time
import os
from usp import *
from aux import json2unidade

class Scraper:
    def __init__(self, BASE_URL = "https://uspdigital.usp.br/jupiterweb/jupCarreira.jsp?codmnu=8275", headless = False):
        self.BASE_URL = BASE_URL
        self.unidades = []

        options = Options()
        if headless:
            options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--start-maximized")
            options.add_argument("--disable-setuid-sandbox")
            options.add_argument("--disable-features=site-per-process")
            options.add_argument("--disable-blink-features=AutomationControlled")
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            options.add_argument(f"user-agent={user_agent}")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
        self.driver = webdriver.Chrome(options=options)

    def scrape_tudo(self):
        print("Fazendo scraping das unidades...")
        self.scrape_unidades()

        for i, unidade in enumerate(self.unidades):
            print(f"Fazendo scraping de: {unidade}")

            if not os.path.exists("json/parts/"):
                os.makedirs("json/parts/")

            if os.path.exists(f"json/parts/unidade_{i}.json"):
                print(f"Unidade já processada: json/parts/unidade_{i}.json")
                json2unidade(f"json/parts/unidade_{i}.json", unidade)
                continue

            err = self.scrape_cursos(unidade)
            while err:
                print("ERRO!!!! TENTANDO NOVAMENTE...")
                err = self.scrape_cursos(unidade)

            # salvar como backup
            with open(f"json/parts/unidade_{i}.json", "w", encoding="utf-8") as f:
                json.dump(unidade.to_dict(), f, ensure_ascii=False, indent=4)
            
    def acessar_pag_inicial(self):
        self.driver.get(self.BASE_URL)
        try: 
            WebDriverWait(self.driver, 15).until(
                lambda driver: len(driver.find_elements(By.TAG_NAME, "option"))>2
            )
        except Exception as e:
            print(f"Não acessou nem a página inicial kkkkkk")

    def scrape_unidades(self):
        #acessar url
        self.acessar_pag_inicial()

        # obter lista de unidades pelo dropdown menu
        unidade_dropdown_element = self.driver.find_element(By.ID, "comboUnidade")
        unidade_select = Select(unidade_dropdown_element)
        for option in unidade_select.options:
            nome = option.text
            value = option.get_attribute("value")
            if value == "": continue

            # instanciar e adicionar a lista
            unidade = Unidade(nome)
            self.unidades.append(unidade)

    def scrape_cursos(self, unidade):
        # garantir que está na página
        if self.driver.current_url != self.BASE_URL:
            self.acessar_pag_inicial()

        # seleciona a unidade
        unidade_dropdown = self.driver.find_element(By.ID, "comboUnidade")
        unidade_select = Select(unidade_dropdown)
        unidade_select.select_by_visible_text(unidade.nome)

        curso_dropdown = self.driver.find_element(By.ID, "comboCurso")
        curso_select = Select(curso_dropdown)

        # checar se já carregou os cursos
        try: 
            WebDriverWait(self.driver, 15).until(
                lambda driver: len(curso_dropdown.find_elements(By.TAG_NAME, "option")) > 1
            )
        except Exception as e:
            print(f"Request de cursos demorou ou a unidade está vazia: {unidade.nome}")
            return True

        # salvar 
        for option in curso_select.options:
            nome = option.text
            value = option.get_attribute("value")
            if value == "": continue

            curso_select.select_by_visible_text(nome)

            curso = Curso(nome, unidade)
            unidade.add_curso(curso)
            self.scrape_curso(curso)
        return False

    def scrape_curso(self, curso):
        unidade = curso.unidade
        # garantir que está na página
        if self.driver.current_url != self.BASE_URL:
            self.acessar_pag_inicial()

        # garantir que a unidade corresponde ao já selecionado
        unidade_dropdown = self.driver.find_element(By.ID, "comboUnidade")
        curso_dropdown = self.driver.find_element(By.ID, "comboCurso")
        unidade_select = Select(unidade_dropdown)
        if unidade_select.first_selected_option.text != unidade.nome:
            unidade_select.select_by_visible_text(unidade.nome)
            try: 
                WebDriverWait(self.driver, 15).until(
                    lambda driver: len(curso_dropdown.find_elements(By.TAG_NAME, "option")) > 1
                )
            except Exception as e:
                print(f"Request de cursos demorou ou a unidade está vazia: {unidade.nome}")
                return True

        # garantir que o curso corresponde ao já selecionado
        curso_select = Select(curso_dropdown)
        if curso_select.first_selected_option.text != curso.nome:
            curso_select.select_by_visible_text(curso.nome)

        # acessar a grade
        buscar_button = self.driver.find_element(By.ID, "enviar")
        grade_link = self.driver.find_element(By.ID, "step4-tab")
        grade_tab = grade_link.find_element(By.XPATH, "..")
        buscar_button.click()
        try: 
            WebDriverWait(self.driver, 15).until(
                lambda driver: (
                    not "ui-state-disabled" in grade_tab.get_attribute("class") or
                    len(driver.find_elements(By.ID, "err")) != 0
                )
            )
        except Exception as e:
            print(f"Não conseguiu acessar a grade")
            return True

        if len(self.driver.find_elements(By.ID, "err")) != 0:
            texto_erro = self.driver.find_element(By.ID, "err")
            irmao = texto_erro.find_element(By.XPATH, "following-sibling::*")
            botao_fechar = irmao.find_element(By.TAG_NAME, "button")
            botao_fechar.click()
            return True

        grade_link.click()
        try:
            aguardar_css = ".ui-widget-header.ui-dialog-titlebar.ui-corner-all.blockTitle"
            WebDriverWait(self.driver, 15).until(
                lambda driver: len(driver.find_elements(By.CSS_SELECTOR, aguardar_css)) == 0
            )
        except Exception as e:
            print(f"Não conseguiu carregar a grade")
            return True

        html_completo = self.driver.page_source
        soup = BeautifulSoup(html_completo, "html.parser")

        # obter durações
        duracao_ideal_elements = soup.select(".duridlhab")
        duracao_ideal = duracao_ideal_elements[1].get_text().strip()
        duracao_minima_elem = soup.select_one(".durminhab")
        duracao_minima = duracao_minima_elem.get_text().strip()
        duracao_maxima_elem = soup.select_one(".durmaxhab")
        duracao_maxima = duracao_maxima_elem.get_text().strip()

        curso.duracao_ideal = duracao_ideal
        curso.duracao_minima = duracao_minima
        curso.duracao_maxima = duracao_maxima

        # obter disciplinas
        grades_container = soup.find(id="gradeCurricular")
        grades_tables = grades_container.find_all("table")
        tables = {}
        for table in grades_tables:
            td_cabecalho = table.find("td", style="padding: 5px; font-weight: bold;")
            categoria = td_cabecalho.get_text(strip=True)
            if categoria == "Disciplinas Obrigatórias":
                tables["obrigatoria"] = table
            elif categoria == "Disciplinas Optativas Livres":
                tables["livre"] = table
            elif categoria == "Disciplinas Optativas Eletivas":
                tables["eletiva"] = table

        def processar_disciplinas(tipo, add_disciplina):
            if tipo not in tables.keys(): return
            lista_tr = tables[tipo].find_all("tr")

            lista_tr = [tr for tr in lista_tr if "color" not in tr.get("style")]
            for tr in lista_tr:
                tds = tr.find_all("td")
                codigo = tds[0].find("a").get_text().strip()
                nome                  = tds[1].get_text().strip()
                creditos_aula         = tds[2].get_text().strip()
                creditos_trabalho     = tds[3].get_text().strip()
                carga_horaria         = tds[4].get_text().strip()
                carga_horaria_estagio = tds[5].get_text().strip()
                carga_horaria_pcc     = tds[6].get_text().strip()
                atividades_tpa        = tds[7].get_text().strip()

                disciplina = Disciplina(
                    codigo,
                    nome,
                    creditos_aula,
                    creditos_trabalho,
                    carga_horaria,
                    carga_horaria_estagio,
                    carga_horaria_pcc,
                    atividades_tpa
                )

                add_disciplina(disciplina)

        processar_disciplinas("obrigatoria", curso.add_disciplina_obrigatoria)
        processar_disciplinas("livre", curso.add_disciplina_optativa_livre)
        processar_disciplinas("eletiva", curso.add_disciplina_optativa_eletiva)
        
        # voltar a página de busca
        buscar_link = self.driver.find_element(By.ID, "step1-tab")
        buscar_link.click()
        try: 
            WebDriverWait(self.driver, 15).until(
                lambda driver: "ui-state-disabled" in grade_tab.get_attribute("class")
            )
        except Exception as e:
            print(f"Não conseguiu acessar a busca")
            return True
        
        return False