import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import random
import os

# Criar diretório data se não existir
os.makedirs('data', exist_ok=True)

# Configurar seed para reprodutibilidade
np.random.seed(42)
random.seed(42)

# Gerar dados de clientes
customers_data = []
for i in range(1, 1001):  # 1000 clientes
    customers_data.append({
        'customer_id': i,
        'customer_name': f'Cliente {i}',
        'email': f'cliente{i}@email.com',
        'registration_date': (datetime.now() - timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d'),
        'city': random.choice(['São Paulo', 'Rio de Janeiro', 'Belo Horizonte', 'Salvador', 'Brasília']),
        'state': random.choice(['SP', 'RJ', 'MG', 'BA', 'DF'])
    })

customers_df = pd.DataFrame(customers_data)
customers_df.to_csv('data/customers.csv', index=False)

# Gerar dados de pedidos
orders_data = []
for i in range(1, 5001):  # 5000 pedidos
    # Introduzir alguns problemas de qualidade intencionalmente
    customer_id = random.randint(1, 1000)
    order_date = datetime.now() - timedelta(days=random.randint(0, 90))
    
    # 5% dos pedidos terão problemas
    if random.random() < 0.05:
        # Problemas intencionais
        if random.random() < 0.3:
            total_value = None  # Valor nulo
        elif random.random() < 0.3:
            total_value = -random.uniform(10, 100)  # Valor negativo
        else:
            total_value = random.uniform(10, 1000)
    else:
        total_value = random.uniform(10, 1000)
    
    # 2% dos pedidos serão duplicados
    if random.random() < 0.02 and i > 1:
        order_id = i - 1  # ID duplicado
    else:
        order_id = i
    
    orders_data.append({
        'order_id': order_id,
        'customer_id': customer_id,
        'order_date': order_date.strftime('%Y-%m-%d'),
        'total_value': total_value,
        'payment_type': random.choice(['credit_card', 'debit_card', 'pix', 'boleto']),
        'status': random.choice(['completed', 'pending', 'cancelled'])
    })

orders_df = pd.DataFrame(orders_data)
orders_df.to_csv('data/orders.csv', index=False)

# Também salvar em JSON
orders_json = orders_df.to_dict('records')
with open('data/orders.json', 'w') as f:
    json.dump(orders_json, f, indent=2, default=str)

print("✅ Dados de exemplo criados:")
print(f"- Clientes: {len(customers_df)} registros")
print(f"- Pedidos: {len(orders_df)} registros")
print(f"- Arquivos salvos: data/customers.csv, data/orders.csv, data/orders.json")

# Mostrar preview dos dados
print("\n📊 Preview dos dados de pedidos:")
print(orders_df.head())
print(f"\nValores nulos em total_value: {orders_df['total_value'].isnull().sum()}")
print(f"IDs duplicados: {orders_df['order_id'].duplicated().sum()}")
print(f"Valores negativos: {(orders_df['total_value'] < 0).sum()}")