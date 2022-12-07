# Truckpad 

Este repositório contém a API solicitada para o teste de código da Truckpad

## Instalação

Este reposítório utiliza o `pyenv`. Execute o comando abaixo para ativá-lo:

```bash
$ source .venv/bin/activate
```

Após a ativação, instale os pacotes listados em `requirements.txt`

```bash
$ pip install -r requirements.txt
```

### Rodando o projeto

Para rodar o projeto basta utilizar o `unicorv`:

```bash
uvicorn truckpad.app:app
```

## Testes

Para executar os testes, execute o comando `pytest`:

```bash
$ pytest tests/test_app.py
```

### Coverage

Para validar a cobertura de testes, basta passar os parametros abaixo para o `pytest`:

```bash
$ pytest --cov=truckpad --cov-report=term-missing tests/test_app.py
```

## Modelos de dados

### Driver

Para armazenar os dados do motorista, basta seguir a estrutura do `JSON` abaixo:

```json
{
  "_id": {
    "$oid": "F0123456789ABCDEF0123456"
  },
  "name": "Fulano",
  "age": 40,
  "gender": "male",
  "has_vehicle": true,
  "license_type": "C",
  "is_loaded": true,
  "vehicle_type": 3
}
```
### Terminal

Os dados de chegada dos terminais segue o formato do `JSON` abaixo

```json
{
  "arrived_at": {
    "$date": "2022-11-30T13:22:57"
  },
  "origin": {
    "latitude": -12.977749,
    "longitude": -38.501629
  },
  "destination": {
    "latitude": 0.035574,
    "longitude": -51.070534
  },
  "driver": {
    "$oid": "B0123456789ABCDEF0123456"
  }
}
```

No caso dos campos `origin` e `destination`, caso o caminhão entre ou saia do terminal sem carga, basta colocar o valor deles como `false`

## Endpoints

### GET `/driver`

Retorna um array com a listagem de todos os motoristas cadastrados

### POST `/driver`

Cria um novo motorista. Os dados devem ser enviados como um `JSON` no body do request

### GET `/driver/truck`

Retorna um array de todos os motoristas que possuem veículo próprio

### GET `/driver/unloaded`

Retorna um array de todos os motoristas que não possuem carga na entrada ou saída

### GET `/driver/{oid}`

Retorna os dados de um motorista identificado pelo `oid` na URL

### PATCH `/driver/{oid}`

Altera os dados do motorista identificado pelo `oid` na URL

### GET `/terminal`

Retorna um array com todos os registros de entrada/saída dos motoristas que passaram pelo terminal

### POST `/terminal`

Cria um novo registro de entrada/saída de caminhão no terminal 

### GET `/driver/trucklist`

Retorna todos os registros do terminal agrupados pelo tipo de veículo, conforme o exemplo abaixo:

```
{
  "<CÓDIGO VEÍCULO>": [
    { <MODEL TERMINAL 1> },
    { <MODEL TERMINAL 2> },
    { <MODEL TERMINAL 3> },
    ...
    { <MODEL TERMINAL N> },
  ]
}
```

### GET `/terminal/stats`

Retorna um objeto com a contagem de todas as entradas/saidas agrupadas por mês, semana e dia, conforme o exemplo abaixo:

```json
{
  "days": [
    { "_id": "2022-11-25", "total": 1 },
    { "_id": "2022-11-30", "total": 1 },
    { "_id": "2022-12-6", "total": 5 }
  ],
  "weeks": [
    { "_id": "2022-47", "total": 1 },
    { "_id": "2022-48", "total": 1 },
    { "_id": "2022-49", "total": 5 }
  ],
  "months": [
    { "_id": "2022-11", "total": 2 },
    { "_id": "2022-12", "total": 5 }
  ]
}
```
## Considerações

Considerando o escopo do exercício e a minha falta de familiaridade com o Python, algunas coisas que gostaria de ter adicionado/feito diferente:

1. **Nomes**: O Endpoint `/terminal` não me agradou muito, mas preferi manter dessa forma pois essa nomenclatura seria melhor discutida em grupo na hora do planejamento dele

1. **Validaçao**: Não sei se existe um modulo preferido para isso, mas gostaria de ter implementado uma validação nos endpoints. Particularmente acho que uma validação no MongoDB utilizando JSON SCHEMA é um conceito que me agrada bastante

1. **MongoDB**: Certas peculiaridades do monho acabaram tomando bastante tempo, creio que para esse teste teria sido mais sensato começar com um banco de dados mais tradicional. Os `agreggations` embora bastante parecidos com o Elastic/Kibana acabaram ficando bem grandes, creio não ter utilizá-los da melhor forma 

1. **Testes**: Embora os testes estejam rápidos e completos, creio que vários deles poderiam ter sido melhor codificados. Um refactor com certeza seria algo no meu radar
