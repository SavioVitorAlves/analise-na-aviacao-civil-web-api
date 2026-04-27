from fastapi import APIRouter
from app.services import cluster_service
import pandas as pd

router = APIRouter()

@router.get("/mapa")
def get_map():
    try:
        dados_pontos = cluster_service.processarDadosMapa()
        df_temp = pd.DataFrame(dados_pontos)
        
        # Carregamos o CSV original para buscar colunas descritivas que podem não estar no mapa
        df_full = pd.read_csv("ocorrencias_tratadas.csv")
        # Garante que o cluster do service seja aplicado ao DF full para análise
        # (Isso assume que a ordem dos dados é mantida ou que você pode mapear pelo índice)
        
        nomes_clusters = {}
        
        for cluster_id in range(4):
            subset = df_temp[df_temp['cluster'] == cluster_id]
            
            if not subset.empty:
                # 1. Buscamos a classificação predominante
                classificacao = subset['classificacao_da_ocorrencia'].mode()[0]
                
                # 2. Lógica de Negócio para Nomes Humanizados
                # Aqui você pode personalizar baseado nas colunas que você sabe que existem
                if "GRAVE" in classificacao.upper():
                    nome_final = "Incidentes de Alto Risco"
                elif cluster_id == 0:
                    nome_final = "Ocorrências em Voos de Instrução"
                elif cluster_id == 1:
                    nome_final = "Falhas Mecânicas / Motores"
                elif cluster_id == 2:
                    nome_final = "Operações em Pista (Pouso/Decolagem)"
                else:
                    nome_final = "Eventos de Táxi Aéreo / Agrícola"
                
                nomes_clusters[cluster_id] = nome_final
            else:
                nomes_clusters[cluster_id] = f"Grupo {cluster_id} - Sem Dados"

        # Atualiza os dados para o front
        for ponto in dados_pontos:
            c_id = ponto.get('cluster')
            ponto['cluster_name'] = nomes_clusters.get(c_id)

        return dados_pontos

    except Exception as e:
        return {"error": str(e)}, 500