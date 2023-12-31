﻿# api_parafuzo
<h1 align="center">Controle de Estacionamento API</h1>

<p align="center">Uma API para controle de estacionamento que facilita o registro de entrada, saída e pagamento de veículos.</p>
<p>https://apiparafuzo.up.railway.app/</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue.svg" alt="Python 3.x">
  <img src="https://img.shields.io/badge/Flask-2.0-green.svg" alt="Flask 2.0">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License MIT">
</p>

## Funcionalidades

- **Registro de Entrada de Veículo**: Registre a entrada de veículos com facilidade.
- **Registro de Saída de Veículo**: Registre a saída de veículos, com verificação de pagamento.
- **Registro de Pagamento**: Registre pagamentos para liberar a saída.
- **Histórico por Placa**: Consulte o histórico de registros por placa.

## Tecnologias Utilizadas

- Python
- MongoDB
- Flask (Framework Web)
- JSON (Armazenamento de dados)
- HTML/CSS (Interface do usuário)


## Pré-requisitos

- Python 3.x instalado.
- Flask e outras bibliotecas Python listadas em `requirements.txt`.


## Rotas da API
#### Registro de Entrada de Veículo:

bash

POST /parking
Exemplo de payload:

json
{
  "plate": "FAA-1234",
  "paid": "1"
}

#### Registro de Saída de Veículo:

POST /parking/{vehicle_id}/out
Exemplo de payload:

json
{
  "paid": "1"
}

#### Registro de Pagamento:

PUT /parking/{vehicle_id}/pay

#### Histórico por Placa:

GET /parking/{plate}
