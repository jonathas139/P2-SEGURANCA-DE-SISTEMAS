import hashlib
import json
import os
from datetime import datetime

CHAIN_FILE = os.path.join(os.path.dirname(__file__), "chain.json")

def calcular_hash(bloco):
    conteudo = f"{bloco['id']}{bloco['timestamp']}{bloco['evento']}{bloco['hash_anterior']}"
    return hashlib.sha256(conteudo.encode()).hexdigest()

def carregar_chain():
    if not os.path.exists(CHAIN_FILE):
        return []
    with open(CHAIN_FILE, "r") as f:
        return json.load(f)

def salvar_chain(chain):
    with open(CHAIN_FILE, "w") as f:
        json.dump(chain, f, indent=2, ensure_ascii=False)

def add_block(evento):
    chain = carregar_chain()
    hash_anterior = chain[-1]["hash_atual"] if chain else "0" * 64
    bloco = {
        "id": len(chain) + 1,
        "timestamp": datetime.now().isoformat(),
        "evento": evento,
        "hash_anterior": hash_anterior,
        "hash_atual": ""
    }
    bloco["hash_atual"] = calcular_hash(bloco)
    chain.append(bloco)
    salvar_chain(chain)
    print(f"[BLOCKCHAIN] Bloco #{bloco['id']} registrado: {evento}")
    return bloco

def validar_chain():
    chain = carregar_chain()
    if not chain:
        print("[VALIDAÇÃO] Blockchain vazia.")
        return True
    for i, bloco in enumerate(chain):
        hash_recalculado = calcular_hash(bloco)
        if hash_recalculado != bloco["hash_atual"]:
            print(f"[ALERTA] Bloco #{bloco['id']} CORROMPIDO — hash inválido!")
            return False
        if i > 0:
            if bloco["hash_anterior"] != chain[i-1]["hash_atual"]:
                print(f"[ALERTA] Bloco #{bloco['id']} CORROMPIDO — encadeamento quebrado!")
                return False
    print(f"[VALIDAÇÃO] Blockchain íntegra. {len(chain)} bloco(s) verificado(s).")
    return True

if __name__ == "__main__":
    add_block("Sistema iniciado")
    add_block("Teste de registro de evento")
    validar_chain()
