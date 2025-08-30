### 📂 `readmes/03-validacao.md`

Este passo implementa o **módulo de validação de dados**, responsável por garantir que os dados extraídos atendem a critérios mínimos de qualidade antes de continuar no pipeline.

---

## 🔶 Objetivo
- Detectar **duplicatas, valores nulos e tipos inválidos**.
- Checar **regras de negócio** importantes (ex.: total_value > 0, orders com customer_id válido).
- Retornar um relatório estruturado com status PASS/FAIL.

---

## 🔶 Estrutura utilizada
- `data/orders.csv`
- `data/customers.csv`
- `src/validation/data_quality.py`

---

## 🔶 Exemplo de Execução
```bash
cd src
python validation/data_quality.py
```

## 🔶 Saída esperada
```bash
📊 Relatório Orders:
{   'dataset': 'orders',
    'errors': {   'duplicate_order_id': 101,
                  'invalid_amount': 124,
                  'missing_total_value': 78},
    'status': 'FAILED',
    'total_records': 5000,
    'validated_at': '2025-08-29T23:28:39.670903'}

📊 Relatório Customers:
{   'dataset': 'customers',
    'errors': {},
    'status': 'PASSED',
    'total_records': 1000,
    'validated_at': '2025-08-29T23:28:39.671907'}
```
## 🔶 Resultado
- O dataset de Orders foi marcado como FAILED devido a:
    - 101 IDs duplicados (duplicate_order_id)
    - 78 valores nulos em total_value (missing_total_value)
    - 124 valores inválidos (total_value <= 0) (invalid_amount)
- O dataset de Customers foi marcado como PASSED, sem erros.
- Próxima etapa: tratar inconsistências detectadas e preparar envio ao Data Lake (S3).

<hr style="height:2px; background-color:#807f7e; border:none;"/>