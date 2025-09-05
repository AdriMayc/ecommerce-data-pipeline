import psycopg2
import pandas as pd
import boto3
import io

# Config S3
bucket = "ecommerce-data-raw-proj"
mart_paths = {
    "dim_customers": "mart/dim_customers/",
    "fact_sales": "mart/fact_sales/"
}

# Config Postgres
conn = psycopg2.connect(
    dbname="ecommerce_dw",
    user="admin",
    password="admin",
    host="localhost",  # ou 127.0.0.1
    port=5432
)
cur = conn.cursor()

# Criar schema se não existir
cur.execute("CREATE SCHEMA IF NOT EXISTS mart;")
conn.commit()

# Função para carregar Parquet → Postgres
def load_parquet_to_postgres(s3_prefix, table_name, create_sql):
    print(f"\n[INFO] Lendo dados de s3://{bucket}/{s3_prefix}")

    s3 = boto3.client("s3")
    objects = s3.list_objects_v2(Bucket=bucket, Prefix=s3_prefix)

    if "Contents" not in objects:
        print(f"[ERRO] Nenhum arquivo encontrado em {s3_prefix}")
        return

    files = [obj["Key"] for obj in objects["Contents"] if obj["Key"].endswith(".parquet")]
    print(f"[INFO] Arquivos encontrados: {files}")

    dfs = []
    for f in files:
        buffer = io.BytesIO()
        s3.download_fileobj(bucket, f, buffer)
        buffer.seek(0)
        dfs.append(pd.read_parquet(buffer))

    if not dfs:
        print(f"[ERRO] Nenhum dataframe carregado de {s3_prefix}")
        return

    df = pd.concat(dfs, ignore_index=True)
    print(f"[INFO] Total de linhas carregadas: {len(df)}")

    # Criar tabela
    cur.execute(create_sql)
    conn.commit()
    print(f"[INFO] Tabela mart.{table_name} criada/verificada")

    # Apagar dados antigos
    cur.execute(f"TRUNCATE mart.{table_name};")
    conn.commit()
    print(f"[INFO] Tabela mart.{table_name} truncada")

    # Inserir linhas
    for row in df.itertuples(index=False):
        placeholders = ",".join(["%s"] * len(row))
        cur.execute(
            f"INSERT INTO mart.{table_name} VALUES ({placeholders});",
            tuple(row)
        )
    conn.commit()
    print(f"[INFO] Inseridos {len(df)} registros em mart.{table_name}")

# Definições das tabelas mart
dim_customers_sql = """
CREATE TABLE IF NOT EXISTS mart.dim_customers (
    customer_id INT,
    customer_name TEXT,
    email TEXT,
    registration_date DATE,
    city TEXT,
    state TEXT
);
"""

fact_sales_sql = """
CREATE TABLE IF NOT EXISTS mart.fact_sales (
    order_id INT,
    customer_id INT,
    order_date DATE,
    total_value NUMERIC,
    payment_type TEXT,
    status TEXT
);
"""

# Executar as cargas
print("Iniciando carga para dim_customers...")
load_parquet_to_postgres(mart_paths["dim_customers"], "dim_customers", dim_customers_sql)

print("Iniciando carga para fact_sales...")
load_parquet_to_postgres(mart_paths["fact_sales"], "fact_sales", fact_sales_sql)

print("Carga concluída para DW Postgres!")

# Fechar conexão
cur.close()
conn.close()