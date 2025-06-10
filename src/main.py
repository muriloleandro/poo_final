from scraper import Scraper
from usp import *
from sys import argv

def preencher_dados(n_unidades):
    scraper = Scraper(headless=True)
    scraper.scrape_tudo(n_unidades)
    lista_dict = [unidade.to_dict() for unidade in scraper.unidades]
    return scraper.unidades

# 1. Lista de cursos por unidade
def curso_por_unidade(unidades):
    print("\n== Lista de Cursos por Unidade ==")
    print("Unidades disponíveis:")
    for i, unidade in enumerate(unidades):
        print(f"{i} - {unidade.nome}")
    print()

    escolha = -1
    while not (0 <= escolha < len(unidades)):
        res = input("Digite o número da unidade que quer escolher: ")
        if not res.isdigit():
            continue
        escolha = int(res)
    unidade_escolhida = unidades[escolha]
    print(f"Você escolheu: {unidade_escolhida.nome}\n")
    if not unidade_escolhida.cursos:
        print("Esta unidade não possui cursos cadastrados.\n")
        return

    print("Cursos disponíveis nesta unidade:")
    for j, curso in enumerate(unidade_escolhida.cursos):
        print(f"{j} - {curso.nome}")
    print()


# 2. Dados de um determinado curso
def dados_curso(unidades):
    print("\n== Dados de um Curso ==")
    # Primeiro listar unidades para escolha
    print("Unidades disponíveis:")
    for i, unidade in enumerate(unidades):
        print(f"{i} - {unidade.nome}")
    print()

    escolha_un = -1
    while not (0 <= escolha_un < len(unidades)):
        res = input("Digite o número da unidade para escolher: ")
        if not res.isdigit():
            continue
        escolha_un = int(res)
    unidade_escolhida = unidades[escolha_un]

    if not unidade_escolhida.cursos:
        print(f"Unidade {unidade_escolhida.nome} não possui cursos cadastrados.\n")
        return

    # Listar cursos da unidade escolhida
    print(f"\nCursos em {unidade_escolhida.nome}:")
    for j, curso in enumerate(unidade_escolhida.cursos):
        print(f"{j} - {curso.nome}")
    print()

    escolha_c = -1
    while not (0 <= escolha_c < len(unidade_escolhida.cursos)):
        res = input("Digite o número do curso para ver os dados: ")
        if not res.isdigit():
            continue
        escolha_c = int(res)
    curso_escolhido = unidade_escolhida.cursos[escolha_c]

    # Exibir dados do curso selecionado
    print(f"\nDados do curso: {curso_escolhido.nome}")
    print(f"Unidade: {curso_escolhido.unidade.nome}")
    print(f"Duração ideal: {curso_escolhido.duracao_ideal}")
    print(f"Duração mínima: {curso_escolhido.duracao_minima}")
    print(f"Duração máxima: {curso_escolhido.duracao_maxima}\n")

    def listar_disciplinas(titulo, lista):
        if lista:
            print(f"{titulo}:")
            for d in lista:
                print(f"  - {d.codigo} | {d.nome} | Créditos aula: {d.creditos_aula}, "
                      f"Trabalho: {d.creditos_trabalho}, Carga horária: {d.carga_horaria}")
            print()
    listar_disciplinas("Disciplinas Obrigatórias", curso_escolhido.disciplinas_obrigatorias)
    listar_disciplinas("Disciplinas Optativas Livres", curso_escolhido.disciplinas_optativas_livres)
    listar_disciplinas("Disciplinas Optativas Eletivas", curso_escolhido.disciplinas_optativas_eletivas)


# 3. Dados de todos os cursos
def dados_todos_cursos(unidades):
    print("\n== Dados de Todos os Cursos ==")
    for unidade in unidades:
        for curso in unidade.cursos:
            print(f"Curso: {curso.nome} (Unidade: {unidade.nome})")
            print(f"  Duração ideal: {curso.duracao_ideal}, Mínima: {curso.duracao_minima}, Máxima: {curso.duracao_maxima}")
            total_obrig = len(curso.disciplinas_obrigatorias)
            total_opt_livres = len(curso.disciplinas_optativas_livres)
            total_opt_elet = len(curso.disciplinas_optativas_eletivas)
            print(f"  Total de disciplinas obrigatórias: {total_obrig}")
            print(f"  Total de disciplinas optativas livres: {total_opt_livres}")
            print(f"  Total de disciplinas optativas eletivas: {total_opt_elet}")
            print("-" * 50)

    print()


# 4. Dados de uma disciplina, inclusive quais cursos ela faz parte
def dados_disciplina(unidades):
    print("\n== Dados de uma Disciplina ==")
    codigo_busca = input("Digite o código (ou parte do nome) da disciplina que deseja buscar: ").strip().lower()
    encontrados = {}
    disciplina_info = None

    for unidade in unidades:
        for curso in unidade.cursos:
            for lista_d in [
                curso.disciplinas_obrigatorias,
                curso.disciplinas_optativas_livres,
                curso.disciplinas_optativas_eletivas
            ]:
                for d in lista_d:
                    if codigo_busca in d.codigo.lower() or codigo_busca in d.nome.lower():
                        if d.codigo not in encontrados:
                            encontrados[d.codigo] = {
                                "disciplina": d,
                                "cursos": set()
                            }
                        encontrados[d.codigo]["cursos"].add(curso.nome)

    if not encontrados:
        print("Nenhuma disciplina encontrada com esse código ou nome.\n")
        return

    # Se encontrou mais de uma disciplina com o padrão, listar e escolher
    if len(encontrados) > 1:
        print("\nForam encontradas várias disciplinas. Selecione uma delas:")
        for idx, (cod, info) in enumerate(encontrados.items()):
            print(f"{idx} - {cod} | {info['disciplina'].nome}")
        print()

        escolha = -1
        chaves = list(encontrados.keys())
        while not (0 <= escolha < len(chaves)):
            res = input("Digite o número da disciplina desejada: ")
            if not res.isdigit():
                continue
            escolha = int(res)
        chave_selecionada = chaves[escolha]
        disciplina_info = encontrados[chave_selecionada]
    else:
        disciplina_info = next(iter(encontrados.values()))

    d = disciplina_info["disciplina"]
    cursos_que_tem = disciplina_info["cursos"]

    print(f"\nDisciplina: {d.codigo} - {d.nome}")
    print(f"Créditos (aula): {d.creditos_aula}, Trabalho: {d.creditos_trabalho}")
    print(f"Carga horária total: {d.carga_horaria}, Estágio: {d.carga_horaria_estagio}, PCC: {d.carga_horaria_pcc}")
    print(f"Atividades TPA: {d.atividades_tpa}\n")
    print("Esta disciplina faz parte dos cursos:")
    for nome_curso in cursos_que_tem:
        print(f"  - {nome_curso}")
    print()


# 5. Disciplinas que são usadas em mais de um curso
def disciplinas_multiplos_cursos(unidades):
    print("\n== Disciplinas em Múltiplos Cursos ==")
    mapa = {}
    for unidade in unidades:
        for curso in unidade.cursos:
            for lista_d in [
                curso.disciplinas_obrigatorias,
                curso.disciplinas_optativas_livres,
                curso.disciplinas_optativas_eletivas
            ]:
                for d in lista_d:
                    if d.codigo not in mapa:
                        mapa[d.codigo] = {
                            "disciplina": d,
                            "cursos": set()
                        }
                    mapa[d.codigo]["cursos"].add(curso.nome)

    multiplos = {cod: info for cod, info in mapa.items() if len(info["cursos"]) > 1}
    if not multiplos:
        print("Nenhuma disciplina encontrada em mais de um curso.\n")
        return

    for cod, info in multiplos.items():
        d = info["disciplina"]
        cursos_que_tem = info["cursos"]
        print(f"Disciplina: {cod} - {d.nome}")
        print("Cursos:")
        for nome_curso in cursos_que_tem:
            print(f"  - {nome_curso}")
        print("-" * 40)

def mostrar_menu():
    print("===== Menu de Consultas =====")
    print("1 - Lista de cursos por unidade")
    print("2 - Dados de um determinado curso")
    print("3 - Dados de todos os cursos")
    print("4 - Dados de uma disciplina (e cursos que a utilizam)")
    print("5 - Disciplinas que aparecem em mais de um curso")
    print("6 - Sair")


if __name__ == "__main__":
    try:
        n_unidades = int(argv[1])+1 if len(argv)>1 else None;
    except ValueError:
        n_unidades = None;

    unidades = preencher_dados(n_unidades)
    opcoes = {
        1: curso_por_unidade,
        2: dados_curso,
        3: dados_todos_cursos,
        4: dados_disciplina,
        5: disciplinas_multiplos_cursos
    }

    while True:
        mostrar_menu()
        try:
            opcao = int(input("Escolha sua opção (1-6): ").strip())
        except ValueError:
            print("Opção inválida. Tente novamente.")

        if 1<=opcao<=5:
            opcoes[opcao](unidades);
        elif opcao==6:
            print("\nEncerrando o programa. Até mais!")
            break
        else:
            print("Opção inválida. Tente novamente.")
