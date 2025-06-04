import json
from usp import *

def json2unidade(caminho_arquivo, unidade):
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        dados = json.load(f)

    if unidade.nome != dados["nome"]:
        print("Tem algo errado aí!!!")

    for curso_data in dados["cursos"]:
        curso = Curso(
            nome=curso_data["nome"],
            unidade=unidade,
            duracao_ideal=curso_data["duracao_ideal"],
            duracao_minima=curso_data["duracao_minima"],
            duracao_maxima=curso_data["duracao_maxima"]
        )

        for d in curso_data["disciplinas_obrigatorias"]:
            disciplina = Disciplina(**d)
            curso.add_disciplina_obrigatoria(disciplina)

        for d in curso_data["disciplinas_optativas_livres"]:
            disciplina = Disciplina(**d)
            curso.add_disciplina_optativa_livre(disciplina)

        for d in curso_data["disciplinas_optativas_eletivas"]:
            disciplina = Disciplina(**d)
            curso.add_disciplina_optativa_eletiva(disciplina)

        unidade.add_curso(curso)

def jsonlista2unidades(caminho_arquivo):
    lista_unidades = []

    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        dados_lista = json.load(f)

    if not isinstance(dados_lista, list):
        raise TypeError("O arquivo JSON deve conter uma lista de objetos de unidade.")

    for dados_unidade in dados_lista:
        unidade = Unidade(nome=dados_unidade["nome"])

        for curso_data in dados_unidade["cursos"]:
            curso = Curso(
                nome=curso_data["nome"],
                unidade=unidade,
                duracao_ideal=curso_data["duracao_ideal"],
                duracao_minima=curso_data["duracao_minima"],
                duracao_maxima=curso_data["duracao_maxima"]
            )

            for d in curso_data["disciplinas_obrigatorias"]:
                disciplina = Disciplina(**d)
                curso.add_disciplina_obrigatoria(disciplina)

            for d in curso_data["disciplinas_optativas_livres"]:
                disciplina = Disciplina(**d)
                curso.add_disciplina_optativa_livre(disciplina)

            for d in curso_data["disciplinas_optativas_eletivas"]:
                disciplina = Disciplina(**d)
                curso.add_disciplina_optativa_eletiva(disciplina)

            unidade.add_curso(curso)

        lista_unidades.append(unidade)

    return lista_unidades

