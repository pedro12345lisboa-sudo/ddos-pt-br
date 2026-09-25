# Stress Test Tool (Async)

Ferramenta de teste de carga de alta performance desenvolvida para simular tráfego HTTP assíncrono e validar a resiliência de infraestruturas web.

## Disclaimer

Este projeto é destinado exclusivamente para fins de testes de estresse em ambientes controlados ou servidores com autorização explícita. O uso indevido desta ferramenta pode resultar em indisponibilidade de serviços. O autor não se responsabiliza por qualquer dano causado.

## Especificações Técnicas

A ferramenta utiliza uma arquitetidade baseada em I/O não bloqueante para maximizar o throughput de requisições com o mínimo de consumo de recursos locais.

- **Runtime**: Python 3.10+
- **Concorrência**: Implementação baseada em `asyncio` para gerenciamento de eventos e `aiohttp` para comunicação assíncrona.
- **Protocolo**: HTTP/1.1 (suporte a Keep-Alive para otimização de conexões).
- **Simulação**: Randomização de cabeçalhos e User-Agents para mitigar detecções baseadas em padrões estáticos.

## Estrutura do Projeto

A arquitetura foi desenhada para modularidade e escalabilidade:

- `src/core/`: Contém o motor de execução (`engine.py`) e a lógica de gerenciamento de sockets e conexões.
- `src/utils/`: Módulos de utilitários para geração de payloads, randomização de headers e logs de sistema.
- `config/`: Gerenciamento de parâmetros de teste (IP, porta, limites de threads e timeouts).
- `logs/`: Armazenamento de logs de execução e métricas de performance.
- `tests/`: Testes unitários para validação da lógica de rede e engine.

## Instalação e Uso

### 1. Preparação do Ambiente

Recomenda-se o uso de ambientes virtuais para isolamento de dependências.

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows
.\venv\Scripts\activate
# Linux/macOS
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
