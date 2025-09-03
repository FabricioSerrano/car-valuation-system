# Car Valuation System

## Visão Geral

O **Car Valuation System** é um projeto Python que automatiza a coleta, transformação e armazenamento de dados de marcas, modelos e anos de veículos a partir da API da Tabela Fipe. O objetivo é manter um banco de dados atualizado com informações relevantes para avaliação de veículos.

## Principais Componentes

- **Controllers**: Responsáveis por orquestrar o processo ETL (Extract, Transform, Load) para cada entidade (marcas, referências, modelos/anos).
  - `BrandController`: Coleta e armazena marcas de veículos.
  - `ReferenceController`: Gerencia as referências de tabela da Fipe.
  - `ModelsController`: Busca e registra modelos e anos de veículos, relacionando-os com marcas e referências.
  - `FuelsController`: Busca e registra todos os tipos de combustíveis disponíveis através do objeto Years
  - `ValueController`: Busca e registra todos os valores dos modelos de veículos disponíveis pelo ano e data de referencia.
- **Models**: Definem as tabelas e entidades do banco de dados usando SQLAlchemy ORM.
- **Utils**: Configurações auxiliares, como logging e variáveis de ambiente.

## Funcionamento

1. **Inicialização**: Ao rodar o `main.py`, o sistema cria as tabelas no banco de dados (caso não existam) e executa o ETL inicial para referências, marcas e modelos/anos.
2. **Agendamento**: Utiliza a biblioteca `schedule` para executar periodicamente o ETL de cada controller, garantindo que o banco de dados esteja sempre atualizado.
3. **Processo ETL**:
   - **Extração**: Faz requisições HTTP para a API da Fipe.
   - **Transformação**: Converte os dados recebidos em objetos Python.
   - **Carga**: Salva os dados no banco de dados MariaDB, evitando duplicidades.

## Principais Arquivos

- `main.py`: Ponto de entrada do sistema e responsável pelo agendamento das tarefas.
- `controllers/models_controller.py`: Implementa a lógica de coleta e registro de modelos e anos de veículos.
- `controllers/brand_controller.py` : Implementa a lógica de coleta e registro de marcas de veículos.
- `controllers/reference_controller.py` : Implementa a lógica de coleta e registro de mês/ano de referencia dos valores
- `controllers/fuels_controller.py` : Implementa a lógica de registro dos tipos de conbustíveis através dos anos dos modelos disponíveis.
- `controllers/value_controller.py` : Deve implementar a lógica de coleta e registro dos valores dos veículos, segundo parametros de referência, marca, modelo e ano de fabricação/combustível.
- `models/`: Contém os modelos ORM das entidades.
- `utils/configs.py`: Configurações do projeto.
- `TODO: tests/` : Implementação dos testes (unitário/itnegração)

## Tecnologias Utilizadas

- Python 3
- SQLAlchemy (ORM)
- MariaDB
- Requests (HTTP)
- Schedule (agendamento de tarefas)
- Logging

## Como Executar

1. Instale as dependências (`pip install -r requirements.txt`).
2. Configure o banco de dados e variáveis de ambiente.
3. Execute `python main.py`.

## Observações

- O sistema foi projetado para ser extensível e facilitar a manutenção dos dados de veículos.
- O código já está preparado para testes unitários e integração futura com outras fontes de dados ou funcionalidades
- *a base deste readme foi gerado por AI, demais informações estão sendo adicionadas conforme evolução do sistema*
