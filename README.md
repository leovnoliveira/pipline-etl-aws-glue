# Documentação do Projeto de Engenharia de Dados

## Visão Geral

Este projeto de engenharia de dados tem como objetivo principal a conversão de arquivos no formato `.csv` para o formato `.parquet`, visando otimizar o armazenamento e o processamento de dados em um bucket S3 da AWS. O pipeline de dados contempla as seguintes etapas e ferramentas:

- **Conversão de Arquivos:** Transformação de arquivos `.csv` em `.parquet` para garantir maior eficiência no armazenamento e leitura dos dados.
- **Armazenamento em S3:** Os arquivos convertidos são armazenados em buckets S3, aproveitando a escalabilidade e durabilidade do serviço de armazenamento da AWS.
- **Processamento com PySpark:** Utilização do PySpark para processamento distribuído dos dados, permitindo manipulação eficiente de grandes volumes de informação.
- **Integração com AWS Glue:** Uso do AWS Glue para catalogação dos dados, facilitando a descoberta, organização e preparação dos dados para análises.
- **Consulta com AWS Athena:** Disponibilização dos dados para consulta ad-hoc utilizando o AWS Athena, permitindo análises SQL diretamente sobre os dados armazenados no S3.

## Objetivos

- Melhorar a performance de leitura e escrita dos dados.
- Reduzir custos de armazenamento utilizando o formato `.parquet`.
- Garantir a escalabilidade e segurança dos dados na nuvem AWS.
- Facilitar o processamento e análise dos dados por meio de ferramentas modernas e integradas.

## Ferramentas Utilizadas

- **AWS S3:** Armazenamento de dados.
- **PySpark:** Processamento distribuído de dados.
- **AWS Glue:** Catalogação e ETL.
- **AWS Athena:** Consulta SQL sobre dados no S3.

## Fluxo de Dados

1. Recebimento de arquivos `.csv`.
2. Conversão para `.parquet`.
3. Upload dos arquivos `.parquet` para o bucket S3.
4. Catalogação dos dados com AWS Glue.
5. Processamento e análise dos dados com PySpark e Athena.

## Considerações

- O projeto segue as melhores práticas de segurança e governança de dados na AWS.
- O uso do formato `.parquet` proporciona compressão e leitura eficiente, essencial para grandes volumes de dados.
- A integração entre Glue e Athena facilita a democratização do acesso aos dados para diferentes áreas da empresa.


## Usos

Clone este repositório com

```
git clone https://github.com/leovnoliveira/pipeline-etl-aws-glue
cd pipeline-etl-aws-glue
```

Exemplo de execução no script `./pipeline/main.py`


{python}```
from pipeline.csv_to_parquet import process_csv

def main():
    # Define the input CSV file, output directory, S3 bucket name, and S3 key
    csv_file = "./data/international_education_costs.csv"
    output_dir = "output"
    bucket_name = "sql-athena-parquet-3"
    s3_key = "parquet_files/internacional_education_costs.parquet"

    # Process the CSV file and upload to S3
    process_csv(csv_file, output_dir, bucket_name, s3_key)

if __name__ == "__main__":
    main()
```
Para executar, utilize os comandos

```
uv venv --python 3.11 # criar um abiente virtual python
source .venv/Scripts/activate # ativar o ambiente criado
uv pip install -r requirements.txt # instalar as bibliotecas necessárias
uv run -m pipeline.main # execute os comandos
```

* P.S.: para instalar os comandos uv, siga os passos

### macOS e Linux
```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Se o seu sistema não tiver `curl`, você pode usar `wget` desta forma:

```
wget -qO- https://astral.sh/uv/install.sh | sh
```

### Windows Powershell
```
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## Documentação do Script `csv_to_parquet.py`

O script `csv_to_parquet.py` foi desenvolvido para processar arquivos CSV, convertê-los para o formato Parquet e realizar o upload do arquivo gerado para um bucket S3 na AWS. Abaixo, segue uma explicação detalhada do funcionamento do script, dividida em etapas lógicas:

### 1. Importação de Bibliotecas
O script utiliza as seguintes bibliotecas:
- **`os`**: Para manipulação de diretórios e arquivos no sistema operacional.
- **`pandas`**: Para leitura e manipulação de dados tabulares.
- **`pyarrow` e `pyarrow.parquet`**: Para conversão de dados para o formato Parquet.
- **`boto3`**: Para interação com os serviços da AWS, como o S3.

### 2. Função Principal: `process_csv`
A função `process_csv` é responsável por todo o fluxo de processamento do arquivo CSV. Ela recebe os seguintes parâmetros:
- **`csv_file`**: Caminho do arquivo CSV de entrada.
- **`output_dir`**: Diretório onde o arquivo Parquet será salvo.
- **`bucket_name`**: Nome do bucket S3 onde o arquivo será enviado.
- **`s3_key`**: Caminho (chave) do arquivo no bucket S3.

### 3. Criação do Diretório de Saída
O script verifica se o diretório de saída especificado existe:
- Caso não exista, ele cria o diretório automaticamente.

### 4. Configuração do Cliente S3
O script utiliza a biblioteca `boto3` para interagir com o S3. Ele pressupõe que as credenciais da AWS estejam configuradas no ambiente, seja por meio de variáveis de ambiente ou de um perfil de configuração.

### 5. Leitura do Arquivo CSV
O script verifica se o arquivo CSV especificado existe:
- Caso o arquivo não seja encontrado, uma exceção `FileNotFoundError` é lançada.
- O arquivo CSV é lido e carregado em um DataFrame do `pandas`.

### 6. Conversão para JSON e Parquet
- O DataFrame é salvo em formato JSON no diretório de saída, com o nome `internacional_education_costs.json`.
- O DataFrame é convertido para o formato Parquet utilizando a biblioteca `pyarrow` e salvo no diretório de saída com o nome `internacional_education_costs.parquet`.

### 7. Upload para o S3
O arquivo Parquet gerado é enviado para o bucket S3 especificado, utilizando o cliente S3 do `boto3`.

### 8. Observações Importantes
- Certifique-se de que as bibliotecas listadas no arquivo `requirements.txt` estejam instaladas antes de executar o script.
- Configure corretamente as credenciais da AWS no ambiente para garantir o funcionamento do upload para o S3.

Com essas etapas, o script `csv_to_parquet.py` oferece uma solução completa para a conversão de arquivos CSV para Parquet e seu armazenamento na nuvem.