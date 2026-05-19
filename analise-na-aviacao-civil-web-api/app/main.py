import asyncio
import threading
import schedule
import time
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from app.services.etl_service import executar_pipeline
from app.routers import analises
from app.routers import pcaAmostra
from app.routers import pcaCompleto
from app.routers import clusterPorRegiao
from app.routers import corelacaoVariaveisNumericas
from app.routers import ocorenciasRegiaoCluster
from app.routers import mapa

# Função que mantém o agendamento rodando em background
def run_scheduler():
    # Agenda a tarefa
    schedule.every().day.at("02:30").do(executar_pipeline)
    # Executa a primeira vez ao iniciar
    executar_pipeline()
    
    while True:
        schedule.run_pending()
        time.sleep(60)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- CÓDIGO DE INICIALIZAÇÃO ---
    # Inicia o agendador em uma thread separada para não bloquear a API
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    
    yield
    
    # --- CÓDIGO DE ENCERRAMENTO ---
    # Aqui você poderia fechar conexões com banco de dados, etc.

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, substitua por "http://localhost:5173"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registra as rotas
app.include_router(analises.router)

app.include_router(pcaAmostra.router)
app.include_router(pcaCompleto.router)
app.include_router(clusterPorRegiao.router)
app.include_router(corelacaoVariaveisNumericas.router)
app.include_router(ocorenciasRegiaoCluster.router)
app.include_router(mapa.router)
#comando para doda o sistema: uvicorn app.main:app --reload
#usar o cd para entrar no diretorio caso nessesario 2 vezes