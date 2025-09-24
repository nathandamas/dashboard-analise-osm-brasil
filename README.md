# Dashboard para Análise Espaço-Temporal do OpenStreetMap no Brasil

Protótipo de dashboard interativo desenvolvido como parte de uma pesquisa para o SOTM Brasil 2025. A ferramenta permite a visualização e análise da distribuição espaço-temporal das contribuições ao OpenStreetMap (OSM) em cidades brasileiras.

Acesse o dashboard por este linik: **https://dashboard-osm-brasil.streamlit.app/**

## Objetivo do Projeto

O objetivo principal deste trabalho é desenvolver um dashboard web que permita visualizar métricas de completude, qualidade e atualidade dos dados OSM através das células da Grade Estatística, integrando indicadores demográficos e econômicos como preditores de qualidade, possibilitando o planejamento informado de atividades e campanhas de mapeamento, com foco em áreas de interesse ecológico e cultural.

## Metodologia

A análise é fundamentada em uma abordagem de avaliação intrínseca da qualidade dos dados, inspirada na metodologia de Minghini et al. (2018). As métricas de qualidade e atividade são agregadas utilizando a Grade Estatística do IBGE como unidade de análise espacial.

As principais métricas visualizadas são:
* **Densidade de Features:** Número total de elementos mapeados.
* **Número de Colaboradores:** Quantidade de usuários únicos que editaram na área.
* **Maturidade (Versão Média):** Média de versões dos elementos, indicando o nível de revisão.
* **Atualidade:** Tempo decorrido desde a última edição na área.

## Como Executar o Dashboard Localmente

1.  **Clone o repositório:**
    `git clone https://www.youtube.com/watch?v=GRf6so_sois`
2.  **Crie e ative um ambiente Conda:**
    `conda create --name sotm_dashboard python=3.9`
    `conda activate sotm_dashboard`
3.  **Instale as dependências:**
    `pip install -r requirements.txt`
4.  **Execute o Streamlit:**
    `streamlit run dashboard.py`

## Dicionário de Dados

Os dados consolidados utilizados neste dashboard podem ser encontrados em: https://doi.org/10.5281/zenodo.17114782.

| Coluna | Descrição |
|---|---|
| `id` | Identificador único da célula da grade. |
| `geometry` | Forma geométrica (polígono) da célula. |
| `cidade` | Nome da cidade a que a célula pertence. |
| `total_features` | Número total de elementos OSM com tags na célula. |
| `num_colaboradores` | Número de colaboradores únicos que editaram na célula. |
| `versao_media`| Média do número de versões por elemento na célula. |
| `idade_em_dias`| Número de dias entre a data atual e a última edição na célula. |
| `data_ultima_edicao` | Data da edição mais recente registrada na célula. |

## Citação

[Damas Antonio, N., Nasr Naim Elias, E., Andrade, F., Miranda Nunes, D., & Camboim, S. (2025). DATASET DO DASHBOARD PARA ANÁLISE ESPAÇO-TEMPORAL DAS EDIÇÕES DO OPENSTREETMAP NO BRASIL [Data set]. Zenodo. https://doi.org/10.5281/zenodo.17114782]
