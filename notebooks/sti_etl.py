# =========================================
# NOTEBOOK PARA ETL +  GERAÇÃO DE GRÁFICOS POR GÊNERO
# Participação feminina e masculina nos cursos de computação do CI/UFPB
# =========================================

# =========================================
# 1. IMPORTAR BIBLIOTECAS
# =========================================
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from google.colab import files

# =========================================
# 2. UPLOAD DO ARQUIVO
# =========================================
uploaded = files.upload()
file_name = list(uploaded.keys())[0]
print("Arquivo carregado:", file_name)

# =========================================
# 3. LEITURA DO EXCEL
# =========================================
df = pd.read_excel(file_name)

print("\nColunas encontradas:")
print(df.columns.tolist())

# =========================================
# 4. PADRONIZAÇÃO DAS COLUNAS
# =========================================
df = df.rename(columns={
    "Ano": "Ano",
    "Período": "Periodo",
    "Código Inep": "Codigo_Inep",
    "Curso": "Curso",
    "Turno": "Turno",
    "Centro": "Centro",
    "Classificação": "Genero",
    "Ingressante": "Ingressantes",
    "Matriculado": "Matriculados",
    "Trancado": "Trancados",
    "Cancelado": "Cancelados",
    "Concluído": "Concluintes",
    "Concluído ": "Concluintes"
})

df.columns = df.columns.str.strip()

print("\nColunas após padronização:")
print(df.columns.tolist())

# =========================================
# 5. LIMPEZA BÁSICA
# =========================================
df["Ano"] = pd.to_numeric(df["Ano"], errors="coerce")
df = df.dropna(subset=["Ano"])
df["Ano"] = df["Ano"].astype(int)

df["Genero"] = df["Genero"].astype(str).str.strip().str.upper()

metricas = ["Ingressantes", "Matriculados", "Trancados", "Cancelados", "Concluintes"]
for col in metricas:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

# =========================================
# 6. FILTRAR CENTRO DE INFORMÁTICA
# =========================================
df_ci = df[df["Centro"].astype(str).str.upper() == "CI"].copy()

print("\nQuantidade de linhas do CI:", len(df_ci))
print("\nCursos encontrados no CI:")
print(df_ci["Curso"].dropna().unique())

# =========================================
# 7. FILTRAR CURSOS DE COMPUTAÇÃO
# =========================================
cursos_alvo = [
    "CIÊNCIA DA COMPUTAÇÃO",
    "CIENCIA DA COMPUTACAO",
    "ENGENHARIA DA COMPUTAÇÃO",
    "ENGENHARIA DA COMPUTACAO",
    "CIÊNCIA DE DADOS E INTELIGÊNCIA ARTIFICIAL",
    "CIENCIA DE DADOS E INTELIGENCIA ARTIFICIAL",
    "LICENCIATURA EM COMPUTAÇÃO",
    "LICENCIATURA EM COMPUTACAO"
]

df_ci = df_ci[df_ci["Curso"].astype(str).str.upper().isin(cursos_alvo)].copy()

print("\nCursos filtrados:")
print(df_ci["Curso"].dropna().unique())

print("\nGêneros encontrados:")
print(df_ci["Genero"].dropna().unique())

# =========================================
# 8. AGRUPAR POR ANO E GÊNERO
# =========================================
dados_genero_ano = (
    df_ci.groupby(["Ano", "Genero"])[metricas]
    .sum()
    .reset_index()
)

print("\nResumo por ano e gênero:")
display(dados_genero_ano.head())

# =========================================
# 9. FUNÇÃO PARA GRÁFICOS DE BARRAS POR GÊNERO
# =========================================
def plot_genero_barras(dados, metrica, titulo_grafico, eixo_y, nome_arquivo):
    plt.figure(figsize=(10, 6))

    cores = {
        "F": "#7B2CBF",   # roxo - mulheres
        "M": "#6C757D"    # cinza - homens
    }

    legendas = {
        "F": "Mulheres",
        "M": "Homens"
    }

    anos = sorted(dados["Ano"].unique())
    largura = 0.35
    x = np.arange(len(anos))

    valores_f = []
    valores_m = []

    for ano in anos:
        temp_f = dados[(dados["Ano"] == ano) & (dados["Genero"] == "F")]
        temp_m = dados[(dados["Ano"] == ano) & (dados["Genero"] == "M")]

        valores_f.append(temp_f[metrica].sum() if not temp_f.empty else 0)
        valores_m.append(temp_m[metrica].sum() if not temp_m.empty else 0)

    barras_f = plt.bar(
        x - largura/2,
        valores_f,
        width=largura,
        color=cores["F"],
        label=legendas["F"]
    )

    barras_m = plt.bar(
        x + largura/2,
        valores_m,
        width=largura,
        color=cores["M"],
        label=legendas["M"]
    )

    # valores nas barras
    for barras in [barras_f, barras_m]:
        for barra in barras:
            altura = barra.get_height()
            plt.text(
                barra.get_x() + barra.get_width()/2,
                altura + max(max(valores_f + valores_m) * 0.01, 0.5),
                f"{int(altura)}",
                ha="center",
                va="bottom",
                fontsize=9
            )

    plt.title(titulo_grafico, fontsize=13, weight="bold")
    plt.xlabel("Ano", fontsize=12)
    plt.ylabel(eixo_y, fontsize=12)
    plt.xticks(x, anos, fontsize=11)
    plt.yticks(fontsize=11)
    plt.grid(True, axis="y", linestyle="--", alpha=0.4)
    plt.legend(title="Gênero", fontsize=10, title_fontsize=10)
    plt.tight_layout()
    plt.savefig(nome_arquivo, dpi=300, bbox_inches="tight")
    plt.show()

# =========================================
# 10. FIGURAS PRINCIPAIS POR GÊNERO
# =========================================
plot_genero_barras(
    dados_genero_ano,
    "Ingressantes",
    "Figura 1 – Evolução do número de estudantes ingressantes por gênero nos cursos de computação do CI/UFPB (2020–2025)",
    "Número de estudantes ingressantes",
    "figura_1_ingressantes_genero.png"
)

plot_genero_barras(
    dados_genero_ano,
    "Matriculados",
    "Figura 2 – Evolução do número total de estudantes matriculados por gênero nos cursos de computação do CI/UFPB (2020–2025)",
    "Número de estudantes matriculados",
    "figura_2_matriculados_genero.png"
)

plot_genero_barras(
    dados_genero_ano,
    "Concluintes",
    "Figura 3 – Evolução do número de estudantes concluintes por gênero nos cursos de computação do CI/UFPB (2020–2025)",
    "Número de estudantes concluintes",
    "figura_3_concluintes_genero.png"
)

# Para "desistiram ou evadiram", vamos usar Cancelados + Trancados
dados_genero_ano["Desistentes_Evadidos"] = (
    dados_genero_ano["Cancelados"] + dados_genero_ano["Trancados"]
)

plot_genero_barras(
    dados_genero_ano,
    "Desistentes_Evadidos",
    "Figura 4 – Evolução do número de estudantes que desistiram ou evadiram por gênero nos cursos de computação do CI/UFPB (2020–2025)",
    "Número de estudantes",
    "figura_4_desistentes_evadidos_genero.png"
)

# =========================================
# 11. TABELA PIVOT PARA APOIO À ANÁLISE
# =========================================
tabela_pivot_matriculados = dados_genero_ano.pivot(
    index="Ano",
    columns="Genero",
    values="Matriculados"
).fillna(0)

tabela_pivot_matriculados = tabela_pivot_matriculados.rename(columns={
    "F": "Matriculadas",
    "M": "Matriculados_Homens"
})

print("\nTabela pivot - matriculados por gênero:")
display(tabela_pivot_matriculados)

# =========================================
# 12. PERCENTUAL FEMININO ENTRE MATRICULADOS
# =========================================
tabela_percentual = dados_genero_ano.pivot(
    index="Ano",
    columns="Genero",
    values="Matriculados"
).fillna(0)

if "F" in tabela_percentual.columns and "M" in tabela_percentual.columns:
    tabela_percentual["Total"] = tabela_percentual["F"] + tabela_percentual["M"]
    tabela_percentual["Percentual_Feminino"] = (
        tabela_percentual["F"] / tabela_percentual["Total"] * 100
    ).round(2)

    print("\nPercentual feminino entre matriculados:")
    display(tabela_percentual[["F", "M", "Total", "Percentual_Feminino"]])

    # gráfico percentual feminino em barras
    plt.figure(figsize=(10, 6))
    barras = plt.bar(
        tabela_percentual.index.astype(str),
        tabela_percentual["Percentual_Feminino"],
        color="#7B2CBF"
    )

    for barra in barras:
        altura = barra.get_height()
        plt.text(
            barra.get_x() + barra.get_width()/2,
            altura + 0.5,
            f"{altura:.2f}",
            ha="center",
            va="bottom",
            fontsize=9
        )

    plt.title(
        "Figura 5 – Evolução do percentual feminino entre estudantes matriculados nos cursos de computação do CI/UFPB (2020–2025)",
        fontsize=13,
        weight="bold"
    )
    plt.xlabel("Ano", fontsize=12)
    plt.ylabel("Percentual feminino (%)", fontsize=12)
    plt.ylim(0, 40)
    plt.yticks(np.arange(0, 41, 10), fontsize=11)
    plt.xticks(fontsize=11)
    plt.grid(True, axis="y", linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.savefig("figura_5_percentual_feminino.png", dpi=300, bbox_inches="tight")
    plt.show()

    # =========================================
    # 13. TENDÊNCIA DO PERCENTUAL FEMININO
    # =========================================
    x = tabela_percentual.index.values.astype(int)
    y = tabela_percentual["Percentual_Feminino"].values.astype(float)

    coef = np.polyfit(x, y, 1)
    tendencia = np.poly1d(coef)

    plt.figure(figsize=(10, 6))

    barras = plt.bar(
        x.astype(str),
        y,
        color="#7B2CBF",
        label="Percentual feminino observado"
    )

    # linha de tendência
    plt.plot(
        range(len(x)),
        tendencia(x),
        linestyle="--",
        linewidth=2.2,
        color="#C77DFF",
        marker="o",
        label="Linha de tendência"
    )

    for i, valor in enumerate(y):
        plt.text(
            i,
            valor + 0.5,
            f"{valor:.2f}",
            ha="center",
            va="bottom",
            fontsize=9
        )

    plt.title(
        "Figura 6 – Tendência temporal do percentual feminino entre estudantes matriculados no CI/UFPB",
        fontsize=13,
        weight="bold"
    )
    plt.xlabel("Ano", fontsize=12)
    plt.ylabel("Percentual feminino (%)", fontsize=12)
    plt.ylim(0, 30)
    plt.yticks(np.arange(0, 31, 10), fontsize=11)
    plt.xticks(range(len(x)), x, fontsize=11)
    plt.grid(True, axis="y", linestyle="--", alpha=0.4)
    plt.legend(title="Legenda", fontsize=10, title_fontsize=10)
    plt.tight_layout()
    plt.savefig("figura_6_tendencia_percentual_feminino.png", dpi=300, bbox_inches="tight")
    plt.show()

    print("Equação da tendência percentual feminina:")
    print(tendencia)

    # =========================================
    # 14. PROJEÇÃO DO PERCENTUAL FEMININO
    # =========================================
    anos_futuros = np.arange(x.max() + 1, x.max() + 6)
    previsao = tendencia(anos_futuros)

    df_previsao = pd.DataFrame({
        "Ano": anos_futuros,
        "Percentual_Feminino_Previsto": previsao.round(2)
    })

    print("\nProjeção do percentual feminino:")
    display(df_previsao)

    anos_completos = list(x) + list(anos_futuros)
    valores_completos = list(y) + list(previsao)

    cores_barras = ["#7B2CBF"] * len(y) + ["#C77DFF"] * len(previsao)

    plt.figure(figsize=(10, 6))
    barras = plt.bar(
        [str(ano) for ano in anos_completos],
        valores_completos,
        color=cores_barras
    )

    for barra, valor in zip(barras, valores_completos):
        plt.text(
            barra.get_x() + barra.get_width()/2,
            valor + 0.5,
            f"{valor:.2f}",
            ha="center",
            va="bottom",
            fontsize=9
        )

    plt.title(
        "Figura 7 – Histórico e projeção do percentual feminino entre estudantes matriculados nos cursos de computação do CI/UFPB",
        fontsize=13,
        weight="bold"
    )
    plt.xlabel("Ano", fontsize=12)
    plt.ylabel("Percentual feminino (%)", fontsize=12)
    plt.ylim(0, 30)
    plt.yticks(np.arange(0, 31, 10), fontsize=11)
    plt.xticks(fontsize=11)
    plt.grid(True, axis="y", linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.savefig("figura_7_projecao_percentual_feminino.png", dpi=300, bbox_inches="tight")
    plt.show()

# =========================================
# 15. EXPORTAÇÃO DAS TABELAS
# =========================================
dados_genero_ano.to_excel("resumo_por_ano_e_genero.xlsx", index=False)

if "F" in tabela_percentual.columns and "M" in tabela_percentual.columns:
    tabela_percentual.reset_index().to_excel("percentual_feminino.xlsx", index=False)
    df_previsao.to_excel("projecao_percentual_feminino.xlsx", index=False)

# =========================================
# 16. DOWNLOAD DOS ARQUIVOS
# =========================================
arquivos_para_baixar = [
    "resumo_por_ano_e_genero.xlsx",
    "figura_1_ingressantes_genero.png",
    "figura_2_matriculados_genero.png",
    "figura_3_concluintes_genero.png",
    "figura_4_desistentes_evadidos_genero.png"
]

if "F" in tabela_percentual.columns and "M" in tabela_percentual.columns:
    arquivos_para_baixar.extend([
        "percentual_feminino.xlsx",
        "projecao_percentual_feminino.xlsx",
        "figura_5_percentual_feminino.png",
        "figura_6_tendencia_percentual_feminino.png",
        "figura_7_projecao_percentual_feminino.png"
    ])

for arquivo in arquivos_para_baixar:
    files.download(arquivo)