import hashlib
import json
import os
import sys
import time
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from blockchain.blockchain import add_block

DOCS_DIR = os.path.join(os.path.dirname(__file__), '../documentos')
HASHES_FILE = os.path.join(os.path.dirname(__file__), '../logs/hashes_referencia.json')

def calcular_hash_arquivo(caminho):
    sha256 = hashlib.sha256()
    with open(caminho, 'rb') as f:
        for bloco in iter(lambda: f.read(4096), b''):
            sha256.update(bloco)
    return sha256.hexdigest()

def carregar_hashes():
    if not os.path.exists(HASHES_FILE):
        return {}
    with open(HASHES_FILE, 'r') as f:
        return json.load(f)

def salvar_hashes(hashes):
    os.makedirs(os.path.dirname(HASHES_FILE), exist_ok=True)
    with open(HASHES_FILE, 'w') as f:
        json.dump(hashes, f, indent=2, ensure_ascii=False)

def escanear_documentos():
    hashes = {}
    os.makedirs(DOCS_DIR, exist_ok=True)
    for arquivo in os.listdir(DOCS_DIR):
        caminho = os.path.join(DOCS_DIR, arquivo)
        if os.path.isfile(caminho):
            hashes[arquivo] = calcular_hash_arquivo(caminho)
    return hashes

def inicializar():
    print("[MONITOR] Inicializando hashes de referência...")
    hashes = escanear_documentos()
    salvar_hashes(hashes)
    add_block(f"Monitor inicializado: {len(hashes)} arquivo(s) indexado(s)")
    print(f"[MONITOR] {len(hashes)} arquivo(s) indexado(s).")

def verificar():
    referencia = carregar_hashes()
    atual = escanear_documentos()
    alertas = []

    for arquivo, hash_ref in referencia.items():
        if arquivo not in atual:
            msg = f"Arquivo EXCLUÍDO: {arquivo}"
            alertas.append(msg)
            add_block(msg)
            print(f"[ALERTA] {msg}")
        elif atual[arquivo] != hash_ref:
            msg = f"Arquivo ALTERADO: {arquivo}"
            alertas.append(msg)
            add_block(msg)
            print(f"[ALERTA] {msg}")

    for arquivo in atual:
        if arquivo not in referencia:
            msg = f"Arquivo NOVO detectado: {arquivo}"
            alertas.append(msg)
            add_block(msg)
            print(f"[ALERTA] {msg}")

    if not alertas:
        print(f"[OK] Todos os arquivos íntegros. ({len(atual)} arquivo(s) verificado(s))")

    return alertas

if __name__ == "__main__":
    inicializar()

    print("\n--- Criando arquivo de teste ---")
    with open(os.path.join(DOCS_DIR, 'teste.txt'), 'w') as f:
        f.write("documento original")

    print("--- Verificando antes da alteração ---")
    inicializar()
    verificar()

    print("\n--- Alterando arquivo ---")
    with open(os.path.join(DOCS_DIR, 'teste.txt'), 'w') as f:
        f.write("documento ALTERADO")

    print("--- Verificando depois da alteração ---")
    verificar()
