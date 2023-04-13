# Especificações do projeto

Considere uma central de atendimentos cujas linhas estão abertas das 8:00 às 18:00, de segunda a sexta-feira e quatro atendentes estão em serviço a qualquer hora e para qualquer ligação.

O gerente da central deve cumprir uma meta de desempenho de 90% das chamadas atendidas em até 1 minuto. Ultimamente, esta meta tem deixado de ser cumprida. 

O objetivo desse trabalho é analisar o desempenho da central de atendimentos e fazer recomendações para a central voltar a cumprir a meta, usando simulação de eventos discretos e análise de dados históricos. Algumas análises são esperadas pelo gerente, porém, ele não espera que as análises se limitem a seguinte lista:

* Qual é o volume máximo de chamadas que pode ser tratado e ainda atingir a meta de desempenho de 90%
das chamadas atendidas em 1 minuto?
* Construa um painel de controle para mostrar o gráfico de cada dia e os indicadores-chave de desempenho
(KPIs)
* Explore diferentes níveis de agregação (trimestral, mensal, semanal). Que nível é mais relevante para a gestão
da central de atendimentos?
* O que o gerente da central de atendimento deve fazer para devolver as operações ao desempenho?

# Dados

Um conjunto de dados (disponível [aqui](calls.csv)) obtidos da empresa registra os timestamps de quando uma chamada foi recebida, quando a chamada foi atendida, e quando a chamada foi concluída. Além disso, contém o registro do tipo de ligação segundo suas características. Os tempos totais de espera e serviço são calculados, assim como uma marcação para saber se a chamada foi atendida dentro do padrão de desempenho.

# Dashboard
O dashboard desenvolvido em Python com as bibliotecas Dash e Plotly apresentou os KPIs, para cada dia selecionado, do percentual de cumprimento da meta, número de atendimentos, tempo de espera para o percentil selecionado, tempo de atendimento para o percentil selecionado, taxa de desistência (ligações que duraram menos de 30 segundos) e taxa de utilização dos atendentes. Os gráficos interativos apresentam os valores do KPI para cada dia do mês selecionado. Diferentes visualizações, além do gráfico de barras, estão disponíveis, como histogramas, gráficos de dispersão e box plots.

![parte 1 dashboard](https://github.com/lucasgmalheiros/simulacao-call-center/blob/main/resultados/img/dash-1.png?raw=true)

![parte 2 dashboard](https://github.com/lucasgmalheiros/simulacao-call-center/blob/main/resultados/img/dash-2.png?raw=true)

![parte 3 dashboard](https://github.com/lucasgmalheiros/simulacao-call-center/blob/main/resultados/img/dash-3.png?raw=true)
