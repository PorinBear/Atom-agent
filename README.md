# Sentry

**AI Agentti Ohjaamo · powered by ATOM**

Sentry on käyttäjälle näkyvä pääagentti. ATOM on taustalla oleva agentti- ja työtila-alusta sekä koko projektiperheen tekninen pohja. Tämä repo näyttää projektin käyttäjälle näkyvän suunnan ja tällä hetkellä rakennetun ytimen — ei kaikkia sisäisiä toteutusratkaisuja.

## Sentryn animaatiot ja lasten versio

Sentryn keskushahmo ei ole vain koriste, vaan käyttöliittymän visuaalinen palaute. Animaatio voi reagoida esimerkiksi kuunteluun, puheeseen, ajatteluun, työn etenemiseen, valmistumiseen ja virhetilanteeseen. Ulkoasu/animaatio valitaan käyttäjän toimesta; vaihtoehtoja ei vaihdeta automaattisesti kesken käytön. Ensimmäiseen julkaisuun käytetään hyväksyttyjä still-kuvia, ja viisi valmista MP4-animaatiota säilytetään erillisinä vaihtoehtoina myöhempää käyttöliittymäpäivitystä varten.

### Lasten Sentry

Lasten versio on oma käyttökokemuksensa, ei vain aikuisten näkymä eri väreillä. Sen keskellä on ystävällinen virtuaalinen hahmo/kumppani ja käyttöliittymä on selkeämpi, rauhallisempi ja helpommin lähestyttävä. Lapsi voi valita hahmon tai ulkoasun itse.

Tavoitteena on digitaalinen kaveri, joka voi keskustella, neuvoa, auttaa tehtävissä ja muistuttaa sovituista asioista. Kokemus voi mukautua käytön myötä lapselle sopivaksi, mutta huoltajan asetukset, ikätasoinen sisältö, yksityisyys ja turvallisuus ovat erillisiä rajoja. Lasten versio ei saa tehdä itsenäisesti korkean vaikutuksen toimia lapsen puolesta.

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

## Sentry-ohjaamo

Sentryn käyttöliittymän tavoite ei ole tavallinen korttidashboard. Ohjaamo rakentuu selkeistä painikkeista, jatkuvasta tilapalautteesta ja agentin sekä käyttäjän välisestä vuorovaikutuksesta.

Käyttäjä näkee työn elinkaaren esimerkiksi:

**Kuuntelen → Suunnittelen → Haen tietoa → Analysoin → Kokoan → Valmis**

Sentry-ohjaamo yhdistää keskustelun, aktiivisen tehtävän, projektit, työkalut, selaimen, tiedostot, muistin ja tulokset samaan näkymään. Tarkoitus on, että käyttäjä näkee mitä ATOM tekee ilman että sisäinen toteutus paljastetaan.

### Näkymävalinta

Aikuisten ja lasten näkymät ovat käyttäjän itse valittavia. Aikuisten Sentry käyttää hillittyjä teknisiä teemoja; lasten Sentry toimii ystävällisempänä virtuaalisena kumppanina, joka neuvoo, auttaa, muistuttaa sovituista asioista ja kasvaa käyttökokemuksen mukana. Animaatiot ja teemat pidetään erillisinä vaihtoehtoina eikä niitä kierrätetä automaattisesti.

> Hyväksytyt media-assettit: 4 staattista näkymää + 5 animaatiotiedostoa, julkaisuassetit päivitetään alkuperäistiedostoista.



## Periaate

ATOM automatisoi rutiinia ja palautettavia työvaiheita. Ulkoiset, peruuttamattomat tai merkittävät toimet kuuluvat hyväksyntärajan taakse.

## Julkinen vs. sisäinen

Julkisesti voidaan näyttää käyttökokemus, työn eteneminen ja tuotteen yleiset kyvykkyydet. Tunnukset, avaimet, selainistunnot, asiakasdata, sisäinen deploy-rakenne ja kilpailuetua tuovat keskeneräiset yksityiskohdat eivät kuulu julkiseen repoon.
