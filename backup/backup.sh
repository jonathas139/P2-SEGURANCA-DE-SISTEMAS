#!/bin/bash

DATA=$(date +%Y%m%d_%H%M%S)
PROJETO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
ORIGEM="$PROJETO_DIR/documentos"
DESTINO="$PROJETO_DIR/backup"
ARQUIVO_TAR="$DESTINO/backup_$DATA.tar.gz"
ARQUIVO_ENC="$ARQUIVO_TAR.enc"
LOG="$PROJETO_DIR/logs/backup.log"
SENHA="securechain2025backup"

echo "[BACKUP] Iniciando backup em $DATA"

tar -czf "$ARQUIVO_TAR" -C "$ORIGEM" .

if [ $? -ne 0 ]; then
    echo "$(date): FALHOU - erro ao compactar" >> "$LOG"
    echo "[ERRO] Falha na compactacao"
    exit 1
fi

openssl enc -aes-256-cbc -salt -pbkdf2 -in "$ARQUIVO_TAR" -out "$ARQUIVO_ENC" -pass pass:"$SENHA"

if [ $? -ne 0 ]; then
    echo "$(date): FALHOU - erro ao criptografar" >> "$LOG"
    echo "[ERRO] Falha na criptografia"
    exit 1
fi

rm "$ARQUIVO_TAR"

TAMANHO=$(du -h "$ARQUIVO_ENC" | cut -f1)

echo "$(date): SUCESSO - arquivo: $ARQUIVO_ENC - tamanho: $TAMANHO" >> "$LOG"

echo "[BACKUP] Concluido: $ARQUIVO_ENC ($TAMANHO)"

python3 "$HOME/securechain/blockchain/blockchain.py" 2>/dev/null

cd "$PROJETO_DIR" && python3 -c "
import sys
sys.path.insert(0, '.')
from blockchain.blockchain import add_block
add_block('Backup executado: $ARQUIVO_ENC | tamanho: $TAMANHO')
"

echo "[BACKUP] Evento registrado na blockchain"
