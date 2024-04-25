# DataParser
OBS:
A planilha fluxo, que mostra desistências tem um atributo chamado total de desistência acomulada... (TODA), por isso eu mudei a tabela para só conter os anos de referência de 2019, como a gente já tem um percentual do total de desistências, depois se quisermos análisar a quantia de desistência em cada ano depois do ingresso podemos usar a tabela inteira, na verdade talvez nem demore muito.

Algumas universidade tem dois cursos de mesmo nome, por enquanto só adicionei o código delas para ser possível distiguir, mas no futuro talvez a gente possa pegar apenas o curso com mais participantes, já que imagino que alguns desses cursos repetidos podem ser por causa de alguma burocracia e eles não foram efetuados completamente.

Gráficos com numPy:
A minha ideia seria fazer um gráfico para cada curso onde os pontos são as universidades, o eixo y é a porcentagem total de desistências ao longo de uma década e o eixo x é a quantia de bolsas da prouni ofertadas.
Aí podemos fazer uma reta que aproxima os pontos. A partir disso também é possível calcular alguns índices que indicam o quão relacionados são os dados dos eixos, Se não me engano a a gente viu o coeficiente de correlação linear de Pearson.
