# PEANUTS

De studenten die aan dit project hebben meegewerkt zijn Renske de Leeuw, Thomas Koene en Wouter Knibbe.

## Samenvatting
Onze webapplicatie PEANUTS zal een combinatie zijn tussen trivia en een bordspel. Je kan je samen met je vrienden/familie opgeven binnen hetzelfde team met een zelfgekozen moeilijkheidsgraad, zodat je tegen elkaar kan spelen. Met behulp van een dobbelsteen zet je stapjes vooruit waarna je uit verschillende categorieën een vraag kan krijgen. Door de vraag goed en binnen de tijd te beantwoorden scoor je extra punten waardoor je verder vooruit kan. Door dit spel kunnen de spelers een competitief spel spelen en zorgt dit voor vermaak. Laat het spel beginnen!

## Features
- Een bord waarop de locatie van de spelers zichtbaar is.
- Registratie waardoor de spelers zich kunnen identificeren in een spel.
- Lobbycode die spelers kunnen invoeren om in hetzelfde spel terecht te komen.
- Bewegingssysteem, zodat de spelers na het gooien van een dobbelsteen stapjes vooruit kunnen zetten.
- API vragen uit verschillende categorieën.
- Winst-pagina waarbij de spelers van het spel kunnen zien of ze het spel hebben gewonnen of verloren.
- Timers om het spel niet al te lang te laten duren.
  - Timer per vraag: de speler heeft 15 seconden de tijd om de vraag goed te beantwoorden.
  - Timer beurt: als er weer een nieuwe speler aan de beurt is heeft deze 24 uur de tijd om zijn volgende vraag te    beantwoorden, anders wordt de speler uit het spel verwijderd.
- Speciale vakjes op het bord, waarbij je je bijvoorbeeld 2 plaatsen vooruit/terug moet verplaatsen.

## Samenwerking
Wouter: heeft het grootste deel aan het bord bijgedragen. Hij heeft ervoor gezorgd dat het bord er staat, dat er een dobbelsteen kan worden gegooid en dat de spelers over het bord kunnen bewegen.

Thomas: heeft ervoor gezorgd dat de vragengenerator werkt, evenals de opmaak van de vragenpagina. Daarnaast kunnen spelers aangeven welk antwoord zij denken dat juist is, en wordt er gecheckt of dit het goede antwoord is.

Renske: heeft ervoor gezorgd dat alle spelers zich kunnen registreren en identificeren. Daarnaast heeft Renske het grootste deel van de layout gedaan en ervoor gezorgd dat de site automatisch refresht. Ook is zijn door Renske helpers functies toegevoegd om o.a. de data uit de database op te vragen.

## Afhankelijkheden
- <https://opentdb.com/> is een mogelijke API die te gebruiken is als bron voor de vragen in het spel.
- Bootstrap voor het gebruiken van de navbar en buttons.
- <https://stackoverflow.com/a/10068351> voor de hexagons op het spelbord.
- <https://github.com/jamesqquick/Build-A-Quiz-App-With-HTML-CSS-and-JavaScript/tree/master/11.%20Fetch%20API%20Questions%20from%20Open%20Trivia%20API> voor het weergeven van de vragen.
- <https://unpkg.com/sweetalert/dist/sweetalert.min.js> om te laten zien of de vraag goed of fout is beantwoord.

Moeilijkheden die wij verder in het project waarschijnlijk tegen gaan komen zijn:
- Zorgen dat de spelers over het bord kunnen bewegen
- Zorgen dat de spelers in dezelfde room komen te zitten
- Zorgen dat de vragen mooi worden weergegeven
- De implementatie van socket.io, waarna werd afgeraden om die nog toe te voegen, dus een automatische refresher
- De database die moet worden geüpdate.

## Controller
De lijst van routes en de methods zijn te vinden in application.py

## Views
Onderstaande afbeelding laat zien welke vereisten we op elk scherm willen tonen en welke schermen allemaal nodig zijn. Daarnaast geven de pijlen aan hoe je voornamelijk door middel van buttons tussen de verschillende templates kunt bewegen.
![Bekijk een screenshot van de website](webIK/doc/Board.png)

## Models
De helpers functies waar wij gebruik van gaan maken zijn
- Login_required: Voorkomt dat gebruikers pagina’s zullen bezoeken waar ze niet het juiste pad voor hebben afgelegd.
- Apology: Efficiënte manier om de gebruiker een indicatie te geven wat er moet gebeuren als er iets fout gaat.
- Add_player: Deze functie voegt een speler toe aan de database als deze een nieuwe room maakt of zich aansluit bij een bestaande room.
- Delete_player: Deze functie verwijdert een speler uit een spel als deze speler niet binnen 1 dag zijn beurt volbrengt of het spel is gewonnen door een speler.
- Player_data: Verzamelt de data van de speler die is ingelogd.
- Board_data: Verzameld de data van alle spelers die in dezelfde room zitten als de speler die is ingelogd.

Daarnaast hebben we gebruik gemaakt van een mapje doc waar de screenshot van het bordspel in te vinden is. Alle css files zijn in het mapje static te vinden en in het mapje templates zijn alle html-templates te vinden.

## Instructievideo
Een korte instructievideo (5 min) is te vinden op: https://youtu.be/cDNOuEegnRI