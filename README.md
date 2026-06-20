# SecureChain Audit

Plataforma de auditoria baseada em blockchain para monitoramento de integridade de arquivos, controle de acesso e backup seguro, desenvolvida para a disciplina de Segurança de Sistemas.

## Visão Geral

O SecureChain Audit integra controle de usuários no sistema operacional, autenticação com senhas protegidas por hash, monitoramento de integridade de arquivos, uma blockchain própria para registro imutável de eventos, backup criptografado e auditoria automatizada do sistema operacional.

## Tecnologias

- **Sistema Operacional:** Linux Debian 13
- **Linguagem:** Python 3
- **Automação:** Bash Script
- **Controle de versão:** Git

## Estrutura de Diretórios

```
P2-SEGURANCA-DE-SISTEMAS/
├── blockchain/
│   ├── blockchain.py        # criação de blocos e validação da cadeia
│   └── chain.json           # persistência da blockchain (gerado automaticamente)
├── auditoria/
│   ├── auth.py               # cadastro de usuários e login
│   ├── monitor.py            # monitoramento de integridade de arquivos
│   ├── auditor.py            # coleta de dados do sistema (who, last, ss, ip a)
│   └── relatorios/           # relatórios gerados automaticamente
├── backup/
│   └── backup.sh              # compactação, criptografia e log de backup
├── logs/                      # hashes de referência e log de backup
├── documentos/                # arquivos monitorados pela integridade
├── usuarios/                  # dados de usuários (senhas em hash)
└── README.md
```

## Controle de Acesso (RF01)

Foram criados três usuários no Debian 13, todos pertencentes ao grupo `securechain`, aplicando o princípio do menor privilégio:

| Usuário | Função | Permissões |
|---|---|---|
| `administrador` | Dono do projeto, acesso total | `rwx` em todo o diretório do projeto |
| `analista` | Executa e lê os módulos | `r-x` em `auditoria/` e `blockchain/` |
| `visitante` | Consulta apenas relatórios | `r-x` somente em `auditoria/relatorios/` |

Permissões aplicadas via `chmod`, `chown` e ACLs (`setfacl`), garantindo segregação de funções: nenhum usuário além do `administrador` pode alterar código, configurações ou a blockchain.

Comandos usados:
```bash
sudo groupadd securechain
sudo useradd -m -G securechain -s /bin/bash administrador
sudo useradd -m -G securechain -s /bin/bash analista
sudo useradd -m -G securechain -s /bin/bash visitante

sudo chown -R administrador:securechain .
sudo chmod -R 750 .

sudo setfacl -R -m u:visitante:rx auditoria/relatorios
sudo setfacl -R -m u:analista:rx auditoria
sudo setfacl -R -m u:analista:rx blockchain
```

## Como Executar

Todos os comandos abaixo devem ser executados a partir da raiz do projeto:

```bash
# 1. Criar/validar a blockchain
python3 blockchain/blockchain.py

# 2. Testar cadastro de usuários e login
python3 auditoria/auth.py

# 3. Testar monitoramento de integridade de arquivos
python3 auditoria/monitor.py

# 4. Executar backup criptografado
chmod +x backup/backup.sh
./backup/backup.sh

# 5. Gerar relatório de auditoria do sistema (who, last, ss, ip a)
python3 auditoria/auditor.py
```

## Módulos

### `blockchain/blockchain.py`
Implementa a blockchain de auditoria. Cada bloco contém `id`, `timestamp`, `evento`, `hash_anterior` e `hash_atual` (SHA-256). A função `validar_chain()` percorre toda a cadeia e detecta tanto adulteração direta de um bloco (hash recalculado diferente do hash armazenado) quanto quebra de encadeamento (hash_anterior divergente do hash do bloco anterior).

### `auditoria/auth.py`
Sistema de autenticação com cadastro de usuários por perfil (`admin`, `analista`, `visitante`) e login com verificação de senha. Senhas armazenadas como hash SHA-256 com salt — nunca em texto puro. Todo evento de cadastro, login bem-sucedido e tentativa de login falha é registrado na blockchain.

### `auditoria/monitor.py`
Monitora o diretório `documentos/`, calculando hash SHA-256 de cada arquivo. Compara com hashes de referência salvos em `logs/hashes_referencia.json` e detecta — e registra na blockchain — arquivos alterados, excluídos ou incluídos.

### `auditoria/auditor.py`
Coleta dados de auditoria do sistema operacional (`who`, `last`, `ss -tulpn`, `ip a`) e gera um relatório datado em `auditoria/relatorios/`. A geração do relatório também é registrada como evento na blockchain.

### `backup/backup.sh`
Compacta o conteúdo de `documentos/` em `.tar.gz`, criptografa com AES-256 (via `openssl enc`), remove o arquivo não criptografado, registra o resultado em `logs/backup.log` e adiciona um bloco na blockchain confirmando a execução.

## Segurança Aplicada

- **Senhas:** hash SHA-256 com salt (nunca texto puro)
- **Backup:** criptografia simétrica AES-256-CBC via OpenSSL
- **Integridade de arquivos e blocos:** hash SHA-256
- **Controle de acesso:** usuários Linux segregados por função, com permissões mínimas necessárias (chmod, chown, ACL)
- **Auditoria contínua:** todo evento relevante do sistema é registrado de forma imutável na blockchain

## Equipe e Responsabilidades

| Integrante | Responsabilidade |
|------------|------------------|
| Afaly Santos | RF01 (usuários e permissões no Linux), RF02 (autenticação) e RF03 (monitoramento de integridade de arquivos) |
| Jonathas dos Santos | RF04 (blockchain), RF05 (backup automatizado) e RF06 (auditoria do sistema operacional) |
| Bruno dos Santos | RF07 (validação da blockchain), relatório técnico e vídeo demonstrativo |

## Observações de Segurança para Produção

- O salt usado em `auth.py` é fixo no código-fonte; em produção, recomenda-se `bcrypt` com salt aleatório por usuário.
- A senha de criptografia do backup está fixa em `backup.sh`; em produção, deveria vir de uma variável de ambiente ou de um cofre de segredos (ex: Vault, AWS Secrets Manager).
