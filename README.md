# Modos de cantonamento da rede ferroviária francesa — Análise exploratória

Análise exploratória em Python dos dados de **cantonamento ferroviário** publicados pela SNCF. O projeto compara como a malha francesa controla o espaçamento entre trens, olhando tanto o número de trechos quanto a quilometragem coberta por cada tecnologia.

## Contexto

Dois trens não podem ocupar o mesmo pedaço de trilho. Para garantir isso, a via é dividida em **cantões**, segmentos que só admitem um trem por vez. O **modo de cantonamento** é a tecnologia que aplica essa regra, e vai do telefone entre estações até a sinalização dentro da cabine, usada na alta velocidade. Por isso a variável funciona como um indicador do nível de modernização de cada pedaço da malha.

## Dados

- **Fonte original:** SNCF Open Data — *Mode de cantonnement des lignes* (data.sncf.com)
- **Arquivo analisado:** `cantonamento_ferroviario_pt_leve.csv` (separador `;`, textos traduzidos para português)
- **Documentação das colunas:** `guia-base-cantonamento-ferroviario.pdf`
- **Dimensão:** 1.631 trechos, 795 linhas férreas, 27 colunas
- **Versão "leve":** não inclui a coluna `geo_forma_geojson` (traçado completo), presente apenas no arquivo completo

### Unidade de observação

Cada linha da tabela é um **trecho**, não uma linha férrea. Uma linha costuma mudar de tecnologia ao longo do percurso e por isso é dividida em vários trechos. Contar trechos e somar quilômetros respondem a perguntas diferentes, e as análises deste projeto indicam sempre qual denominador foi usado.

### Principais colunas

| Grupo | Colunas |
|---|---|
| Identificação | `id_trecho`, `codigo_linha`, `nome_linha`, `ordem_trecho` |
| Variável central | `modo_cantonamento` (25 categorias) |
| Agrupamentos | `familia_tecnologica` (7 famílias), `nivel_automacao` (0–4), `tipo_via` |
| Posição e tamanho | `pk_inicial_km`, `pk_final_km`, `extensao_km` |
| Geografia | `latitude_*`, `longitude_*`, coordenadas Lambert-93, `geo_ponto_central` |

## Estrutura do projeto

```
.
├── README.md
├── app.py                              # dashboard Streamlit
├── eda_cantonamento_sncf.py            # script da análise (gera os PNGs)
├── requirements.txt                    # dependências
├── dados_sncf_sprint3/
│   ├── cantonamento_ferroviario_pt_leve.csv
│   └── guia-base-cantonamento-ferroviario.pdf
└── graficos_eda/
    ├── 02_familias_trechos_vs_km.png
    ├── 03_top_modos_km.png
    └── 05_top_linhas.png
```

## Como executar

**Requisitos:** Python 3.9+ e as bibliotecas listadas em `requirements.txt` (`pandas`, `numpy`, `matplotlib` e `streamlit`).

```bash
pip install -r requirements.txt
python eda_cantonamento_sncf.py dados_sncf_sprint3/cantonamento_ferroviario_pt_leve.csv graficos_eda
```

Para abrir o **dashboard interativo** (Streamlit):

```bash
streamlit run app.py
```

O navegador abre em `http://localhost:8501` com as três análises em abas e um controle para escolher quantos itens aparecem nos rankings.

Para gerar apenas os PNGs com o script de linha de comando, use o comando anterior. Os dois argumentos são opcionais: o primeiro é o caminho do CSV e o segundo a pasta de saída dos gráficos. O script imprime no terminal as tabelas que alimentam cada gráfico.

## Tratamento dos dados

- **2 trechos sem extensão nem PK** (linhas urbanas de Paris, com PK em formato alfabético): removidos das análises em km.
- **212 trechos "Outro / não especificado"** (13%): mantidos nas contagens por modo e família.
- **`tipo_via`** só existe quando o nome do modo a menciona, em cerca de 38% dos trechos. Não foi usada nos gráficos.

## Gráficos e principais resultados

Extensão total mapeada: **cerca de 30.600 km**.

### 02 — Famílias tecnológicas: % de trechos vs % de km

O bloco automático domina nas duas medidas (63,9% dos trechos e 58,5% dos km). As diferenças aparecem nas outras famílias: o **bloco manual** é 5,7% dos trechos mas 11,2% dos km, porque seus trechos são longos (mediana de 32,9 km). A **sinalização de cabine** é 5,5% dos trechos e 8,7% dos km.

### 03 — Top 10 modos por quilometragem

O **BAL** (bloco automático luminoso) sozinho cobre 38,1% da extensão. Dos 25 modos existentes, 16 têm menos de 25 trechos.

### 05 — 10 maiores linhas por quilometragem

A maior linha mapeada é Paris-Lyon a Marseille-St-Charles (862 km, um único trecho), seguida de Combs-la-Ville a St-Louis (LGV), com 711 km.

## Limitações

- A extensão é a soma dos trechos cadastrados, e não necessariamente o tamanho físico da rede.
- A versão leve não permite desenhar o traçado das linhas, apenas pontos.
- Os dados são um retrato do cadastro da SNCF na data de publicação, sem dimensão temporal.

## Possíveis próximos passos

- Usar o arquivo completo (com GeoJSON) para mapas com o traçado real.
- Comparar as linhas de alta velocidade (LGV) entre si.
- Cruzar o modo de cantonamento com dados de tráfego ou velocidade, se disponíveis.
