# Clientes com assinatura pausada

import pandas as pd

df = pd.read_csv("/content/data-test-analytics_5.csv")

paused = df['status'] == 'paused'
paused = paused.sort_values(ascending=False)
sum(paused)

active = df['status'] == 'active'
active = active.sort_values(ascending=False)
sum(paused)

canceled = df['status'] == 'canceled'
canceled = canceled.sort_values(ascending=False)
sum(paused)

import matplotlib.pyplot as plt

quantidades = df['status'].value_counts()

plt.bar(quantidades.index, quantidades.values, width=0.2)

plt.xlabel('Status')
plt.ylabel('Quantidade')
plt.title('Quantidades de clientes ativos, pausados e cancelados')

for i, value in enumerate(quantidades.values):
    plt.annotate(str(value), xy=(i, value), ha='center', va='bottom')

plt.show()


# Tempo desde a última compra do cliente

data_referencia = pd.Timestamp('2021-02-16')

limite_tempo = data_referencia - pd.DateOffset(days=45)

df['last_date_purchase'] = pd.to_datetime(df['last_date_purchase'])

churn = df[(df['last_date_purchase'] < limite_tempo) & (df['status'] == 'active')]

len(churn)

# Queda no valor médio de gasto por pedido

data_analise = pd.to_datetime('2021-02-16')

clientes_ativos = df[df['status'] == 'active'].copy()

clientes_ativos['created_at'] = pd.to_datetime(clientes_ativos['created_at'])

clientes_ativos['Media_Gasto_Desde_Criacao'] = clientes_ativos.apply(lambda row: clientes_ativos[(clientes_ativos['created_at'] <= row['created_at']) & (clientes_ativos['created_at'] <= data_analise)]['average_ticket'].mean(), axis=1)

clientes_queda = clientes_ativos[clientes_ativos['average_ticket'] < clientes_ativos['Media_Gasto_Desde_Criacao']]

clientes_queda.head(1000)

# Churn por Estado

import matplotlib.pyplot as plt

cancelados_por_estado = df[df['status'] == 'canceled'].groupby('state').size()
cancelados_por_estado = cancelados_por_estado.sort_values(ascending=False)

tabela_cancelados_por_estado = pd.DataFrame({'Estado': cancelados_por_estado.index, 'Cancelados': cancelados_por_estado.values})

plt.figure(figsize=(10, 6))

estados = tabela_cancelados_por_estado['Estado']
cancelamentos = tabela_cancelados_por_estado['Cancelados']

plt.bar(estados, cancelamentos)

for i in range(len(estados)):
    plt.text(estados[i], cancelamentos[i], str(cancelamentos[i]), ha='center', va='bottom')

plt.title('Churn por Estado')
plt.xlabel('Estado')
plt.ylabel('Número de Cancelamentos')

plt.xticks(rotation=45)

plt.show()

# Churn por idade

from datetime import datetime

df['birth_date'] = pd.to_datetime(df['birth_date'])

data_atual = datetime.now()

df['idade'] = (data_atual - df['birth_date']).astype('<m8[Y]')

faixas_idade = [0, 18, 25, 35, 45, 55, float('inf')]
labels_faixas = ['0-18', '19-25', '26-35', '36-45', '46-55', '55+']

df['faixa_idade'] = pd.cut(df['idade'], bins=faixas_idade, labels=labels_faixas)

cancelamentos_por_idade = df[df['status'] == 'canceled'].groupby('faixa_idade').size()

print(cancelamentos_por_idade)

 
import matplotlib.pyplot as plt

cancelados_por_idade = df[df['status'] == 'canceled'].groupby('faixa_idade').size().reset_index(name='Cancelamentos')

tabela_cancelamentos_por_idade = pd.DataFrame(cancelados_por_idade)

plt.figure(figsize=(7, 3))

faixas_idade = tabela_cancelamentos_por_idade['faixa_idade']
cancelamentos = tabela_cancelamentos_por_idade['Cancelamentos']

plt.bar(faixas_idade, cancelamentos)

plt.title('Cancelamentos por Faixa de Idade')
plt.xlabel('Faixa de Idade')
plt.ylabel('Número de Cancelamentos')

plt.xticks(rotation=45)

plt.show()

# Receita perdida em razão do Churn

clientes_cancelados = df[df['status'] == 'canceled']

media_receita_cancelados = clientes_cancelados['all_revenue'].mean()

print(media_receita_cancelados)