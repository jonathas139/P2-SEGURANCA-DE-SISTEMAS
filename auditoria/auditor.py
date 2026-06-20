import subprocess
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from blockchain.blockchain import add_block

RELATORIOS_DIR = os.path.join(os.path.dirname(__file__), 'relatorios')

def executar_comando(comando):
    try:
        resultado = subprocess.run(
            comando, shell=True, capture_output=True, text=True, timeout=10
        )
        return resultado.stdout if resultado.stdout else resultado.stderr
    except Exception as e:
        return f"Erro ao executar '{comando}': {e}"

def gerar_relatorio():
    os.makedirs(RELATORIOS_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = os.path.join(RELATORIOS_DIR, f"auditoria_{timestamp}.txt")

    comandos = {
        "Usuarios conectados (who)": "who",
        "Historico de logins (last)": "last -n 20",
        "Portas e servicos em escuta (ss -tulpn)": "ss -tulpn",
        "Interfaces de rede (ip a)": "ip a"
    }

    with open(nome_arquivo, 'w') as f:
        f.write(f"RELATORIO DE AUDITORIA DO SISTEMA\n")
        f.write(f"Gerado em: {datetime.now().isoformat()}\n")
        f.write("=" * 60 + "\n\n")

        for titulo, comando in comandos.items():
            f.write(f"--- {titulo} ---\n")
            saida = executar_comando(comando)
            f.write(saida)
            f.write("\n\n")

    print(f"[AUDITOR] Relatorio gerado: {nome_arquivo}")
    add_block(f"Relatorio de auditoria do sistema gerado: {os.path.basename(nome_arquivo)}")
    return nome_arquivo

if __name__ == "__main__":
    gerar_relatorio()
