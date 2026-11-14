"""
Análise exploratória – Modos de cantonamento da rede ferroviária francesa (SNCF)
Gráficos gerados:
  02 – Famílias tecnológicas: % de trechos vs % da quilometragem
  03 – Top 10 modos de cantonamento por quilometragem
  05 – 10 maiores linhas por quilometragem
Uso: python eda_cantonamento_sncf.py [caminho_csv] [pasta_saida]
"""
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

CSV = sys.argv[1] if len(sys.argv) > 1 else "dados_sncf_sprint3/cantonamento_ferroviario_pt_leve.csv"
OUT = Path(sys.argv[2] if len(sys.argv) > 2 else "graficos_eda")
OUT.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({"figure.dpi": 110, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "grid.alpha": .25, "font.size": 10})


def salvar(nome):
    plt.tight_layout()
    plt.savefig(OUT / nome, bbox_inches="tight")
    plt.close()


# Carga e limpeza: 2 trechos sem extensão são descartados nas análises em km
df = pd.read_csv(CSV, sep=";")
d = df.dropna(subset=["extensao_km"]).copy()
km_total = d.extensao_km.sum()
print(f"{len(df)} trechos, {df.codigo_linha.nunique()} linhas | extensão total mapeada: {km_total:,.0f} km")

# ---------------------------------------------------------------- Gráfico 02
fam = d.groupby("familia_tecnologica").agg(trechos=("id_trecho", "size"), km=("extensao_km", "sum"))
fam["pct_trechos"] = fam.trechos / fam.trechos.sum() * 100
fam["pct_km"] = fam.km / fam.km.sum() * 100
fam = fam.sort_values("km", ascending=False)
print("\nFamílias tecnológicas:\n", fam.round(1).to_string())

fig, ax = plt.subplots(figsize=(9, 4.5))
y = np.arange(len(fam))
ax.barh(y - .2, fam.pct_trechos, .4, label="% dos trechos", color="#8ecae6")
ax.barh(y + .2, fam.pct_km, .4, label="% da quilometragem", color="#023047")
ax.set_yticks(y, fam.index)
ax.invert_yaxis()
ax.set(xlabel="%", title="Famílias tecnológicas: contagem de trechos ≠ quilometragem")
ax.legend()
salvar("02_familias_trechos_vs_km.png")

# ---------------------------------------------------------------- Gráfico 03
modo = d.groupby("modo_cantonamento").agg(trechos=("id_trecho", "size"), km=("extensao_km", "sum"))
modo["pct_km"] = modo.km / km_total * 100
modo = modo.sort_values("km", ascending=False)
print("\nTop 10 modos:\n", modo.head(10).round(1).to_string())

top = modo.head(10).iloc[::-1]
fig, ax = plt.subplots(figsize=(10, 5))
ax.barh(top.index.str.slice(0, 60), top.km, color="#219ebc")
for i, (k, p) in enumerate(zip(top.km, top.pct_km)):
    ax.text(k, i, f" {k:,.0f} km ({p:.1f}%)", va="center", fontsize=8)
ax.set(xlabel="km", title="Top 10 modos por quilometragem")
ax.set_xlim(0, top.km.max() * 1.25)
salvar("03_top_modos_km.png")

# ---------------------------------------------------------------- Gráfico 05
lin = d.groupby(["codigo_linha", "nome_linha"]).agg(trechos=("id_trecho", "size"), km=("extensao_km", "sum"),
                                                    modos=("modo_cantonamento", "nunique")).reset_index()
print("\nTop 10 linhas por km:\n", lin.sort_values("km", ascending=False).head(10).round(1).to_string(index=False))

top_l = lin.sort_values("km", ascending=False).head(10).iloc[::-1]
fig, ax = plt.subplots(figsize=(10, 5))
ax.barh(top_l.nome_linha.str.slice(0, 45), top_l.km, color="#fb8500")
ax.set(xlabel="km", title="10 maiores linhas por quilometragem mapeada")
salvar("05_top_linhas.png")

print(f"\nGráficos salvos em: {OUT.resolve()}")
