### 📂 `readmes/06-carga-warehouse.md`

Neste passo realizamos a **carga dos dados transformados (mart)** que estavam no Data Lake (S3) para o **Data Warehouse (Postgres)**.  
Assim fechamos o ciclo completo **Raw → Staging → Mart → DW**

## 🔶 Objetivo

- Trazer os dados já tratados pelo Glue (camada **mart**) para dentro do **Postgres**.  
- Disponibilizar tabelas analíticas `dim_customers` e `fact_sales` para consultas SQL.

## 🔶 Estrutura

### Postgres

- `ecommerce_dw`

### Schemas
- `mart`

### Tabelas
- `mart.dim_customers`
- `mart.fact_sales`

## 🔶 Processo de Carga (Python)

Criamos o script [`load_to_warehouse.py`](../load_to_warehouse.py) que faz:

1. Conecta no S3 via boto3 → lê arquivos Parquet da camada `mart/`:
   - `s3://ecommerce-data-raw-proj/mart/dim_customers/...`
   - `s3://ecommerce-data-raw-proj/mart/fact_sales/...`
   
2. Usa **pandas + pyarrow** para carregar os dados.

3. Conecta no **Postgres** (via psycopg2):
   - `dbname=ecommerce_dw`, `user=admin`, `password=admin`, `host=localhost`, `port=5432`

4. Cria as tabelas, caso não existam:
   ```sql
   CREATE TABLE IF NOT EXISTS mart.dim_customers (
       customer_id INT,
       customer_name TEXT,
       email TEXT,
       registration_date DATE,
       city TEXT,
       state TEXT
   );

   CREATE TABLE IF NOT EXISTS mart.fact_sales (
       order_id INT,
       customer_id INT,
       order_date DATE,
       total_value NUMERIC,
       payment_type TEXT,
       status TEXT
   );
Faz `TRUNCATE` e insere todos os registros (carga full).

## 🔶 Resultado

- mart.dim_customers preenchida com clientes (exemplo: 1000 registros).
- mart.fact_sales preenchida com pedidos completados (exemplo: 1789 registros).

Essas tabelas podem ser consumidas por ferramentas de BI, dashboards ou análises SQL diretamente no Data Warehouse.

<hr style="height:2px; background-color:#807f7e; border:none;">