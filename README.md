# Análise da Segurança Operacional na Aviação Civil: Uso de Dados Automatizados para Monitoramento e Prevenção ✈️🤖

Este repositório contém o **Backend (Web API)** do Trabalho de Conclusão de Curso (TCC) para o curso de Tecnologia em Análise e Desenvolvimento de Sistemas do **Instituto Federal do Tocantins (IFTO) - Campus Araguaína**.

O projeto consiste em um sistema inteligente que automatiza a coleta, tratamento e análise de dados de ocorrências aeronáuticas da ANAC, utilizando aprendizado de máquina para identificar padrões de risco.

## 🚀 Funcionalidades Principais

- **ETL Automatizado:** Extração, Transformação e Carga de dados diretamente do portal de Dados Abertos da ANAC.
- **Pipeline Agendado:** O sistema executa o reprocessamento da base de dados diariamente às 02:30 de forma autônoma.
- **Inteligência Artificial:** Aplicação do algoritmo **K-Means** para clusterização de ocorrências e **PCA** para redução de dimensionalidade.
- **API RESTful:** Disponibilização de endpoints para consumo de dados tratados, indicadores (KPIs) e resultados analíticos para o frontend.
- **Monitoramento Espacial:** Filtro geoespacial (Bounding Box) para garantir a precisão dos dados dentro do território brasileiro.

## 🏗️ Arquitetura do Sistema

O projeto foi desenvolvido seguindo os princípios de **Clean Code** e **Arquitetura Limpa**, garantindo a separação de responsabilidades:

1.  **Camada de Serviço (ETL):** Responsável pela lógica de higienização, tratamento de valores nulos e normalização.
2.  **Camada de Rotas (API):** Desenvolvida com **FastAPI** para alta performance e documentação automática.
3.  **Camada de Inteligência:** Processamento matemático via Scikit-Learn.

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.x
- **Framework Web:** [FastAPI](https://fastapi.tiangolo.com/)
- **Manipulação de Dados:** [Pandas](https://pandas.pydata.org/)
- **Machine Learning:** [Scikit-Learn](https://scikit-learn.org/)
- **Servidor ASGI:** Uvicorn
- **Agendamento:** Schedule

## 📁 Estrutura do Projeto

```text
├── app/
│   ├── routers/          # Definição dos endpoints da API
│   ├── services/         # Lógica de negócio e script de ETL
│   └── utils/            # Funções auxiliares
├── main.py               # Ponto de entrada da aplicação e Scheduler
├── requirements.txt      # Dependências do projeto
├── pipeline.log          # Histórico de execução do ETL
└── ocorrencias_tratadas.csv # Base de dados final após processamento
```

## 👨‍💻 Equipe do Projeto

Desenvolvido por:
- Sávio Vitor Alves do Santos
- Victor Manoel de Sousa Ferraz

Sob a orientação de:

- Orientador: Dr. Walisson Pereira de Sousa
- Co-orientadora: Dra. Sabrina Guimarães Paiva

Instituto Federal de Educação, Ciência e Tecnologia do Tocantins (IFTO) - Campus Araguaína, 2026.
