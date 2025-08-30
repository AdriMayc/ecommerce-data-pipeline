import pandas as pd
import json
import logging
from typing import Dict, List, Optional
from pathlib import Path
import os
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DataExtractor:
    
    def __init__(self, data_path: str = "data/"):
        self.data_path = Path(data_path)
        logger.info(f"DataExtractor inicializado com caminho: {self.data_path}")
    
    def extract_orders_csv(self, filename: str = "orders.csv") -> pd.DataFrame:

        try:
            file_path = self.data_path / filename
            logger.info(f"Extraindo dados de pedidos de: {file_path}")
            
            df = pd.read_csv(file_path)
            logger.info(f"Dados extraídos com sucesso: {len(df)} registros")
            
            return df
            
        except FileNotFoundError:
            logger.error(f"Arquivo não encontrado: {file_path}")
            raise
        except Exception as e:
            logger.error(f"Erro ao extrair dados: {str(e)}")
            raise
    
    def extract_orders_json(self, filename: str = "orders.json") -> pd.DataFrame:
        try:
            file_path = self.data_path / filename
            logger.info(f"Extraindo dados de pedidos de: {file_path}")
            
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            df = pd.DataFrame(data)
            logger.info(f"Dados extraídos com sucesso: {len(df)} registros")
            
            return df
            
        except FileNotFoundError:
            logger.error(f"Arquivo não encontrado: {file_path}")
            raise
        except Exception as e:
            logger.error(f"Erro ao extrair dados: {str(e)}")
            raise
    
    def extract_customers_csv(self, filename: str = "customers.csv") -> pd.DataFrame:
        try:
            file_path = self.data_path / filename
            logger.info(f"Extraindo dados de clientes de: {file_path}")
            
            df = pd.read_csv(file_path)
            logger.info(f"Dados extraídos com sucesso: {len(df)} registros")
            
            return df
            
        except FileNotFoundError:
            logger.error(f"Arquivo não encontrado: {file_path}")
            raise
        except Exception as e:
            logger.error(f"Erro ao extrair dados: {str(e)}")
            raise
    
    def get_extraction_metadata(self, df: pd.DataFrame, source: str) -> Dict:
        return {
            'source': source,
            'extraction_timestamp': datetime.now().isoformat(),
            'total_records': len(df),
            'columns': list(df.columns),
            'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024 / 1024,
            'null_counts': df.isnull().sum().to_dict()
        }

def main():
    extractor = DataExtractor()
    
    # Testar extração de pedidos CSV
    try:
        orders_df = extractor.extract_orders_csv()
        metadata = extractor.get_extraction_metadata(orders_df, "orders.csv")
        
        print("Metadados da extração:")
        print(f"- Fonte: {metadata['source']}")
        print(f"- Registros: {metadata['total_records']}")
        print(f"- Colunas: {metadata['columns']}")
        print(f"- Uso de memória: {metadata['memory_usage_mb']:.2f} MB")
        print(f"- Valores nulos por coluna: {metadata['null_counts']}")
        
    except Exception as e:
        logger.error(f"Erro no teste: {str(e)}")


if __name__ == "__main__":
    main()