# Participação Feminina nos Cursos de Computação do CI/UFPB

Este projeto realiza uma análise exploratória e prospectiva da participação feminina nos cursos de computação do Centro de Informática da Universidade Federal da Paraíba (CI/UFPB), utilizando dados institucionais referentes ao período de 2020 a 2025.

O estudo investiga a evolução da presença feminina nos cursos da área de computação, calcula indicadores de participação por gênero e aplica um modelo de regressão linear simples para projetar cenários futuros de participação feminina.

---

## Objetivos

- Analisar a evolução do número de estudantes por gênero
- Calcular o percentual feminino entre estudantes matriculados
- Identificar tendências temporais da participação feminina
- Projetar cenários futuros para os próximos anos
- Produzir visualizações e tabelas para análise acadêmica

---

## Estrutura do projeto
```
│
├── data
│ ├── input # dados de entrada
│ └── output # resultados gerados
│
├── notebooks # análise exploratória
│ ├── sti_etl.py # scripts em python
│
├── README.md
├── requirements.txt
└── .gitignore
```
---

## Dados de entrada

Os dados devem ser colocados na pasta:


data/input/


Exemplo de arquivo:


dados_ci_ufpb.xlsx


O arquivo deve conter informações institucionais como:

- Ano
- Curso
- Centro
- Gênero
- Ingressantes
- Matriculados
- Trancados
- Cancelados
- Concluintes

---

## Resultados gerados

Os resultados são salvos automaticamente em:


data/output/


Arquivos gerados:

### Tabelas

- resumo_por_ano_e_genero.xlsx
- percentual_feminino.xlsx
- projecao_percentual_feminino.xlsx

### Gráficos

- Evolução de ingressantes por gênero
- Evolução de matriculados por gênero
- Evolução de concluintes por gênero
- Evolução de evasão por gênero
- Percentual feminino ao longo do tempo
- Tendência temporal
- Projeção futura da participação feminina

---

## Metodologia

A análise segue as seguintes etapas:

1. Limpeza e padronização dos dados
2. Filtragem dos cursos de computação do CI/UFPB
3. Agrupamento por ano e gênero
4. Cálculo do percentual feminino entre estudantes matriculados
5. Aplicação de regressão linear simples para identificação de tendência
6. Projeção da participação feminina para os próximos anos

---

## Tecnologias utilizadas

- Python
- Pandas
- NumPy
- Matplotlib
- Google Colab

---

## Como executar

1️⃣ Clone o repositório

```bash
git clone https://github.com/seu-usuario/participacao-feminina-ci-ufpb.git

2️⃣ Instale as dependências

pip install -r requirements.txt

3️⃣ Coloque o arquivo de dados em

data/input/

4️⃣ Execute o script

python notebooks/sti_etl.py
```

## Licença

Projeto desenvolvido para fins acadêmicos e de pesquisa, dentro do projeto HEDY-DATA DO WIEUFPB&MCC.