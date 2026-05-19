from fastapi import APIRouter
from app.services import cluster_service
import pandas as pd

router = APIRouter()

@router.get("/pcacompleto")
def read_root():
    # 1. Processamento dos dados
    df = pd.read_csv("ocorrencias_tratadas.csv")
    dataSet = cluster_service.Padornizador(df)
    amostra = cluster_service.ObterAmostra(dataSet)
    pca_data = cluster_service.ObterPcaData(dataSet)
    pca_data_amostra = cluster_service.ObterPcaDataAmostra(amostra)
    modelo = cluster_service.ObterModeloV1(pca_data_amostra)
    
    # 2. Gera o DataFrame com a coluna 'cluster'
    df_clusters = cluster_service.ObterDfClusters(df, modelo, pca_data)

    # 3. Lógica para definir os nomes humanizados (Igual à rota /mapa)
    nomes_clusters = {}
    for cluster_id in range(4):
        # Filtramos o dataframe pelo cluster atual
        subset = df_clusters[df_clusters['cluster'] == cluster_id]
        
        if not subset.empty:
            # Pegamos a classificação predominante para ajudar na lógica
            classificacao = subset['classificacao_da_ocorrencia'].mode()[0]
            
            if "GRAVE" in classificacao.upper():
                nome_final = "Incidentes de Alto Risco"
            elif cluster_id == 0:
                nome_final = "Ocorrências em Voos de Instrução"
            elif cluster_id == 1:
                nome_final = "Falhas Mecânicas / Motores"
            elif cluster_id == 2:
                nome_final = "Operações em Pista"
            else:
                nome_final = "Eventos de Táxi Aéreo / Agrícola"
            
            nomes_clusters[cluster_id] = nome_final
        else:
            nomes_clusters[cluster_id] = f"Grupo {cluster_id} - Sem Dados"

    # 4. Montagem do retorno (Trocando o ID pelo Nome)
    data_to_send = [
        {
            "pc1": float(row[0]), 
            "pc2": float(row[1]), 
            "cluster": nomes_clusters.get(int(label)) # Enviamos o nome humanizado
        }
        for row, label in zip(pca_data, df_clusters["cluster"])
    ]  

    return data_to_send