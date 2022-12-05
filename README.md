# Truckpad 

[[TOC]]


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
