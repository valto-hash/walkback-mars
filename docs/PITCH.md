# WALKBACK | 3-minute pitch notes (Português)

Use only if the local event asks for a live pitch. The official demonstration is the seven-slide English presentation in `presentation.html`.

## Slide 1 — Can you get back in time?

“Em Marte, planejar uma caminhada não é apenas escolher o caminho mais curto. É comparar a estimativa de retorno com os recursos de suporte à vida e com uma janela de aviso. O WALKBACK transforma essa pergunta em uma visualização interativa para Jezero, usando waypoints reais do Perseverance e deixando as hipóteses visíveis.”

## Slide 2 — The challenge

“O desafio pede uma visualização em camadas que reúna dados científicos para apoiar o planejamento de caminhadas humanas em Marte. Segurança, eficiência e retorno científico precisam ser considerados juntos. Jezero tem uma rota real do Perseverance, o que permite comparar a geometria da proposta com deslocamentos de um rover.”

## Slide 3 — What is implemented

“O protótipo tem uma cena 3D, a rota do rover, pontos de interesse, perfil de elevação, câmera em primeira pessoa, triagem de inclinação, envelopes de tempo e visada geométrica de rádio. Os waypoints do Mars 2020 estão embutidos. Também adicionamos uma ferramenta opcional para processar e importar o MDE CTX do MRO, mas esse arquivo precisa ser baixado e carregado pelo usuário.”

## Slide 4 — Two budgets, four states

“O envelope azul/verde/laranja/vermelho compara duas condições independentes: o orçamento de tempo de retorno derivado do suporte de vida e a janela hipotética de aviso inserida pelo usuário. Há também um relógio demonstrativo acelerado, em que um minuto simulado passa a cada segundo real, atualizando o mapa. Somente verde passa pelos dois limites. A janela não é uma previsão de tempestade solar e não calcula dose de radiação.”

## Slide 5 — Model and uncertainty

“O custo de caminhada usa o polinômio de Minetti para inclinação, medido em esteira na Terra, e uma hipótese de sensibilidade para 0,38 g. A hipótese não é uma validação para astronautas em trajes. O solver trabalha em células de aproximadamente 215 metros, e o relevo padrão é procedural fora do corredor do rover. Por isso, o projeto é um protótipo exploratório, não um sistema certificado de segurança.”

## Slide 6 — Route comparison

“Entre os pontos selecionados, os segmentos retos propostos somam aproximadamente 12,2 quilômetros. O odômetro do Perseverance registra cerca de 32,3 quilômetros nos segmentos correspondentes. A soma das variações positivas de altitude entre os pontos selecionados é aproximadamente 784 metros entre as âncoras selecionadas. Esses números comparam geometria e não demonstram que a rota seja caminhável por humanos.”

## Slide 7 — What comes next

“Os próximos passos são carregar o MDE CTX real, integrar outras camadas orbitais e geológicas, aumentar a resolução do solver, modelar solo e energia, integrar previsão de eventos solares e dose de radiação, e validar o modelo com especialistas em atividade extraveicular. Nossa prioridade é distinguir claramente dados medidos, estimativas e hipóteses.”