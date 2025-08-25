# 🌐 Calculadora de Rede Completa

Um sistema completo em Python para cálculos e análises de redes IP, desenvolvido para facilitar o trabalho de administradores de rede, estudantes e profissionais de TI.

## 📋 Funcionalidades

### ✅ Funcionalidades Principais

- **Cálculo de Informações de Rede**: Análise completa de redes IP
- **Conversões**: CIDR ↔ Máscara Decimal
- **Divisão de Sub-redes (FLSM)**: Fixed Length Subnet Masking
- **VLSM**: Variable Length Subnet Masking
- **Validação**: IPs e redes
- **Verificação de Pertencimento**: Se um IP pertence a uma rede
- **Cálculo de Super-rede**: Agregação de redes
- **Classificação de IPs**: Classe e tipo (público/privado)

### 🔧 Ferramentas Incluídas

1. **NetworkCalculator**: Classe principal com todas as funcionalidades
2. **Interface CLI**: Interface de linha de comando interativa
3. **Suite de Testes**: Testes automatizados para validação

## 🚀 Como Usar

### Instalação

1. Clone ou baixe os arquivos do projeto
2. Certifique-se de ter Python 3.6+ instalado
3. Execute o programa:

```bash
python cli_interface.py
```

### Uso da Interface CLI

A interface oferece um menu interativo com as seguintes opções:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              MENU PRINCIPAL                                │
├─────────────────────────────────────────────────────────────────────────────┤
│  1. Calcular informações de rede                                           │
│  2. Converter CIDR para máscara decimal                                    │
│  3. Converter máscara decimal para CIDR                                    │
│  4. Dividir rede em sub-redes (FLSM)                                       │
│  5. Calcular VLSM (Variable Length Subnet Masking)                         │
│  6. Verificar se IP pertence a uma rede                                    │
│  7. Calcular super-rede                                                    │
│  8. Validar endereço IP                                                    │
│  9. Validar rede                                                           │
│  0. Sair                                                                   │
└─────────────────────────────────────────────────────────────────────────────┘
```


## 📖 Exemplos de Uso

### 1. Análise de Rede

**Entrada**: `192.168.1.0/24`

**Saída**:
```
╔══════════════════════════════════════════════════════════════╗
║                    INFORMAÇÕES DA REDE                      ║
╠══════════════════════════════════════════════════════════════╣
║ Rede:              192.168.1.0                              ║
║ CIDR:              /24                                       ║
║ Máscara:           255.255.255.0                            ║
║ Broadcast:         192.168.1.255                            ║
║ Primeiro Host:     192.168.1.1                              ║
║ Último Host:       192.168.1.254                            ║
║ Total de Hosts:    254                                       ║
║ Total Endereços:   256                                       ║
║ Classe:            C                                         ║
║ Tipo:              Privada                                   ║
╚══════════════════════════════════════════════════════════════╝
```

### 2. Divisão em Sub-redes (FLSM)

**Entrada**: Rede `192.168.1.0/24`, 4 sub-redes

**Saída**:
```
ID  Rede               CIDR   Máscara         Broadcast       Hosts   
────────────────────────────────────────────────────────────────────
1   192.168.1.0        /26    255.255.255.192 192.168.1.63    62      
2   192.168.1.64       /26    255.255.255.192 192.168.1.127   62      
3   192.168.1.128      /26    255.255.255.192 192.168.1.191   62      
4   192.168.1.192      /26    255.255.255.192 192.168.1.255   62      
```

### 3. VLSM (Variable Length Subnet Masking)

**Entrada**: Rede `192.168.1.0/24`, hosts necessários: [50, 25, 10, 5]

**Saída**:
```
Ordem  Solicitado Rede               CIDR   Disponível Range de Hosts        
──────────────────────────────────────────────────────────────────────────
1      50         192.168.1.0        /26    62         192.168.1.1 - 192.168.1.62
2      25         192.168.1.64       /27    30         192.168.1.65 - 192.168.1.94
3      10         192.168.1.96       /28    14         192.168.1.97 - 192.168.1.110
4      5          192.168.1.112      /29    6          192.168.1.113 - 192.168.1.118
```

## 🧪 Testes

Para executar os testes automatizados:

```bash
python test_calculator.py
```

Os testes cobrem:
- Validação de IPs e redes
- Conversões entre CIDR e máscara
- Cálculos de sub-redes
- VLSM
- Verificação de pertencimento
- Classificação de IPs
- Testes de integração

## 📁 Estrutura do Projeto

```
tools/
├── network_calculator.py    # Classe principal com todas as funcionalidades
├── cli_interface.py         # Interface de linha de comando
├── test_calculator.py       # Suite de testes
├── requirements.txt         # Dependências do projeto
└── README.md               # Documentação (este arquivo)
```

## 🔧 Dependências

O projeto utiliza apenas bibliotecas padrão do Python:
- `ipaddress`: Para manipulação de endereços IP
- `socket`: Para conversões de rede
- `struct`: Para manipulação de dados binários
- `unittest`: Para testes automatizados

## 🎯 Casos de Uso

### Para Administradores de Rede
- Planejamento de sub-redes
- Análise de espaço de endereçamento
- Validação de configurações
- Documentação de redes

### Para Estudantes
- Aprendizado de conceitos de rede
- Verificação de cálculos manuais
- Compreensão de VLSM e FLSM
- Prática com diferentes cenários

### Para Desenvolvedores
- Integração em sistemas maiores
- Automação de tarefas de rede
- Validação de configurações
- Base para ferramentas mais complexas

## 🚀 Funcionalidades Futuras

- [ ] Suporte para IPv6
- [ ] Interface gráfica (GUI)
- [ ] Exportação de resultados (CSV, JSON)
- [ ] Calculadora de bandwidth
- [ ] Análise de performance de rede
- [ ] Integração com APIs de rede
- [ ] Suporte para VLANs
- [ ] Calculadora de delay e latência

## 🔐 Funcionalidades Futuras de Segurança

- [ ] Scanner de Portas TCP (similar ao Nmap básico)
- [ ] Fingerprinting de Serviços (captura de banners)
- [ ] Ping Sweep (descoberta de hosts ativos na rede)
- [ ] Verificação de vulnerabilidades comuns (FTP anônimo, Telnet, etc.)
- [ ] Consulta de IPs em APIs externas (Shodan, VirusTotal)
- [ ] Força bruta em serviços (SSH/FTP) para fins educativos
- [ ] Exportação de relatórios de segurança em JSON/CSV


## 🤝 Contribuições

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Implemente suas mudanças
4. Execute os testes
5. Envie um pull request

## 📝 Licença

Este projeto é de código aberto e está disponível sob a licença MIT.

## 📞 Suporte

Para dúvidas, sugestões ou problemas:
- Abra uma issue no repositório
- Consulte a documentação
- Execute os testes para verificar o funcionamento
- 📧 Email: rodrigo@rodrigoviana.dev.br
- 🌐 Site: https://rodrigoviana.dev.br
- 💼 LinkedIn: https://linkedin.com/in/rodrigo-viana


---
