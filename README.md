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

## Dados

Um conjunto de dados (disponível [aqui](calls.csv)) obtidos da empresa registra os timestamps de quando uma chamada foi recebida, quando a chamada foi atendida, e quando a chamada foi concluída. Além disso, contém o registro do tipo de ligação segundo suas características. Os tempos totais de espera e serviço são calculados, assim como uma marcação para saber se a chamada foi atendida dentro do padrão de desempenho.
