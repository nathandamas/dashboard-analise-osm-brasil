# dashboard.py (versão com correção para o TypeError 'isnan')

import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
import os
import re

# Função auxiliar para limpar os números
def limpar_numero(valor):
    try:
        # Converte para string, remove os pontos e depois converte para float
        return float(str(valor).replace('.', ''))
    except (ValueError, TypeError):
        # Se o valor já for um número ou não puder ser convertido, retorna como está
        return pd.to_numeric(valor, errors='coerce')

st.set_page_config(page_title="Dashboard OSM Brasil", layout="wide")
st.title("Dashboard para Análise Espaço-Temporal do OpenStreetMap no Brasil")


@st.cache_data
def carregar_dados(pasta_dados="data"):
    arquivos_geojson = [f for f in os.listdir(pasta_dados) if f.endswith('.geojson')]
    lista_gdfs_final = []
    cidades_encontradas = []

    for nome_arquivo_geojson in arquivos_geojson:
        nome_cidade_extraido = "desconhecida"
        try:
            match = re.search(r'grade_1km_([a-zA-ZçÇãÃô]+)_4674.geojson', nome_arquivo_geojson, re.IGNORECASE)
            if not match: continue
            nome_cidade_extraido = match.group(1).lower()

            nome_arquivo_csv_esperado = f"resultados_analise_osm_{nome_cidade_extraido}.csv"
            caminho_csv = None
            for f_csv in os.listdir(pasta_dados):
                if f_csv.lower() == nome_arquivo_csv_esperado:
                    caminho_csv = os.path.join(pasta_dados, f_csv)
                    break
            if not caminho_csv: continue

            gdf_base = gpd.read_file(os.path.join(pasta_dados, nome_arquivo_geojson))
            df_metricas = pd.read_csv(caminho_csv, sep=';')
            df_metricas.columns = df_metricas.columns.str.strip()
            
            for col in ['versao_media', 'frequencia_atualizacao_anual']:
                if col in df_metricas.columns:
                    # Aplica a limpeza, mas não mais a conversão para float aqui
                    df_metricas[col] = df_metricas[col].astype(str).str.replace('.', '', regex=False)

            gdf_base['cidade'] = nome_cidade_extraido.capitalize()
            coluna_id_geo = 'ID_UNICO' if 'ID_UNICO' in gdf_base.columns else 'id'
            coluna_id_csv = 'celula_id' if 'celula_id' in df_metricas.columns else 'id'

            gdf_base[coluna_id_geo] = gdf_base[coluna_id_geo].astype(str)
            df_metricas[coluna_id_csv] = df_metricas[coluna_id_csv].astype(str)
            
            gdf_unido = gdf_base.merge(df_metricas, left_on=coluna_id_geo, right_on=coluna_id_csv, how="left")
            gdf_unido.rename(columns={coluna_id_geo: 'id'}, inplace=True)

            lista_gdfs_final.append(gdf_unido)
            cidades_encontradas.append(nome_cidade_extraido.capitalize())
            # st.success(f"Dados para '{nome_cidade_extraido.capitalize()}' carregados.")

        except Exception as e:
            st.error(f"Falha CRÍTICA ao processar '{nome_cidade_extraido.capitalize()}': {e}")
            
    if not lista_gdfs_final:
        return gpd.GeoDataFrame(), []
        
    return pd.concat(lista_gdfs_final, ignore_index=True), sorted(cidades_encontradas)

# --- EXECUÇÃO DO DASHBOARD ---
dados_geo, lista_cidades = carregar_dados()

if not dados_geo.empty:
    st.sidebar.header("Filtros de Visualização")
    if lista_cidades:
        cidade_selecionada = st.sidebar.selectbox("Selecione a Cidade:", lista_cidades)
        METRICAS = {
            "Densidade de Features": "total_features",
            "Número de Colaboradores": "num_colaboradores",
            "Maturidade (Versão Média)": "versao_media",
            "Atualidade (Dias desde a última edição)": "idade_em_dias"
        }
        metrica_selecionada = st.sidebar.selectbox("Selecione a Métrica:", list(METRICAS.keys()))
        coluna_metrica = METRICAS[metrica_selecionada]

        dados_filtrados = dados_geo[dados_geo['cidade'] == cidade_selecionada].copy()
        
        # --- CORREÇÃO FINAL APLICADA AQUI ---
        # Converte a coluna da métrica para numérico de forma segura.
        # Erros de conversão se tornarão 'NaN' (Not a Number)
        dados_filtrados[coluna_metrica] = pd.to_numeric(dados_filtrados[coluna_metrica], errors='coerce')
        
        # Preenche os valores nulos (NaN) com 0 para que o mapa possa renderizá-los
        dados_filtrados.fillna(0, inplace=True)
        
        chave_mapa = 'id'
        
        st.subheader(f"Visualizando: '{metrica_selecionada}' para '{cidade_selecionada}'")

        if not dados_filtrados.empty and 'geometry' in dados_filtrados.columns:
            centro_mapa = [dados_filtrados.geometry.centroid.y.mean(), dados_filtrados.geometry.centroid.x.mean()]
            mapa = folium.Map(location=centro_mapa, zoom_start=11, tiles="OpenStreetMap")
            
            folium.Choropleth(
                geo_data=dados_filtrados,
                data=dados_filtrados,
                columns=[chave_mapa, coluna_metrica],
                key_on=f'feature.properties.{chave_mapa}',
                fill_color='YlOrRd',
                legend_name=f"{metrica_selecionada}"
            ).add_to(mapa)

            st.components.v1.html(mapa._repr_html_(), height=500)