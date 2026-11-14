# WALKBACK | Roteiro de fala (PT-BR)

Apresentação pública em inglês, com 7 slides. Este roteiro em português acompanha a apresentação interativa em `presentation.html`. Duração aproximada: 3 minutos. O pitch oral só deve ser usado se o evento local solicitar.

## Slide 1 — Can you get back in time? (~20 s)

“Em Marte, planejar uma caminhada não é apenas escolher o caminho mais curto. É saber se a equipe consegue retornar com os consumíveis disponíveis e alcançar um abrigo dentro de uma janela de aviso. O WALKBACK transforma essa pergunta em uma visualização interativa para Jezero, usando dados reais do Perseverance e deixando as simplificações visíveis.”

## Slide 2 — The challenge (~25 s)

“O desafio pede uma visualização em camadas que combine dados científicos para apoiar caminhadas humanas em Marte. Segurança, eficiência e retorno científico precisam ser analisados juntos. Jezero é uma boa escolha porque preserva registros de um antigo sistema de rio e lago e também possui uma rota real do Perseverance, que permite comparar a geometria do nosso planejamento com dados de um rover.”

## Slide 3 — The prototype (~25 s)

“O protótipo reúne a rota do Perseverance, uma rota humana proposta entre pontos de interesse e uma cena 3D interativa. O usuário pode explorar em primeira pessoa, selecionar o abrigo, ajustar parâmetros de retorno, visualizar inclinação e analisar a visada de rádio. Há sete paradas científicas propostas e interface em português, inglês, espanhol e alemão.”

## Slide 4 — Two safety envelopes (~30 s)

“A principal contribuição do WALKBACK é separar dois limites. O envelope azul estima o retorno a pé com base nos consumíveis restantes, velocidade configurada e margem. O envelope verde estima se o abrigo pode ser alcançado antes do intervalo de aviso selecionado. O motor usa Dijkstra sobre uma grade e uma função de caminhada inspirada em Tobler. Os valores são parâmetros de demonstração, não especificações reais de traje nem limites certificados.”

## Slide 5 — Data and uncertainty (~30 s)

“Hoje, os dados embutidos são os waypoints do Mars 2020, com posição, altitude e odômetro. Fora do corredor do rover, o relevo é procedural; a inclinação usa uma grade de aproximadamente 200 metros, e o modelo de caminhada ainda não corrige a gravidade de Marte. Não há camadas integradas de solo, energia solar ou dose local de radiação. O aviso verde usa uma janela configurável, não uma previsão real de tempestade. Por isso, este é um protótipo exploratório, não um sistema certificado de segurança.”

## Slide 6 — Route comparison (~25 s)

“Entre os pontos selecionados, a rota humana proposta em segmentos retos soma cerca de 12,2 quilômetros. O odômetro do Perseverance registra aproximadamente 32,3 quilômetros e a subida acumulada fica perto de 784 metros. O rover fez desvios para investigar alvos científicos. Esses números servem como referência de geometria e plausibilidade, não como prova de que a rota seja caminhável por humanos.”

## Slide 7 — Next steps (~25 s)

“O próximo passo é aumentar a fidelidade dos dados e do modelo: substituir o terreno procedural por um modelo digital de terreno real, integrar camadas mineralógicas e geológicas, ajustar o custo de caminhada à gravidade marciana e incorporar parâmetros de traje e radiação validados. Energia solar, poeira e comunicação também precisam entrar no planejamento. A mesma arquitetura pode inspirar aplicações na Lua e em áreas remotas da Terra, mas esses modos ainda não estão implementados. Nosso compromisso é mostrar o que já funciona e o que ainda precisa de validação.”
