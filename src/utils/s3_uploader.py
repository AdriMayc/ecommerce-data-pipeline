import boto3
import logging
import os
from pathlib import Path
from botocore.exceptions import ClientError
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class S3Uploader:


    def __init__(self, bucket_name: str, aws_region: str = "sa-east-1"):
        self.bucket_name = bucket_name
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=aws_region,
        )
        logger.info(f"S3Uploader inicializado para bucket '{bucket_name}' na região {aws_region}")

    def ensure_bucket_exists(self):
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
            logger.info(f"Bucket '{self.bucket_name}' já existe.")
        except ClientError:
            self.s3_client.create_bucket(
                Bucket=self.bucket_name,
                CreateBucketConfiguration={"LocationConstraint": self.s3_client.meta.region_name},
            )
            logger.info(f"Bucket '{self.bucket_name}' criado com sucesso.")

    def upload_file(self, local_path: str, s3_prefix: str = "raw/orders") -> str: 
        try:
            filename = Path(local_path).name
            today = datetime.today()
            s3_key = f"{s3_prefix}/{today.year}/{today.month:02d}/{filename}"

            self.s3_client.upload_file(local_path, self.bucket_name, s3_key)
            s3_uri = f"s3://{self.bucket_name}/{s3_key}"
            logger.info(f"Upload realizado: {s3_uri}")
            return s3_uri
        except Exception as e:
            logger.error(f"Erro ao fazer upload: {str(e)}")
            raise


def main():
    bucket = os.getenv("S3_BUCKET_RAW_PROJ", "ecommerce-data-raw-proj")
    uploader = S3Uploader(bucket_name=bucket, aws_region=os.getenv("AWS_DEFAULT_REGION", "sa-east-1"))

    uploader.ensure_bucket_exists()

    # Exemplo: subir os arquivos orders.csv e customers.csv
    uploader.upload_file("data/orders.csv", "raw/orders")
    uploader.upload_file("data/customers.csv", "raw/customers")


if __name__ == "__main__":
    main()