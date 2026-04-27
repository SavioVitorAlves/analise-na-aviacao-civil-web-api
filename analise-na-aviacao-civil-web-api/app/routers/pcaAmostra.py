from fastapi import APIRouter
from app.services import cluster_service
from sklearn.model_selection import train_test_split # Import necessário para replicar a amostra
import pandas as pd

router = APIRouter()

@router.get("/pcaamostra")
def read_root():
    # 1. Carga e Padronização
    df = pd.read_csv("ocorrencias_tratadas.csv")
    dataSet = cluster_service.Padornizador(df)
    
    # 2. Gerar a Amostra (IMPORTANTE: Usar o mesmo random_state do service)
    # Como o seu service usa train_test_split com random_state=42, fazemos o mesmo no DF original
    # para que as linhas do DF batam com as linhas do dataSet amostrado.
    df_amostra, _ = train_test_split(df, train_size=0.10, random_state=42)
    amostra_padronizada = cluster_service.ObterAmostra(dataSet)
    
    # 3. PCA e Modelo na Amostra
    pca_data_amostra = cluster_service.ObterPcaDataAmostra(amostra_padronizada)
    modelo_v1 = cluster_service.ObterModeloV1(pca_data_amostra)
    
    # Adicionamos os labels de cluster ao nosso DataFrame de amostra
    df_amostra = df_amostra.copy()
    df_amostra['cluster'] = modelo_v1.labels_

    # 4. Lógica de Nomes Humanizados (Consistente com /mapa e /pcacompleto)
    nomes_clusters = {}
    for cluster_id in range(4):
        subset = df_amostra[df_amostra['cluster'] == cluster_id]
        
        if not subset.empty:
            # Pegamos a classificação predominante na amostra
            classificacao = subset['classificacao_da_ocorrencia'].mode()[0]
            
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

    # 5. Montagem do retorno
    data_to_send = [
        {
            "pc1": float(row[0]), 
            "pc2": float(row[1]), 
            "cluster": nomes_clusters.get(int(label))
        }
        for row, label in zip(pca_data_amostra, modelo_v1.labels_)
    ]  
    
    return data_to_send