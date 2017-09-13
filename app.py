import os
import logging
from flask import Flask, request, jsonify
import yaml
app = Flask(__name__)

PARAMS_BOOL = [
    "email_validado",
    "tel_validado"
]


def do_score(data):
    global PARAMS_BOOL
    arquivo = "parametros.yaml"
    app.logger.debug("Lendo arquivo de parametros")
    try:
        with open(arquivo, "r") as p:
            parametros = yaml.load(p)
            app.logger.debug("Arquivo de parametros ok")
            app.logger.debug(parametros)
    except yaml.YAMLError as exc:
        print(exc)
        return 
    
    score_atual = 0
    if "cadastro" in parametros:
        for param_ref in PARAMS_BOOL:
            if int(data.get(param_ref, 0)) == 1:
                app.logger.debug("Adicionar " + param_ref)
                score_atual += int(parametros["cadastro"][param_ref])
            
    else:
        return "Parametros de cadastro nao encontrado"
    return jsonify(
        score=score_atual
    ) 

@app.route('/score', methods=['GET', 'POST'])
def score():
    if request.method == 'POST':
        return do_score(request.json)
    return 'opcao invalida'