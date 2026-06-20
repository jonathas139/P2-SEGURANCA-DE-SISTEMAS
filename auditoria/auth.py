import hashlib
import json
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from blockchain.blockchain import add_block

USUARIOS_FILE = os.path.join(os.path.dirname(__file__), '../usuarios/usuarios.json')

def carregar_usuarios():
    if not os.path.exists(USUARIOS_FILE):
        return {}
    with open(USUARIOS_FILE, 'r') as f:
        return json.load(f)

def salvar_usuarios(usuarios):
    os.makedirs(os.path.dirname(USUARIOS_FILE), exist_ok=True)
    with open(USUARIOS_FILE, 'w') as f:
        json.dump(usuarios, f, indent=2, ensure_ascii=False)

def hash_senha(senha):
    salt = "securechain2025"
    return hashlib.sha256((senha + salt).encode()).hexdigest()

def cadastrar_usuario(nome, senha, perfil):
    perfis_validos = ['admin', 'analista', 'visitante']
    if perfil not in perfis_validos:
        print(f"[ERRO] Perfil inválido. Use: {perfis_validos}")
        return False
    usuarios = carregar_usuarios()
    if nome in usuarios:
        print(f"[ERRO] Usuário '{nome}' já existe.")
        return False
    usuarios[nome] = {
        "senha_hash": hash_senha(senha),
        "perfil": perfil,
        "criado_em": datetime.now().isoformat()
    }
    salvar_usuarios(usuarios)
    add_block(f"Usuário criado: {nome} | perfil: {perfil}")
    print(f"[OK] Usuário '{nome}' cadastrado com perfil '{perfil}'.")
    return True

def login(nome, senha):
    usuarios = carregar_usuarios()
    if nome not in usuarios:
        add_block(f"Tentativa de login falhou: usuário '{nome}' não existe")
        print("[ERRO] Usuário não encontrado.")
        return None
    if usuarios[nome]['senha_hash'] != hash_senha(senha):
        add_block(f"Tentativa de login falhou: senha incorreta para '{nome}'")
        print("[ERRO] Senha incorreta.")
        return None
    add_block(f"Login realizado: {nome} | perfil: {usuarios[nome]['perfil']}")
    print(f"[OK] Login bem-sucedido. Perfil: {usuarios[nome]['perfil']}")
    return usuarios[nome]['perfil']

if __name__ == "__main__":
    cadastrar_usuario("admin", "senha123", "admin")
    cadastrar_usuario("ana", "ana456", "analista")
    cadastrar_usuario("visita", "vis789", "visitante")
    print("\n--- Testando login ---")
    login("admin", "senha123")
    login("ana", "senha_errada")
    login("naoexiste", "abc")
