# %%
import pandas as pd
import plotly.express as px
import numpy as np
import seaborn as sns
from fitter import Fitter, get_common_distributions, get_distributions
from datetime import datetime

# %% [markdown]
# # Base de dados das ligações

# %%
# Leitura dos dados
df = pd.read_csv("calls.csv")

# Conversão do time stamp da data
df["date"] = pd.to_datetime(df.date, format="%d/%m/%Y")
df["call_started"] = pd.to_datetime(df.call_started, format="%I:%M:%S %p")

# %%
df.head()

# %% [markdown]
# O gerente deseja que 90% das chamadas sejam atendidas em até um minuto

# %%
# Chamadas que aguardam mais de um minuto (60 segundos)
df.loc[df["wait_length"] > 60].head()

# %% [markdown]
# ## Análise anual

# %%
# Número de chamadas analisadas
n = len(df)  # 51708

# Chamadas que demoraram mais de um minuto para serem atendidas
falhas = df.loc[df["wait_length"] > 60]
qtd_falhas = len(falhas)  # 4227

# Percentual anual de falhas
print(f"No ano de 2021, em média, {(qtd_falhas / n) * 100 :.2f}% das ligações demoraram mais de 60 segundos para serem atendidas")

# %% [markdown]
# ### Distribuição de ligações

# %%
# Quantidade de dias comerciais registrados
len(df["date"].unique())

# %%
# Agrupando ligações por dia
ligacoes = df.groupby(["date"])["daily_caller"].max()
ligacoes.head()

# %%
# Mostra a tendência de ligações por dia ao longo do ano
fig = px.line(ligacoes)
fig.show()

# %% [markdown]
# ### Estatística descritiva

# %%
# Tempo médio de espera
print("Descrição do Tempo de Espera: \n",df["wait_length"].describe(),"\n","-"*100)
print("\n","Descrição das ligações:",ligacoes.describe())

# %%
# Boxplot tempo de espera
fig = px.box(df, y="wait_length")
fig.show()

# %%
# Tempo médio de serviço
df["service_length"].describe()

# %%
# Boxplot tempo de serviço
fig = px.box(df, y="service_length")
fig.show()

# %%
# Save wait times
# np.savetxt(r".\times\wait_times.txt", df["wait_length"].values, fmt='%d')
# Save service times
# np.savetxt(r".\times\service_times.txt", df["service_length"].values, fmt='%d')

# %% [markdown]
# #### Fit dos tempos de serviço

# %%
fig = px.histogram(df, x="service_length")
fig.show()

# %%
tempos_servico = df["service_length"].values
f = Fitter(tempos_servico, distributions=get_common_distributions())
f.fit()
f.summary()

# %%
# Melhor fit para tempos de serviço é exponencial
f.get_best(method = 'sumsquare_error')

# %%
# Exponencial de média 299,1
f.fitted_param["expon"]

# %%
#criando nova coluna no DF
df["arrival_time"] = (df["call_started"].sub(df["call_started"].shift(1)))

df["arrival_time"][0] = 0
time_series = df.iloc[:,10].astype("timedelta64[s]")
time_series = time_series.dt.total_seconds()
df["arrival_time"] = time_series

print(type(df["arrival_time"][2]))

df.head()



# %%



