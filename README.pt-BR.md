# 🚙 Uber Expense Analytics

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://uber-expense-analytics.streamlit.app/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)

Uma aplicação web interativa para análise completa de suas despesas com Uber. Visualize gastos, distâncias percorridas, mapas de calor e rotas da sua corrida mais cara.

## 📊 Funcionalidades 

- **📈 Dashboard Interativo**: Visualize métricas principais como total gasto, número de corridas e quilometragem
- **🗓️ Filtros Avançados**: Filtre por ano e tipo de corrida (UberX, Uber Comfort, etc.)
- **📊 Gráficos Dinâmicos**: Acompanhe gastos e km percorridos mês a mês
- **🗺️ Mapa de Calor**: Visualize seus locais de desembarque mais frequentes
- **🚗 Rota da Corrida Mais Cara**: Veja a rota completa da sua viagem mais custosa
- **📥 Export de Dados**: Baixe planilhas com dados filtrados

## 🎯 Como Usar

### 1. Acesse a Aplicação

Visite [uber-expense-analytics.streamlit.app](https://uber-expense-analytics.streamlit.app/)

### 2. Exporte Seus Dados do Uber
<div style="display: flex;">
   <div style="flex: 1; padding: 10px;">
   Para obter seu histórico de viagens do Uber:

   1. **Acesse o site do Uber**
      - Entre em [https://privacy.uber.com/exploreyourdata/](https://privacy.uber.com/exploreyourdata/)
      - Faça login com sua conta

   2. **Navegue até Download**
      - Clique no menu superior
      - Selecione **"Baixar"** ou **"Download"**
      - Clique em **"Baixar seus dados"** ou **"Download your data"**

   3. **Solicite o Export**
      - Marque a opção **"Histórico de viagens"** ou **"Trip history"**
      - Clique em **"Enviar solicitação"** ou **"Submit request"**
      - Aguarde o email de confirmação (pode levar alguns minutos ou até 24h)

   4. **Baixe o Arquivo**
      - Você receberá um email com link para download
      - Baixe o arquivo ZIP
      - Extraia o arquivo `trips_data.csv`
   </div>
<div style="flex: 1; padding: 10px; margin-left: 10px; text-align: center;">
   <img src="img/download_receipt.gif" alt="Download Uber Data" 
         style="max-width: 70%; border: none; outline: none; box-shadow: none;">
</div>
</div>
### 3. Faça Upload na Aplicação

1. Na aplicação, clique no botão **"Browse files"** ou arraste seu arquivo CSV (ex. `trips_data-0.csv`) para a área de upload
2. Aguarde o processamento dos dados
3. Explore os gráficos e métricas no dashboard
4. Use os filtros na barra lateral para personalizar a visualização

## 📸 Screenshots

### Dashboard Principal
O dashboard exibe métricas chave e gráficos interativos de suas despesas.
<img src="img/main_dashboard.png" alt="Main Dashboard" style="max-width: 60%; border: none; outline: none; box-shadow: none;">

### Mapa de Calor
Visualize os locais onde você mais utiliza o Uber através de um mapa de calor interativo.
<img src="img/heatmap.png" alt="Heat Map" style="max-width: 60%; border: none; outline: none; box-shadow: none;">

### Rota da Corrida Mais Cara
Veja o trajeto completo da sua viagem mais custosa com pontos de embarque e desembarque.
<img src="img/route.png" alt="Most Expensive Trip Route" style="max-width: 60%; border: none; outline: none; box-shadow: none;">

## 🛠️ Tecnologias Utilizadas

- **[Streamlit](https://streamlit.io/)**: Framework para criação da aplicação web
- **[Pandas](https://pandas.pydata.org/)**: Manipulação e análise de dados
- **[Plotly](https://plotly.com/)**: Gráficos interativos e mapas
- **[OpenRouteService](https://openrouteservice.org/)**: API para traçar rotas no mapa

## 🚀 Rodando Localmente

### Pré-requisitos

- Python 3.12 ou superior
- Conta no OpenRouteService (para API key)

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/UberExpenseAnalytics.git
cd UberExpenseAnalytics
```

2. Crie um ambiente virtual:
```bash
python -m venv .venv
source .venv/bin/activate  # No Windows: .venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure a API Key:
   - Crie uma conta gratuita em [openrouteservice.org](https://openrouteservice.org/)
   - Obtenha sua API key
   - Crie o arquivo `.streamlit/secrets.toml`:
```toml
ORS_API_KEY="sua_api_key_aqui"
```

5. Execute a aplicação:
```bash
streamlit run app.py
```

A aplicação estará disponível em `http://localhost:8501`

## 📁 Estrutura do Projeto

```
UberExpenseAnalytics/
│
├── app.py                 # Aplicação principal Streamlit
├── data_pipeline.py       # Processamento de dados CSV
├── charts.py              # Funções para gráficos e mapas
├── transform.py           # Transformações de dados (legacy)
├── requirements.txt       # Dependências do projeto
├── LICENSE               # Licença MIT
│
├── .streamlit/
│   └── secrets.toml      # Configurações secretas (API keys)
│
└── .idea/                # Configurações do PyCharm (IDE)
```

## 📊 Formato dos Dados

O arquivo CSV do Uber deve conter as seguintes colunas:
- `request_time`: Data e hora da solicitação
- `status`: Status da corrida (completed, canceled, etc.)
- `fare_amount`: Valor da corrida
- `distance`: Distância percorrida em km
- `product_type`: Tipo de produto (UberX, Uber Comfort, etc.)
- `begintrip_lat`, `begintrip_lng`: Coordenadas de início
- `dropoff_lat`, `dropoff_lng`: Coordenadas de fim
- `begintrip_address`: Endereço de embarque
- `dropoff_address`: Endereço de desembarque

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fazer fork do projeto
2. Criar uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abrir um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👨‍💻 Autor

**Erivelton Junior**

- GitHub: [@erivelton-jr](https://github.com/erivelton-jr)
- LinkedIn: [Erivelton Ribeiro Luz Junior](https://linkedin.com/in/eriveltonjr)

## 🙏 Agradecimentos

- Comunidade Streamlit pela excelente ferramenta
- OpenRouteService pela API de rotas gratuita

## ⚠️ Aviso

Esta aplicação é independente e não é afiliada à Uber Technologies Inc. Use por sua conta e risco. Seus dados são processados localmente e não são armazenados.

---

⭐ Se este projeto foi útil para você, considere dar uma estrela no GitHub!