#!/bin/sh
curl -X POST -H "Content-Type: application/json" -d @dados2.json http://127.0.0.1:5000/cadastro/82342345623
curl http://127.0.0.1:5000/cadastro/82342345623
