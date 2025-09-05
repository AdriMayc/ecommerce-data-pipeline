#  🔷 E-commerce Data Pipeline

Este repositório implementa um pipeline de dados fim a fim para e-commerce, cobrindo toda a jornada:

- Ingestão (CSV/JSON)
- Validação e qualidade
- Armazenamento em **Data Lake (S3)**
- Transformações **(AWS Glue)**
- Carga em **Data Warehouse (PostgreSQL)**
- Dashboards de monitoramento **(Superset/Metabase)**

##  🔶 Documentação por Etapa
Todos os guias detalhados estão na pasta [readmes/](readmes/)
 
1. [Ambiente e Setup](readmes/01-ambiente.md)
2. [Extração de Dados](readmes/02-extracao.md)
3. [Validação e Limpeza](readmes/03-validacao.md)
4. [Data Lake (S3)](readmes/04-datalake.md)
5. [Transformações (Glue)](readmes/05-transformacoes-glue.md)
6. [Data Warehouse (PostgreSQL)](readmes/06-carga-warehouse.md)
7. [Monitoramento e Dashboards](readmes/07-monitoramento-dashboards.md)
 
##  🔶 Motivação

Imagine um e-commerce em crescimento que processa milhares de pedidos por dia. O time de negócios precisa de **relatórios de vendas, churn e margens**, mas enfrenta problemas:

- 📉 **Pedidos duplicados ou incompletos** (valores inválidos, datas faltando).
- ⚠️ **KPIs divergentes** entre relatórios.
- 📊 **Processos manuais** para união de planilhas CSV/JSON.
- ⏱️ **Métricas lentas e sem monitoramento** (dias de atraso).

Um pipeline robusto, automatizado e monitorado resolve esses pontos ao:

- Garantir consistência e confiabilidade.
- Centralizar dados em um **Data Warehouse PostgreSQL.**
- Automatizar ingestão → transformação → dashboards.
- Permitir **decisões estratégicas em tempo real.**

##  🔶 Guia Passo a Passo

Cada tópico possui um guia detalhado em um README específico.

### 🔻 Ambiente

- Repositório Git, virtualenv/Poetry, variáveis de ambiente, Docker.

- Stack: Python (Pandas + boto3), PostgreSQL, AWS (S3, Glue), Superset/Metabase.

>📖 Guia: [01-ambiente.md](readmes/01-ambiente.md)

---

### 🔻 Extração de dados (CSV/JSON)

- Simulação de pedidos.

- Script Python para ingestão + metadados.

>📖 Guia: [02-extracao.md](readmes/02-extracao.md)

---

### 🔻 Validação e limpeza

- Verificação de nulos, duplicatas, formatos.

- Relatórios de erros (PASS/FAIL).

>📖 Guia: [03-validacao.md](readmes/03-validacao.md)

---

### 🔻 Data Lake (S3)

- Buckets organizados: raw → curated → processed.

- Particionamento por data.

>📖 Guia: [04-datalake-s3.md](readmes/04-datalake.md)

---

### 🔻 Transformações

- Glue: batch inicial.

>📖 Guia: [05-transformacoes-dbt-glue.md](readmes/05-transformacoes-dbt-glue.md)

---

### 🔻 Carga no Data Warehouse

- Esquema analítico, tabelas dimensão/fato.

>📖 Guia: [06-carga-warehouse.md](readmes/06-carga-warehouse.md)

---

### 🔻 Monitoramento e Dashboards

- KPIs: receita, ticket médio, pedidos.

>📖 Guia: [07-monitoramento-dashboards.md](readmes/07-monitoramento-dashboards.md)


## 🔷 Encerramento

Este pipeline mostra a conversão de dados brutos de e-commerce em métricas confiáveis e painéis de fácil acesso. Ele assegura qualidade e transparência, e está pronto para orquestração futura, caso haja necessidade de execuções recorrentes.

> Obrigado por conferir este projeto! 

---

Para conhecer mais sobre meus projetos e perfil profissional:

- 🌐 Portfólio: [www.adrianomayco.site](https://portfolio-adriano-mayco.vercel.app)  
- 💼 LinkedIn: [linkedin.com/in/adriano-mayco/](https://www.linkedin.com/in/adriano-mayco/)  
- ✉️ E-mail: [contato@adrianomayco.site](mailto:contato@adrianomayco.site)


<hr style="height:2px; background-color:#807f7e; border:none;">

