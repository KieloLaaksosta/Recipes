# Reseptit

## Sovelluksen toiminnot

* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
* Käyttäjät voivat jakaa reseptejään muille sovelluksen käyttäjille.
* Respeteistä löytyy lista tarvittavista raaka-aineista sekä valmistusohje. Lisäksi resepteille voi antaa tunnisteita kuten vegaainen, alle 15 min, levonnaiset yms.
* Käyttäjät pystyvät arvostelemaan ja kommentoimaan reseptejä.
* Käyttäjä pystyy etsimään reseptejä hakusanalla ja rajaamaan tuloksia tunnisteiden avulla.
* Käyttäjä pystyy poistamaan ja muokkaamaan omia reseptejään ja arvioutaan.
* Sovelluksessa on käyttäjäsivut, jotka näyttävät tilastoja ja käyttäjän lisäämät respetit ja arvostelut.

## Sovelluksen asennus

Asenna `flask`-kirjasto:

```bash
$ pip install flask
```

Luo tietokannan taulut ja lisää alkutiedot:

```bash
$ sqlite3 database.db < schema.sql
$ sqlite3 database.db < init.sql
$ sqlite3 database.db < index.sql
```

Voit käynnistää sovelluksen näin:

```bash
$ flask run
```

Pylintin antaman tuloksen arvionti on tiedostossa pylint.md 

# Suuri tietomäärä

Sovellustan on testattu seuraavilla määrillä kehitys pavelimella (development build):

    Käyttäjiä: 1000
    Reseptejä: 100 000
    Arvosteluja: 1 000 000
    Tunnisteita (resepteillä keskimäärin 2 tunnistetta): 6

Tällöin haku ilman mitään ehtoja kesti 1.55 s

Haku tunnisteet: tiukkaan budjettiin ja laktoositon ja haku sana "name3" kesti 0.2 s

Käyttäjä sivun hakeminen kesti 1.68 s

Resepti sivun hakeminen oli välitöntä 0.0 s