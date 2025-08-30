### 📂 `readmes/05-transfomacoes-glue.md`

Neste passo implementamos a camada de **staging (stg)** e **mart (analítica)** usando o **AWS Glue** como mecanismo de ETL em **PySpark.**

## 🔶 Objetivo

- Transformar os dados brutos (`raw/`) depositados no Data Lake (S3) em dados limpos (`stg/`) e modelados para análise (`mart/`).
- Utilizar o Glue para aplicar regras de negócio e conversões de tipos de dados.
- Escrever os resultados de volta no S3 em formato Parquet otimizado.

## 🔶 Estrutura utilizada

```hash
s3://ecommerce-data-raw-proj/
├── raw/
│ ├── customers/2025/08/customers.csv
│ └── orders/2025/08/orders.csv
│
├── stg/
│ ├── customers/part-0000.snappy.parquet
│ └── orders/part-0000.snappy.parquet
│
└── mart/
├── fact_sales/part-0000.snappy.parquet
└── dim_customers/part-0000.snappy.parquet
```

## 🔶 Processo no Glue

1. **Leitura**
   - Leitura dos arquivos `customers.csv` e `orders.csv` da camada **raw**.
   - Definição de `schema` explícito via `StructType` para evitar problemas de inferência.

2. **Transformação**
   - Conversão de tipos (`int`, `double`, `date`).
   - Criação do `stg_customers` e `stg_orders`.
   - Criação das tabelas analíticas:
     - `mart.fact_sales` (apenas pedidos com `status = 'completed'`).
     - `mart.dim_customers`.

3. **Escrita**
   - Dados gravados em formato **Parquet** no S3 para otimizar consulta via Athena ou Redshift Spectrum.

## 🔶 Script PySpark do Job

- Código implementado em **Script editor do Glue**.
- Inclui:
  - Schemas (`customers_schema`, `orders_schema`).
  - Leitura de múltiplos níveis de partição (`*/*/*.csv`).
  - Escrita em `/stg/` e `/mart/`.
>O script PySpark está disponível em: [`glue/job-spark.py`](../glue/job-spark.py)

## 🔶 Resultado

- Dados foram processados com sucesso e se encontram disponíveis em:
  - `s3://ecommerce-data-raw-proj/stg/...`
  - `s3://ecommerce-data-raw-proj/mart/...`



Estes dados agora estão prontos para o **Passo 06 – Carga no Data Warehouse**.

<hr style="height:2px; background-color:#807f7e; border:none;">