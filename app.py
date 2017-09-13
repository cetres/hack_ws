import os
import logging
from flask import Flask, request, jsonify, abort
import yaml
app = Flask(__name__)

DADOS_DIR = "dados"

PARAMS_BOOL = [
    "email_validado",
    "tel_validado"
]


if not os.path.exists(DADOS_DIR):
    os.mkdir(DADOS_DIR)

def get_autorizacao(score, acao):
    arquivo = "parametros.yaml"
    
    app.logger.debug("Lendo arquivo de parametros")
    try:
        with open(arquivo, "r") as p:
            parametros = yaml.load(p)
            app.logger.debug("Arquivo de parametros ok")
            app.logger.debug("Parametros: %s" % parametros)
    except yaml.YAMLError as exc:
        app.logger.critical(exc)
        abort(500) 
    if not "nivel" in parametros:
        app.logger.critical("Niveis nao parametrizados")
        abort(500) 
    if not acao in parametros["nivel"]:
        app.logger.critical("Nivel %s nao cadastrado" % acao)
        abort(500) 
    acao_nivel = parametros["nivel"][acao]
    app.logger.debug("Acao nivel [%s]: %s" % (type(acao_nivel),acao_nivel))
    
    if acao_nivel > score:
        return False
    else:
        return True


def get_score(cpf):
    global PARAMS_BOOL
    arquivo = "parametros.yaml"
    app.logger.debug("Lendo arquivo de parametros")
    try:
        with open(arquivo, "r") as p:
            parametros = yaml.load(p)
            app.logger.debug("Arquivo de parametros ok")
            app.logger.debug("Parametros: %s" % parametros)
    except yaml.YAMLError as exc:
        app.logger.critical(exc)
        abort(500) 

    cadastro = get_cadastro(cpf)

    score_atual = 0
    if "cadastro" in parametros:
        for param_ref in PARAMS_BOOL:
            if not param_ref in parametros["cadastro"]:
                app.logger.error("Parametro %s nao existe nas configuracoes" % (param_ref))
                continue
            if int(cadastro.get(param_ref, 0)) == 1:
                valor = int(parametros["cadastro"][param_ref])
                app.logger.debug("Parametro %s: %d" % (param_ref, valor))
                score_atual += valor            
    else:
        return "Parametros de cadastro nao encontrado"
    app.logger.debug("Score calculado: %s" % score_atual)
    return score_atual

def get_cadastro(cpf):
    global DADOS_DIR
    path = os.path.join(DADOS_DIR, cpf)
    if not os.path.exists(path):
        abort(404)
    try:
        with open(path, "r") as f:
            return yaml.load(f)
    except yaml.YAMLError as exc:
        app.logger.critical(exc)
        abort(500)
    return
        
def post_cadastro(cpf, dados):
    global DADOS_DIR
    parametros = {}
    app.logger.debug("Dados post %s: %s" % (type(dados), dados))
    path = os.path.join(DADOS_DIR, cpf)
    if os.path.exists(path):
        app.logger.debug("Arquivo do cpf %s encontrado. Abrindo..." % cpf)
        try:
            with open(path, "r") as f:
                parametros = yaml.load(f)
                app.logger.debug("Dados CPF %s: %s" % (cpf, parametros))
        except yaml.YAMLError as exc:
            app.logger.critical(exc)
            abort(500)
    else:
        app.logger.debug("Nao encontrado arquivo do cpf %s" % cpf)
    parametros.update(dados)
    try:
        with open(path, "w") as f:
            app.logger.debug("Abrindo arquivo para gravacao do cpf %s" % cpf)
            yaml.dump(parametros, f)
    except yaml.YAMLError as exc:
        app.logger.critical(exc)
        abort(500)
    return ""


@app.route('/cadastro/<cpf>', methods=['GET', 'POST'])
def cadastro(cpf):
    app.logger.debug("Cadastro CPF: %s" % cpf)
    if request.method == 'GET':
        return jsonify(get_cadastro(cpf))
    elif request.method == 'POST':
        return post_cadastro(cpf, request.json)
    return 'opcao invalida'

@app.route('/score/<cpf>', methods=['GET'])
def score(cpf):
    app.logger.debug("Score CPF: %s" % cpf)
    cadastro = get_cadastro(cpf)
    if "acao" in request.args:
        score = get_score(cpf)
        return jsonify(acesso=get_autorizacao(score, request.args.get("acao", cadastro)))
    else:
        return jsonify(score=get_score(cpf))
    
    
@app.errorhandler(404)
def page_not_found(error):
    return '', 404
    
@app.errorhandler(500)
def system_error(error):
    return '', 500