# Projectvoorstel "NAAM APPLICATIE"

## Samenvatting
Onze webapplicatie “NAAM APPLICATIE” zal een combinatie zijn tussen trivia en een bordspel. Je kan je samen met je vrienden/familie opgeven binnen hetzelfde team, zodat je tegen elkaar kan spelen. Met behulp van een dobbelsteen zet je stapjes vooruit waarna je uit verschillende categorieën een vraag kan krijgen. Door de vraag goed en binnen de tijd te beantwoorden scoor je extra punten waardoor je verder vooruit kan.De vragen zullen voor alle deelnemers op niveau zijn, om verschillen in leeftijd op te vangen. Door dit spel kunnen de spelers een competitief spel spelen en zorgt dit voor vermaak. Laat het spel beginnen!

## Features
Grote, noodzakelijke features:
- Een bord waarop de locatie van de spelers zichtbaar is.
- Registratie waardoor de spelers zich kunnen identificeren in een spel.
- Lobbycode die spelers kunnen invoeren om in hetzelfde spel terecht te komen.
- Veld om een naam in te vullen, zodat de spelers op het bord worden geïdentificeerd.
- Bewegingssysteem, zodat de spelers na het gooien van een dobbelsteen stapjes vooruit kunnen zetten.
- API vragen uit verschillende categorieën.
- Winst-pagina waarbij de spelers van het spel kunnen zien wie het spel heeft gewonnen als dit is afgelopen.
- Timers om het spel niet al te lang te laten duren.
- Timer per vraag: de speler heeft 20/30 seconden de tijd om de vraag goed te beantwoorden.
- Timer beurt: als er weer een nieuwe speler aan de beurt is heeft deze 48 uur de tijd om zijn volgende vraag te beantwoorden, anders wordt deze beurt overgeslagen.

Kleine features:
- Speciale vakjes op het bord, waarbij je je bijvoorbeeld 5 plaatsen vooruit/terug moet verplaatsen.
- Verschillende borden met een ander aantal tegels, waardoor ook de spel duur kan variëren.
- Verschillende borden in moeilijkheidsgraad, dus makkelijk - gemiddeld - moeilijk.

## Afhankelijkheden
- <http://jservice.io> is een mogelijke API die te gebruiken is als bron voor de vragen in het spel.
- <https://www.funnygames.nl/spel/trivia.html>
- Bootstrap voor het gebruiken van de navbar
- ... voor de hexagons op het spelbord
- ... voor het weergeven van de vragen

Moeilijkheden die wij verder in het project waarschijnlijk tegen gaan komen zijn:
- Zorgen dat de spelers over het bord kunnen bewegen
- Zorgen dat de spelers in dezelfde room komen te zitten

## Controller


## Views
Onderstaande afbeelding laat zien welke vereisten we op elk scherm willen tonen en welke schermen allemaal nodig zijn. Daarnaast geven de pijlen aan hoe je voornamelijk door middel van buttons tussen de verschillende templates kunt bewegen.
![Ontwerp spel](doc/IMG_4141.HEIC)

## Models
De helpers functies waar wij gebruik van gaan maken zijn

Login_required:
Voorkomt dat gebruikers pagina’s zullen bezoeken waar ze niet het juiste pad voor hebben afgelegd.

Apology:
Efficiënte manier om de gebruiker een indicatie te geven wat er moet gebeuren als er iets fout gaat.