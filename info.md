# Home Assistant Correios

[![Generic badge](https://img.shields.io/badge/contributor-@dougiteixeira-<COLOR>.svg)](https://github.com/dougiteixeira)
[![Generic badge](https://img.shields.io/badge/contributor-@oridestomkiel-<COLOR>.svg)](https://github.com/oridestomkiel)

## Rastreamento de objetos nos correios.

![exemplo1](https://raw.github.com/luyzfernando08/ha-correios/blob/main/exemplo1.jpg)

### Configuração Automática

A adição da integração à sua instância do Home Assistant pode ser feita através da interface do usuário, usando este botão:

#### IMPORTANTE: Clique no botão abaixo com a opção de abrir em uma nova janela

<a href="https://my.home-assistant.io/redirect/config_flow_start?domain=correios" rel="Rastreamento Correios">![Correios](https://my.home-assistant.io/badges/config_flow_start.svg)</a>

### Configuração Manual:

* Na barra lateral clique em Configuração .
* No menu de configuração selecione Dispositivos e Serviços .

![hacs10](https://raw.github.com/luyzfernando08/ha-correios/main/resources/hacs-10.png)

* Vá no canto direito embaixo e clique em “+ Adicionar Integração”.
* Na lista, pesquise e selecione “Rastreamento Correios” .

![hacs7](https://raw.github.com/luyzfernando08/ha-correios/main/resources/hacs-07.png)

* Digite a descrição e o código da ecomenda e clique no botão Enviar.

![hacs8](https://raw.github.com/luyzfernando08/ha-correios/main/resources/hacs-08.png)

- [x] Pronto, agora você verá seus rastreios e poderá realizar as suas integrações!

![hacs9](https://raw.github.com/luyzfernando08/ha-correios/main/resources/hacs-09.png)

***

## State and Attributes

### State

* Descrição do status atual do objeto

#### - EVENTOS SRO - CORREIOS

https://www.correios.com.br/atendimento/ferramentas/sistemas/arquivos/lista-de-eventos-rastreamento-de-objetos

### Attributes

* Descrição: Apelido dado ao objeto no arquivio de configuração
* Código Objeto: Código identificador do objeto nos Correios
* Data Prevista: Quando existente, exibe a previsão de entrega do objeto
* Tipo Postal: Tipo de serviço referente ao pacote enviado.

![exemplo2](https://raw.github.com/luyzfernando08/ha-correios/blob/main/exemplo2.jpg)