## WebScraper do júpiterweb

### Instalando as bibliotecas

Rode em seu terminal:
```shell
pip install -r requirements.txt
```

### Usando o programa

Rode em seu terminal:
```shell
python src/main.py
```

Você poderá escolher entre fazer o scraping de dados, ou usar os dados já obtidos (para evitar gastar seu tempo e internet).

O scraping de dados salva cada unidade em um arquivo json (`json/parts/unidade_X.json`) para motivos de backup (caso o programa falhe no meio), e posteriormente junta todas um arquivo só (`json/USP.json`). Caso queira refazer o scraping de dados já obtidos, basta apagar os arquivos de unidade.

Após obter os dados, você poderá escolher quais operações quer fazer com esses dados.