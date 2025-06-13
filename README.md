## WebScraper do Júpiterweb

**Grupo**:
 - Glauco Fleury Correa de Moraes - 15456302
 - Murilo Leandro Garcia - 15480943
 - Vitor Daniel de Resende - 15554396

### Instalando as bibliotecas

Rode em seu terminal:
```shell
pip install -r requirements.txt
```

### Usando o programa

Rode em seu terminal:
```shell
python src/main.py [número de unidades desejadas]
```

O número de unidades desejadas na execução é opcional, e caso seja
omitido, fará com que o programa obtenha as informações de todas as
unidades.

Ao executar o programa, o usuário deve esperar enquanto o script
navega pelo Júpiterweb obtendo as informações de todos os cursos das
unidades desejadas.

Após o script obter os dados, o usuário deve escolher uma das
seguintes opções de um menu:

1. **Lista de cursos por unidade**: Pede para o usuário escolher uma
  unidade da USP e exibe todos os cursos dessa unidade.
2. **Dados de um determinado curso**: Pede para o usuário escolher uma
  unidade da USP e um curso dessa unidade, e exibe as informações do
  curso escolhido.
3. **Dados de todos os cursos**: Exibe imediatamente as informações de
  todos os cursos obtidos pelo script.
4. **Dados de uma disciplina (e cursos que a utilizam)**: Pede para o
  usuário escolher uma unidade da USP e um curso dessa unidade, e
  exibe as informações de uma disciplina, exibindo também os cursos
  obtidos pelo script nos quais essa disciplina está presente na grade.
5. **Disciplinas que aparecem em mais de um curso**: Exibe
  imediatamente a lista de todas as disciplinas que estão presentes na
  grade de mais de um dos cursos obtidos pelo script.
6. **Sair**: Fecha o programa
