### 📂 `readmes/01-ambiente.md`

Este documento orienta a configuração inicial do ambiente para o projeto Ecommerce Data Pipeline, incluindo a criação de recursos AWS, configuração de credenciais e preparação do ambiente local.

## 🔶 Pré-requisitos

### Conta AWS
- Conta AWS ativa com permissões para:
- S3 (criação de buckets, upload/download de objetos)
- Glue (criação de crawlers, databases, jobs)
- Athena (execução de queries, configuração de workgroups)
- IAM (criação de usuários, roles e políticas)

### Ambiente Local
- Python 3.8+ instalado
- Git para controle de versão
- AWS CLI (opcional, mas recomendado)

## 🔶 Configuração AWS

### 1. Criação do Bucket S3
Crie um bucket para armazenar os dados do projeto:

### Via AWS CLI (opcional)
aws s3 mb s3://ecommerce-datalake-project --region sa-east-1
- **Ou via Console AWS:**

    1. Acesse S3 → Create bucket

    2. Nome: ecommerce-datalake-project (ou nome único de sua escolha)

    3. Região: sa-east-1 (ou região de sua preferência)

    4. Configurações padrão (Block all public access = habilitado)

### 2. Estrutura de Pastas no S3
Crie a seguinte estrutura no bucket:

````
s3://ecommerce-datalake-project/
├── mart/
│   ├── dim_customers.parquet/
│   └── fact_sales.parquet/
└── queries-athena/
    └── (pasta para resultados do Athena)
````

### 3. Usuário IAM para Metabase
Crie um usuário IAM com as seguintes permissões:

Política JSON:
````
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "athena:*",
        "glue:GetDatabase",
        "glue:GetDatabases",
        "glue:GetTable",
        "glue:GetTables",
        "glue:GetPartitions",
        "s3:GetBucketLocation",
        "s3:GetObject",
        "s3:ListBucket",
        "s3:ListBucketMultipartUploads",
        "s3:ListMultipartUploadParts",
        "s3:AbortMultipartUpload",
        "s3:PutObject"
      ],
      "Resource": "*"
    }
  ]
}
````
Passos:

1. IAM → Users → Create user

2. Nome: metabase-athena-user

3. Attach policy: Cole a política JSON acima

4. Importante: Salve as credenciais (Access Key + Secret Key)

## 🔶 Ambiente Python Local

### 1. Clone do Repositório
````
git clone <seu-repositorio>
cd ecommerce-data-pipeline
````
### 2. Ambiente Virtual

````
# Criar ambiente virtual
python -m venv .venv

# Ativar (Windows)
.venv\Scripts\activate

# Ativar (Linux/Mac)
source .venv/bin/activate
````
### 3. Instalação de Dependências

```
pip install -r requirements.txt
```

### 4. Configuração de Credenciais AWS (Opcional)

Se for usar AWS CLI ou boto3 localmente:

``aws configure``

Ou crie o arquivo ``~/.aws/credentials:``

```
[default]
aws_access_key_id = SEU_ACCESS_KEY
aws_secret_access_key = SEU_SECRET_KEY
region = sa-east-1
```

## 🔶 Metabase (Docker)

```
# subir
docker compose up -d

# logs (opcional)
docker compose logs -f

# parar
docker compose down
```

## 🔶 Glue Data Catalog

1. Glue → Databases → Add database
    - Nome: ecommerce_db
2. Glue → Crawlers → Create crawler
    - Nome: ecommerce-mart-crawler
    - Data source: s3://ecommerce-datalake-project/mart/
    - IAM role: uma role com acesso a S3 + Glue
    - Target database: ecommerce_db
    - Schedule: On demand
3. Execute o crawler e verifique se criou as tabelas (ex.: dim_customers, fact_sales).

## 🔶 Athena
Settings → Query result location:

``s3://ecommerce-datalake-project/queries-athena/``

- Teste no console do Athena:

```
SHOW TABLES IN ecommerce_db;
SELECT COUNT(*) FROM ecommerce_db.fact_sales;
```

## 🔶 Conexão no Metabase (Athena)

- Database type: Amazon Athena
- Region: sa-east-1
- Workgroup: primary
- S3 staging directory:
``s3://ecommerce-datalake-project/queries-athena/``
- Catalog: AwsDataCatalog
- Database: ecommerce_db
- Access key / Secret key: do usuário IAM criado


## 🔶 Checklist rápido

- [ ] Bucket S3 criado e pastas mart/ e queries-athena/
- [ ] Usuário IAM do Metabase com permissões (S3, Glue, Athena)
- [ ] Credenciais AWS configuradas localmente (ou via Docker env)
- [ ] Database ecommerce_db no Glue
- [ ] Crawler executado e tabelas criadas
- [ ] Athena com query result location apontando para queries-athena/
- [ ] Metabase rodando via Docker e conectado ao Athena

<hr style="height:2px; background-color:#807f7e; border:none;">