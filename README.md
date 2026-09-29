# ATOM AI

ATOM on jatkuvasti kehittyvä agentti- ja työtila-alusta. Tämä repo näyttää projektin käyttäjälle näkyvän suunnan ja tällä hetkellä rakennetun ytimen — ei kaikkia sisäisiä toteutusratkaisuja.

## Viimeisin kehityspäivitys — työn alla

Nykyinen varmennettu kehityslinja sisältää:
- jatkuvan agenttisilmukan ja taustatyön
- prioriteetti- ja resurssienhallinnan
- tavoitegraafin, riippuvuudet, blocker-tilat ja etenemisen
- selain- ja tutkimustyökalujen orkestroinnin
- muistia ja hallittua oppimista
- PWA-käyttöliittymän
- provider/model-routingin pohjan
- lokituksen ja turvallisen hyväksyntämallin jatkokehityksen

Kehitys jatkuu. Julkinen README ei ole täydellinen tekninen inventaario eikä lupaus siitä, että kaikki suunnitellut ominaisuudet ovat jo tuotannossa.

## Ohjaamo

ATOMin käyttöliittymän tavoite ei ole tavallinen korttidashboard. Ohjaamo rakentuu selkeistä painikkeista, jatkuvasta tilapalautteesta ja agentin sekä käyttäjän välisestä vuorovaikutuksesta.

Käyttäjä näkee työn elinkaaren esimerkiksi:

**Kuuntelen → Suunnittelen → Haen tietoa → Analysoin → Kokoan → Valmis**

Ohjaamo yhdistää keskustelun, aktiivisen tehtävän, projektit, työkalut, selaimen, tiedostot, muistin ja tulokset samaan näkymään. Tarkoitus on, että käyttäjä näkee mitä ATOM tekee ilman että sisäinen toteutus paljastetaan.

![ATOM live-ohjaamo](docs/images/atom-live-cockpit.png)

![ATOM työtila](docs/images/atom-live-workspace.png)

## Periaate

ATOM automatisoi rutiinia ja palautettavia työvaiheita. Ulkoiset, peruuttamattomat tai merkittävät toimet kuuluvat hyväksyntärajan taakse.

## Julkinen vs. sisäinen

Julkisesti voidaan näyttää käyttökokemus, työn eteneminen ja tuotteen yleiset kyvykkyydet. Tunnukset, avaimet, selainistunnot, asiakasdata, sisäinen deploy-rakenne ja kilpailuetua tuovat keskeneräiset yksityiskohdat eivät kuulu julkiseen repoon.
