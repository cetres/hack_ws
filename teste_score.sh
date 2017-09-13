#!/bin/sh
echo "Teste de obtencao de score"
curl http://127.0.0.1:5000/score/82342345623
echo "Teste de avaliacao de acesso"
curl http://127.0.0.1:5000/score/82342345623?acao=dados_segurado
