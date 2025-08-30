### 📂 `readmes/02-extracao.md`

Este passo implementa o módulo de **extração** do pipeline, responsável por ler os dados brutos (CSV e JSON) e gerar **metadados** básicos para monitoramento.


## 🔶 Objetivo
- Ler arquivos CSV (`orders.csv`, `customers.csv`) e JSON (`orders.json`) com dados de exemplo.
- Estruturar os dados em `pandas.DataFrame`.
- Retornar **metadados**: quantidade de registros, colunas, nulos e uso de memória.

---

## 🔶 Estrutura utilizada
- `data/orders.csv`
- `data/orders.json`
- `data/customers.csv`
- `src/extraction/data_extractor.py`

---

## 🔶 Exemplo de Execução
```bash
cd src
python extraction/data_extractor.py
```

## 🔶 Saída esperada

```bash
2025-08-29 22:57:57,267 - __main__ - INFO - Extraindo dados de pedidos de: data/orders.csv
2025-08-29 22:57:57,274 - __main__ - INFO - Dados extraídos com sucesso: 5000 registros
Metadados da extração:
- Fonte: orders.csv
- Registros: 5000
- Colunas: ['order_id', 'customer_id', 'order_date', 'total_value', 'payment_type', 'status']
- Uso de memória: 0.94 MB
- Valores nulos por coluna: {'order_id': 0, 'customer_id': 0, 'order_date': 0, 'total_value': 78, 'payment_type': 0, 'status': 0}
```

## 🔶 Resultado

- Dados de **orders** e **customers** foram extraídos com sucesso.
- Metadados permitem entender rapidamente a qualidade inicial do dataset.
- Detectamos **78 valores nulos em** total_value, que serão tratados na próxima etapa (validação).

<hr style="height:2px; background-color:#807f7e; border:none;">