# Recipe

## Sovelluksen toiminnot

* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
* Käyttäjät voivat jakaa reseptejään muille sovelluksen käyttäjille.
* Respeteistä löytyy lista tarvittavista raaka-aineista sekä valmistusohje. Lisäksi resepteille voi antaa tunnisteita kuten vegaainen, alle 15 min, levonnaiset yms.
* Käyttäjät pystyvät arvostelemaan ja kommentoimaan reseptejä.
* Käyttäjä pystyy etsimään respetejä hakusanalla ja rajaamaan tuloksia tunnisteiden avulla.
* Sovelluksessa on käyttäjäsivut, jotka näyttävät tilastoja ja käyttäjän lisäämät respetit ja arvostelut.

## Sovelluksen asennus

Asenna `flask`-kirjasto:

```
$ pip install flask
```

Luo tietokannan taulut ja lisää alkutiedot:

```
$ sqlite3 database.db < schema.sql
$ sqlite3 database.db < init.sql
```

Voit käynnistää sovelluksen näin:

```
$ flask run
```