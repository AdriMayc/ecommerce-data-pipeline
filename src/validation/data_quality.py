import pandas as pd
import logging
from typing import Dict, Any
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class DataQualityValidator:
    
    def __init__(self):
        logger.info("Validator inicializado")

    def validate_orders(self, orders_df: pd.DataFrame, customers_df: pd.DataFrame) -> Dict[str, Any]:
        errors = {}

        # 1. Checar duplicatas por order_id
        duplicates = orders_df.duplicated(subset=["order_id"]).sum()
        if duplicates > 0:
            errors["duplicate_order_id"] = int(duplicates)

        # 2. Checar valores nulos em colunas críticas
        critical_cols = ["order_id", "customer_id", "order_date", "total_value"]
        nulls = orders_df[critical_cols].isnull().sum().to_dict()
        for col, count in nulls.items():
            if count > 0:
                errors[f"missing_{col}"] = int(count)

        # 3. Checar valores inválidos em total_value
        invalid_amounts = (orders_df["total_value"].fillna(0) <= 0).sum()
        if invalid_amounts > 0:
            errors["invalid_amount"] = int(invalid_amounts)

        # 4. Validar se customer_id existe na base de clientes
        invalid_customers = ~orders_df["customer_id"].isin(customers_df["customer_id"])
        invalid_customers_count = invalid_customers.sum()
        if invalid_customers_count > 0:
            errors["invalid_customer_id"] = int(invalid_customers_count)

        # 5. Checar formato da data
        try:
            pd.to_datetime(orders_df["order_date"], errors="raise", format="%Y-%m-%d")
        except Exception as e:
            errors["invalid_order_date_format"] = f"Erro: {str(e)}"

        report = {
            "dataset": "orders",
            "total_records": len(orders_df),
            "errors": errors,
            "status": "FAILED" if errors else "PASSED",
            "validated_at": datetime.now().isoformat()
        }

        logger.info(f"Validação concluída. Status: {report['status']}")
        return report

    def validate_customers(self, customers_df: pd.DataFrame) -> Dict[str, Any]:
        errors = {}

        # IDs duplicados
        duplicates = customers_df.duplicated(subset=["customer_id"]).sum()
        if duplicates > 0:
            errors["duplicate_customer_id"] = int(duplicates)

        # Campos obrigatórios do schema REAL
        critical_cols = ["customer_id", "customer_name", "email"]
        nulls = customers_df[critical_cols].isnull().sum().to_dict()
        for col, count in nulls.items():
            if count > 0:
                errors[f"missing_{col}"] = int(count)

        report = {
            "dataset": "customers",
            "total_records": len(customers_df),
            "errors": errors,
            "status": "FAILED" if errors else "PASSED",
            "validated_at": datetime.now().isoformat()
        }

        logger.info(f"Validação concluída. Status: {report['status']}")
        return report


def main():
    try:
        orders_df = pd.read_csv("data/orders.csv")
        customers_df = pd.read_csv("data/customers.csv")

        validator = DataQualityValidator()

        orders_report = validator.validate_orders(orders_df, customers_df)
        customers_report = validator.validate_customers(customers_df)

        print("\n📊 Relatório Orders:", orders_report)
        print("📊 Relatório Customers:", customers_report)

    except Exception as e:
        logger.error(f"Erro na execução: {str(e)}")


if __name__ == "__main__":
    main()