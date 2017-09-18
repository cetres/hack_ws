#!/usr/bin/env python

import os
import random
from datetime import timedelta, datetime
import yaml

email_providers = ["gmail.com", "hotmail.com", "yahoo.com"]
nomes = []
with open("nomes.txt") as f:
  for n in f.readlines():
    nomes.append(n[:-1])

int_delta = (80 * 365 * 24 * 60 * 60)

for i in range(1000):
    nome1 = nomes[int(random.random()*len(nomes))]
    nome2 = nomes[int(random.random()*len(nomes))]
    random_second = random.randrange(int_delta)
    cliente = {
        "nome": "%s %s" % (nome1, nome2),
        "email": "%s%s@%s" % (nome1[0].lower(),nome2.lower(),email_providers[int(random.random()*len(email_providers))]),
        "tel": str(10000000000*random.random())[:8],
        "email_validado": 1 if random.random() > 0.75 else 0,
        "tel_validado": 1 if random.random() > 0.6 else 0,
        "dt_nascimento": (datetime.now() - timedelta(seconds=random_second)).strftime("%d/%m/%Y"),
        "tel_correlacao_crivo": 1 if random.random() > 0.90 else 0,
        "fraude": 0
    }
    if random.random() > 0.75:
        if cliente["email_validado"] == 0 and cliente["tel_correlacao_crivo"] == 0 and cliente["email"].endswith("hotmail.com"):
            cliente["fraude"] = 1
        
    cpf = str(1000000000000*random.random())[:11]

    with open(os.path.join("dados", cpf), "w") as f:
        yaml.dump(cliente, f)
    
    print(cliente)
