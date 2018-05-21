# WildFire
Simulation of wildfire spread using cellular automaton.

## TODO:
* Grzesiek
  - zrobic mapy (material, wysokosc, wilgotnosc, temepratura), kazda najlepiej w osobnym pliku txt
* Alex
  - zrobic metode zapalającą (ma ustawic status materialy na 3)
* Michał
  - rozpoczac pisanie wlasciwej symulacji

## NOTES:

1. Wiatr ma byc staly, jednolity na cala mape
1. Ogien na danej kratce przestaje sie palic tylko w dwoch wypadkach:
    - wypali sie paliwo
    - opad atmosferyczny zgasi ogien, jesli tak to ilosc paliwa pozostaje taka jak w ostatnim momencie palenia i zwieksza sie bardzo wilgotnosc
1. Im wyzsza temperatura ognia tym szybciej wypala on paliwo
1. Ogien rozprzestrzenia sie szybciej w kierunu wyzszych terenow oraz w kierunku wiania wiatru
1. Auto ignition jest to temperatura w ktorej nastepuje samozaplon
1. Flash point jest to temperatura w ktorej material podpala sie od otwartego ognia
1. Jeden cykl odpowiada jednej minucie
1. Kiedy kratka bedzie sie palic bedzie to sygnalizowane migajacym kolorem, im wolniej miga tym mniej jest paliwa na danej kratce a kolor materialu dazy do czarnego

oddawanie do max 21.05
obliczenia rownolegle z CUDA
