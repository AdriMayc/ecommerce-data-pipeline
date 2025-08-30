### 📂 `readmes/04-datalake.md`

Este passo implementa a camada de **armazenamento no Data Lake** utilizando o Amazon S3. Os dados extraídos e validados são enviados para buckets S3, organizados em uma estrutura de pastas que facilita o consumo e a governança.

---

## 🔶 Objetivo
- Armazenar os dados brutos (`orders.csv`, `customers.csv`) no S3.
- Utilizar o serviço **boto3** para interagir com a AWS.
- Organizar os arquivos em uma estrutura particionada por data (`raw/<dataset>/<ano>/<mes>/<arquivo>`).
- Garantir que os buckets existam ou sejam criados automaticamente.

---

## 🔶 Estrutura utilizada
- `src/utils/s3_uploader.py`
- Variáveis de ambiente no `.env` para credenciais AWS e nome do bucket.

---

## 🔶 Configuração de Ambiente
Certifique-se de que as seguintes variáveis estão definidas no seu arquivo `.env` na raiz do projeto:
```bash
AWS_ACCESS_KEY_ID=SEU_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY=SEU_SECRET_ACCESS_KEY
AWS_DEFAULT_REGION=us-east-1
S3_BUCKET_RAW_PROJ=ecommerce-data-raw-proj # Ou o nome que você definir
```

## 🔶 Exemplo de Execução
```bash
cd src
python utils/s3_uploader.py
```

## 🔶 Saída esperada

```bash
2025-08-30 01:04:27,372 - botocore.credentials - INFO - Found credentials in shared credentials file: ~/.aws/credentials
2025-08-30 01:04:27,494 - __main__ - INFO - S3Uploader inicializado para bucket 'ecommerce-data-raw-proj' na região sa-east-1
2025-08-30 01:04:28,711 - __main__ - INFO - Bucket 'ecommerce-data-raw-proj' criado com sucesso.
2025-08-30 01:04:28,866 - __main__ - INFO - Upload realizado: s3://ecommerce-data-raw-proj/raw/orders/2025/08/orders.csv
2025-08-30 01:04:28,941 - __main__ - INFO - Upload realizado: s3://ecommerce-data-raw-proj/raw/customers/2025/08/customers.csv
```

## 🔶 Resultado

- Os arquivos orders.csv e customers.csv foram enviados com sucesso para o bucket S3 especificado.
- A estrutura de pastas no S3 segue o padrão `raw/<dataset>/<ano>/<mes>/<arquivo>`, facilitando a organização e consultas futuras.

<hr style="height:2px; background-color:#807f7e; border:none;">