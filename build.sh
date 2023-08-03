#!/usr/bin/env bash

# sai do script se algum comando falhar
set -o errexit

# atualiza o pip
/opt/render/project/src/.venv/bin/python3.9 -m pip install --upgrade pip

# Instala as dependências do projeto
pip install -r requirements.txt

# Coleta os arquivos estáticos em um único diretório
python manage.py collectstatic --no-input

# Executa as migrações
python manage.py migrate