class Unidade:
    def __init__(self, nome):
        self.nome = nome
        self.cursos = []

    def __str__(self):
        return f"Unidade: {self.nome}"

    def add_curso(self, curso):
        self.cursos.append(curso)

    def to_dict(self):
        return {
            "nome": self.nome,
            "cursos": [curso.to_dict() for curso in self.cursos]
        }

class Curso:
    def __init__(self, nome, unidade, duracao_ideal=None, duracao_minima=None, duracao_maxima=None):
        self.nome = nome
        self.unidade = unidade
        self.duracao_ideal = duracao_ideal
        self.duracao_minima = duracao_minima
        self.duracao_maxima = duracao_maxima
        self.disciplinas_obrigatorias = []
        self.disciplinas_optativas_livres = []
        self.disciplinas_optativas_eletivas = []

    def __str__(self):
        return f"Curso: {self.nome} - Unidade: {self.unidade.get_nome()}"

    def add_disciplina_obrigatoria(self, disciplina):
        self.disciplinas_obrigatorias.append(disciplina)

    def add_disciplina_optativa_livre(self, disciplina):
        self.disciplinas_optativas_livres.append(disciplina)

    def add_disciplina_optativa_eletiva(self, disciplina):
        self.disciplinas_optativas_eletivas.append(disciplina)

    def to_dict(self):
        return {
            "nome": self.nome,
            "unidade": self.unidade.nome,
            "duracao_ideal": self.duracao_ideal,
            "duracao_minima": self.duracao_minima,
            "duracao_maxima": self.duracao_maxima,
            "disciplinas_obrigatorias": [d.to_dict() for d in self.disciplinas_obrigatorias],
            "disciplinas_optativas_livres": [d.to_dict() for d in self.disciplinas_optativas_livres],
            "disciplinas_optativas_eletivas": [d.to_dict() for d in self.disciplinas_optativas_eletivas]
        }

class Disciplina:
    def __init__(self, codigo, nome, creditos_aula, creditos_trabalho, carga_horaria,
                 carga_horaria_estagio, carga_horaria_pcc, atividades_tpa):
        self.codigo = codigo
        self.nome = nome
        self.creditos_aula = creditos_aula
        self.creditos_trabalho = creditos_trabalho
        self.carga_horaria = carga_horaria
        self.carga_horaria_estagio = carga_horaria_estagio
        self.carga_horaria_pcc = carga_horaria_pcc
        self.atividades_tpa = atividades_tpa

    def __str__(self):
        return f"Disciplina: {self.codigo} - {self.nome}"

    def to_dict(self):
        return {
            "codigo": self.codigo,
            "nome": self.nome,
            "creditos_aula": self.creditos_aula,
            "creditos_trabalho": self.creditos_trabalho,
            "carga_horaria": self.carga_horaria,
            "carga_horaria_estagio": self.carga_horaria_estagio,
            "carga_horaria_pcc": self.carga_horaria_pcc,
            "atividades_tpa": self.atividades_tpa,
        }
