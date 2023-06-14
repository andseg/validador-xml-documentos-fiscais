# Validador de XML para Documentos Fiscais

Este é um projeto que consiste em um validador de arquivos XML para documentos fiscais, em desenvolvimento por [andseg](https://github.com/andseg), [FelpsFranco](https://github.com/FelpsFranco) e [Davii-code](https://github.com/Davii-code). O validador é específico para notas fiscais eletrônicas (NF-e).

## Funcionalidades

- Validação de arquivos XML de notas fiscais NF-e;
- Verificação de conformidade com os padrões, layouts (leiautes) e esquemas definidos pela legislação fiscal;
- Identificação de erros e inconsistências no XML;
- Relatório detalhado de erros encontrados;

## Requisitos

- [Python 3.6 ou superior](https://www.python.org/downloads/)
- (Opcional) [Docker](https://www.docker.com)

## Instalação e Execução (Sem Docker)

1. Clone o repositório:

   ```bash
   git clone https://github.com/andseg/validador-xml-documentos-fiscais.git
   ```

2. Navegue até o diretório do projeto:

   ```bash
   cd validador-xml-documentos-fiscais
   ```

3. (Opcional) Crie um ambiente virtual:

   ```bash
   python3 -m venv env
   ```

4. Ative o ambiente virtual:

   - No Linux/macOS:

     ```bash
     source env/bin/activate
     ```

   - No Windows (PowerShell):

     ```bash
     .\env\Scripts\Activate.ps1
     ```

5. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```
      
6. Navegue até o diretório do projeto:

   ```bash
   cd validador-xml-documentos-fiscais
   ```

7. Execute o servidor de desenvolvimento:

   ```bash
   python manage.py runserver
   ```
   
## Instalação e Execução (Com Docker)

1. Clone o repositório:

   ```bash
   git clone https://github.com/andseg/validador-xml-documentos-fiscais.git
   ```
   
2. Navegue até o diretório do projeto:

   ```bash
   cd validador-xml-documentos-fiscais
   ```
   
3. Execute o Docker Compose:

   ```bash
   docker compose up
   ```

## Utilização

1. Acesse o localhost [http://127.0.0.1:8000](http://127.0.0.1:8000) ou o equivalente configurado na sua versão do projeto.
2. Clique no botão para inserir uma nota fiscal (Formato .xml).
3. Clique em enviar para validar o documento e exibir informações da validação.

## Contribuição

Contribuições são bem-vindas! Se você encontrou um bug, tem uma sugestão ou deseja adicionar uma nova funcionalidade, fique à vontade para abrir uma [issue](https://github.com/andseg/validador-xml-documentos-fiscais/issues) ou enviar um pull request.

Certifique-se de seguir as diretrizes de contribuição do projeto.

## Referências

- Referência do validador de schema:
https://lxml.de/validation.html#xmlschema

- Manual de Contribuinte da SEFAZ:
[Manual de Orientação ao Contribuinte - MOC - versão 7.0 - NF-e e NFC-e.pdf](https://github.com/andseg/validador-xml-documentos-fiscais/files/11616210/Manual.de.Orientacao.ao.Contribuinte.-.MOC.-.versao.7.0.-.NF-e.e.NFC-e.pdf)

- Layout e validações do XML:
[ANEXO I - Leiaute e Regra de Validação - NF-e e NFC-e.pdf](https://github.com/andseg/validador-xml-documentos-fiscais/files/11616205/ANEXO.I.-.Leiaute.e.Regra.de.Validacao.-.NF-e.e.NFC-e.pdf)

## Licença

EM EDIÇÃO

---
