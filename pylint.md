# Pylint arvio

Pylintin antamat virheet jakautuvat kolmeen luokaan: 

  - liian pitkät rivit

  - moduulin tuonti epäonnistuu

  - dokumentaatio puuttuu

  - Kaikki virheet tunnistetaan try catch lohkolla.

Ei keskitytyä benchmarking tiedostoon, sillä se ei kuulu itse sovellukseen.

## Moduulien tuonti epäonnistuu

Moduulien tuonnin epäonnistuminen ei johdu virheestä ohjelmassa vaan virheestä pylintin määritelyssä. 
Onneksi tämä ei merkittävästi vaiktua saatuun palautteeseen, joten pylintin säätämiseen ei vaivauduta käyttämään aikaa.

## Pitkät rivit

### recipes.py
Kaikki rivit ovat lähellä pylintin oletus maksimi pituutta 100 merkkiä. Tarkastetaan kuitenkin nämä rivit.

Liian pitkiä rivejä on:

  - error_msg = f"Reseptin nimen tulee olla vähintään {validation.MIN_RECIPE_NAME_LENGTH} merkkiä pitkä."W

  - error_msgs.append(f"Käyttänimen tulee olla enintään {validation.MAX_USERNAME_LENGTH} merkkiä pitkä.")

  - error_msgs.append(f"Salasanan tulee olla vähintään {validation.MIN_PASSWORD_LENGHT} merkkiä pitkä.")

  - error_msgs.append(f"Salasanan tulee olla enintään {validation.MAX_PASSWORD_LENGHT} merkkiä pitkä.")

Loputkin rivit ovat virhe viestejen lisäämistä.

On hyväksyttävää, että pitkät virheviestit asetetaan pitkillä riveillä, sillä viestejä ei voida jakaa useampaan riviin ilman, että virhe viestiinkin tulee ylimääräisiä rivejä. Rivejä, joilla virhe viesti lisätään listan voitaisiin lythentää hieman, apumuuttujan avulla, mutta tämä vain huonontaisi luettavuutta.

### Dokumentaatio

Ohjelma on tähän mennessä simppeli, ja sillä on vain yksi kehittäjä. Dokumentaatio ei ole siis ollut tähän menenssä tarpeellista. Hyvässä koodissa funkiot pitäisi kommentoida, mutta tätä pientä kurssi projektia varten siihen ei ryhdytty.