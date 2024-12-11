import pygame
import random
import pandas as pd


"""Funktionen um zu Prüfen, ob die felder in der Umgebung frei sind"""
def pruefe_links(x, y, feld):
    if feld[y][x - 1] == 1:
        return False
    else:
        return True

def pruefe_rechts(x, y, feld):
    if feld[y][x + 1] == 1:
        return False
    else:
        return True

def pruefe_oben(x, y, feld):
    if feld[y - 1][x] == 1:
        return False
    else:
        return True

def pruefe_unten(x, y, feld):
    if feld[y + 1][x] == 1:
        return False
    else:
        return True


"""Funktionen um Punkte auf dem Spielfeld zu verwalten"""
# schaut, ob noch Punkte auf dem Spielfeld sind
def pruefen_auf_2(feld):
    for y in range(len(feld)):
        for x in range(len(feld[y])):
            if feld[y][x] == 2:
                return False
    return True

# füllt Punkte auf, wenn alle weg sind
def punkte_auffuellen(feld, level):
    # Prüfen, ob alle `2` zu `0` geändert wurden
    if pruefen_auf_2(feld):
        for y in range(len(feld)):
            for x in range(len(feld[y])):
                if feld[y][x] == 0:
                    feld[y][x] = 2
        level += 1
    level_up = "Level: " + str(level)
    return level, level_up

# punkt einsammeln, wenn pacman in frisst
def punkt_einsammeln(feld, pacman_y, pacman_x, score, punkte):
    if feld[pacman_y][pacman_x] == 2:
        feld[pacman_y][pacman_x] = 0
        print("Pacman hat einen Punkt aufgesammelt")
        score += 25
        pygame.mixer.Sound.play(punkte)
    score_text = "Your Score: " + str(score)
    return score_text, score


"""Funktionen für die Geister"""
# mögliche Richtungen für Geist bestimmen
def ermittle_moegliche_richtungen(x, y, feld):
    richtungen = []
    if pruefe_links(x, y, feld):
        richtungen.append("links")
    if pruefe_rechts(x, y, feld):
        richtungen.append("rechts")
    if pruefe_oben(x, y, feld):
        richtungen.append("oben")
    if pruefe_unten(x, y, feld):
        richtungen.append("unten")
    return richtungen

# Geist in zufällige Richtung bewegen
def geist_bewegen(x, y, feld):
    moegliche_richtungen = ermittle_moegliche_richtungen(x, y, feld)

    #zufällige richtung auswählen
    richtung = random.choice(moegliche_richtungen)

    #geist in diese richtung bewegen
    if richtung == "links":
        x -= 1
    elif richtung == "rechts":
        x += 1
    elif richtung == "oben":
        y -= 1
    elif richtung == "unten":
        y += 1
    return x, y

# Geist zeichnen
def zeichne_geist(screen, x, y, farbe, multi, korrektur_breite, korrektur_hoehe):
    # Oberer Teil des Geistes (Kopf, runde Form)
    geist = pygame.draw.ellipse(screen, farbe, [x * multi + korrektur_breite, y * multi + korrektur_hoehe, 20, 20])

    # Unterer Teil des Geistes (gezackte Form)
    geist_body_points = [
        (x * multi + korrektur_breite, y * multi + korrektur_hoehe + 10),  # Linker Punkt
        (x * multi + korrektur_breite + 5, y * multi + korrektur_hoehe + 20),
        (x * multi + korrektur_breite + 10, y * multi + korrektur_hoehe + 10),
        (x * multi + korrektur_breite + 15, y * multi + korrektur_hoehe + 20),
        (x * multi + korrektur_breite + 20, y * multi + korrektur_hoehe + 10)
    ]
    pygame.draw.polygon(screen, farbe, geist_body_points)

    # Augen (weiß mit blauen Pupillen)
    pygame.draw.ellipse(screen, (255, 255, 255), [x * multi + korrektur_breite + 5, y * multi + korrektur_hoehe + 5, 5, 5])
    pygame.draw.ellipse(screen, (255, 255, 255), [x * multi + korrektur_breite + 12, y * multi + korrektur_hoehe + 5, 5, 5])
    pygame.draw.ellipse(screen, (0, 0, 255), [x * multi + korrektur_breite + 7, y * multi + korrektur_hoehe + 7, 2, 2])
    pygame.draw.ellipse(screen, (0, 0, 255), [x * multi + korrektur_breite + 14, y * multi + korrektur_hoehe + 7, 2, 2])

    return geist


"""Funktionen für die Spielfigur Pacman"""
# Drehen des Pacman Bildes
def pacman_drehen(image, pacman_richtung):
    if pacman_richtung == "rechts":  # Rechts
        return image
    elif pacman_richtung == "links":  # Links
        return pygame.transform.rotate(image, 180)
    elif pacman_richtung == "hoch":  # Unten
        return pygame.transform.rotate(image, 90)
    elif pacman_richtung == "runter":  # Oben
        return pygame.transform.rotate(image, -90)

# Pacman in aktuelle Richtung bewegen
def pacman_bewegen(pacman_richtung, pacman_x, pacman_y, feld):
    if pacman_richtung == "rechts" and pruefe_rechts(pacman_x, pacman_y, feld):
        pacman_x += 1
    elif pacman_richtung == "links" and pruefe_links(pacman_x, pacman_y, feld):
        pacman_x -= 1
    elif pacman_richtung == "hoch" and pruefe_oben(pacman_x, pacman_y, feld):
        pacman_y -= 1
    elif pacman_richtung == "runter" and pruefe_unten(pacman_x, pacman_y, feld):
        pacman_y += 1
    return pacman_x, pacman_y

# bei Eingabe des Users die Richtung ändern
def richtung_aendern(event, pacman_x, pacman_y, feld, pacman_richtung):
    # Pfeiltasten
    if event.key == pygame.K_RIGHT and pruefe_rechts(pacman_x, pacman_y, feld):
        print("Pacman läuft nach rechts")
        pacman_richtung = "rechts"
    elif event.key == pygame.K_LEFT and pruefe_links(pacman_x, pacman_y, feld):
        print("Pacman läuft nach links")
        pacman_richtung = "links"
    elif event.key == pygame.K_UP and pruefe_oben(pacman_x, pacman_y, feld):
        print("Pacman läuft nach oben")
        pacman_richtung = "hoch"
    elif event.key == pygame.K_DOWN and pruefe_unten(pacman_x, pacman_y, feld):
        print("Pacman läuft nach unten")
        pacman_richtung = "runter"
    # Taste für WASD
    elif event.key == pygame.K_w and pruefe_oben(pacman_x, pacman_y, feld):
        print("Pacman läuft nach oben")
        pacman_richtung = "hoch"
    elif event.key == pygame.K_a and pruefe_links(pacman_x, pacman_y, feld):
        print("Pacman läuft nach links")
        pacman_richtung = "links"
    elif event.key == pygame.K_s and pruefe_unten(pacman_x, pacman_y, feld):
        print("Pacman läuft nach unten")
        pacman_richtung = "runter"
    elif event.key == pygame.K_d and pruefe_rechts(pacman_x, pacman_y, feld):
        print("Pacman läuft nach rechts")
        pacman_richtung = "rechts"
    return pacman_richtung


"""Funktionen für das Spielfeld"""
# Spielfeld aus Datei einlesen
def spielfeld_aus_datei():
    spielfeld = []
    with open("PacMan_Feld.txt", "r") as datei:
        # strip() entfehrnen von leerzeichen
        # split() teilt die zeile einer Liste
        # append() fügt in die oben definierte Matrix ein
        # map(int, ...) Umwandlung von String in eine Int
        for zeile in datei:
            row = list(map(int, zeile.strip().split()))
            spielfeld.append(row)
    return spielfeld

# Spielfeld zeichnen
def zeichne_spielfeld(feld, screen, blau, gelb, schwarz, multi, korrektur_breite, korrektur_hoehe):
    for y in range(len(feld)):
        for x in range(len(feld[y])):
            if feld[y][x] == 1:
                pygame.draw.rect(screen, blau,[x * multi + korrektur_breite, y * multi + korrektur_hoehe, multi, multi], 1)
            if feld[y][x] == 0:
                pygame.draw.rect(screen, schwarz,[x * multi + korrektur_breite, y * multi + korrektur_hoehe, multi, multi])
            if feld[y][x] == 2:
                pygame.draw.ellipse(screen, gelb,[x * multi + 5 + korrektur_breite, y * multi + 5 + korrektur_hoehe, 10, 10])


"""Hilfefunktionen für die Funktionen der Fenster"""
# schaut ob ein Knopf gehovert wird
def wird_gehovert(mouse_pos, x, y, width, height):
    return x <= mouse_pos[0] <= x + width and y <= mouse_pos[1] <= y + height

# Prüft, ob das Spiel vorbei ist, also ob Pacman gegen einen Geist gelaufen ist
def pruefe_gameover(geist1, geist2, geist3, geist4, pacman, getroffen, score, level, text_ende, vergleich, screen, file ,name):
    if pacman.colliderect(geist4) or pacman.colliderect(geist3) or pacman.colliderect(geist2) or pacman.colliderect(geist1):
        if pacman.colliderect(geist1):
            text_ende = "Du wurdest von Blinky getroffen"
        elif pacman.colliderect(geist2):
            text_ende = "Du wurdest von Clyde getroffen"
        elif pacman.colliderect(geist3):
            text_ende = "Du wurdest von Inky getroffen"
        elif pacman.colliderect(geist4):
            text_ende = "Du wurdest von Pinky getroffen"
        pygame.mixer.Sound.play(getroffen)
        aktueller_score = str(score)
        level_aktuell = str(level)
        gameover_fenster(text_ende, aktueller_score, vergleich, screen, level_aktuell, file, name)
        return True
    else:
        return False


"""Funktionen für die verschiedenen Fenster des Programms"""
# Hauptmenü Fenster
def hauptmenue():
    # Eigenschaften Bildschirm
    breite, hoehe = 640, 480
    screen = pygame.display.set_mode((breite, hoehe))
    pygame.display.set_caption("PacMan Hauptmenü")

    # Eigenschaften Knöpfe
    knopf_spielen_x, knopf_spielen_y, knopf_spielen_breite, knopf_spielen_hoehe = 270, 150, 100, 50
    knopf_beenden_x, knopf_beenden_y, knopf_beenden_breite, knopf_beenden_hoehe = 270, 270, 100, 50
    knopf_highscore_x, knopf_highscore_y, knopf_highscore_breite, knopf_highscore_hoehe = 270, 210, 100, 50
    knopf_farbe = (0, 128, 255)
    hover_farbe = (0, 100, 200)
    text_farbe = (255, 255, 255)
    font = pygame.font.Font(None, 36)  # Default font

    # Spielen Knopf
    knopf_spielen_text = font.render("Spielen", True, text_farbe)
    text_rect_spielen = knopf_spielen_text.get_rect(center=(knopf_spielen_x + knopf_spielen_breite // 2, knopf_spielen_y + knopf_spielen_hoehe // 2))

    # Beenden Knopf
    knopf_beenden_text = font.render("Beenden", True, text_farbe)
    text_rect_beenden = knopf_beenden_text.get_rect(center=(knopf_beenden_x + knopf_beenden_breite // 2, knopf_beenden_y + knopf_beenden_hoehe // 2))

    # Highscore Knopf
    knopf_highscore_text = font.render("Highscore", True, text_farbe)
    text_rect_highscore = knopf_highscore_text.get_rect(center=(knopf_highscore_x + knopf_highscore_breite // 2, knopf_highscore_y + knopf_highscore_hoehe // 2))

    # Hintergrundmusik
    pygame.mixer.music.load('sounds/main.mid')
    pygame.mixer.music.play(-1, 0.0)

    # Loop fürs Hauptmenü
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            # Check for button click
            if event.type == pygame.MOUSEBUTTONDOWN:
                if wird_gehovert(pygame.mouse.get_pos(), knopf_spielen_x, knopf_spielen_y, knopf_spielen_breite, knopf_spielen_hoehe):
                    spiel(screen)
                    return
                elif wird_gehovert(pygame.mouse.get_pos(), knopf_highscore_x, knopf_highscore_y, knopf_highscore_breite, knopf_highscore_hoehe):
                    highscore_fenster(screen)
                    return
                elif wird_gehovert(pygame.mouse.get_pos(), knopf_beenden_x, knopf_beenden_y, knopf_beenden_breite, knopf_beenden_hoehe):
                    return

        # Bildschirm löschen
        screen.fill((0, 0, 0))

        # Ändere Farbe wenn hovered
        mouse_pos = pygame.mouse.get_pos()
        aktuelle_farbe_spielen = hover_farbe if wird_gehovert(mouse_pos, knopf_spielen_x, knopf_spielen_y, knopf_spielen_breite, knopf_spielen_hoehe) else knopf_farbe
        aktuelle_farbe_beenden = hover_farbe if wird_gehovert(mouse_pos, knopf_beenden_x, knopf_beenden_y, knopf_beenden_breite, knopf_beenden_hoehe) else knopf_farbe
        aktuelle_farbe_highscore = hover_farbe if wird_gehovert(mouse_pos, knopf_highscore_x, knopf_highscore_y, knopf_highscore_breite, knopf_highscore_hoehe) else knopf_farbe
        # Zeichne Knöpfe
        pygame.draw.rect(screen, aktuelle_farbe_spielen, (knopf_spielen_x, knopf_spielen_y, knopf_spielen_breite, knopf_spielen_hoehe), border_radius=10)
        screen.blit(knopf_spielen_text, text_rect_spielen)
        pygame.draw.rect(screen, aktuelle_farbe_beenden, (knopf_beenden_x, knopf_beenden_y, knopf_beenden_breite, knopf_beenden_hoehe), border_radius=10)
        screen.blit(knopf_beenden_text, text_rect_beenden)
        pygame.draw.rect(screen, aktuelle_farbe_highscore, (knopf_highscore_x, knopf_highscore_y, knopf_highscore_breite, knopf_highscore_hoehe), border_radius=10)
        screen.blit(knopf_highscore_text, text_rect_highscore)

        # Update display
        pygame.display.flip()


# Funktion für das Spiel selbst
def spiel(screen):
    # Einstellungen vom Benutzer
    name = "Anwender"

    # genutzte Farbe
    orange = (255, 140, 0)
    rot = (255, 0, 0)
    schwarz = (0, 0, 0)
    gelb = (255, 255, 0)
    blau = (0, 0, 255)
    hellblau = (135, 206, 255)
    pink = (255, 0, 255)

    # Multiplikator, sonst wird das fFld nicht richtig dargestellt, da es nur die Koordinaten nimmt, welche sehr klein sind, z.b (16,22)
    multi = 20

    # Maße des Fensters
    fensterhoehe = 480
    fensterbreite = 640

    # Koordinaten Geist 1
    geist1_x = 10
    geist1_y = 7

    #Koordinaten Geist 2
    geist2_x = 10
    geist2_y = 7

    #Koordinaten Geist 3
    geist3_x = 10
    geist3_y = 7

    #Koordinaten Geist 4
    geist4_x = 10
    geist4_y = 7

    # Pacman-Frames laden
    pacman_bilder = [
        pygame.image.load('images/geschlossen.png'),  # Mund geschlossen
        pygame.image.load('images/leichtOffen.png'),  # Mund leicht geöffnet
        pygame.image.load('images/weiterOffen.png'),  # Mund weiter geöffnet
        pygame.image.load('images/ganzOffen.png')  # Mund ganz offen
    ]
    frame = 0
    pacman_bilder = [pygame.transform.scale(img, (18, 18)) for img in pacman_bilder]

    # Koordinaten und Richtung von Pacman
    pacman_x = 10
    pacman_y = 14
    pacman_richtung = "hoch"

    #Score und Level
    score = 0
    level = 1

    #Sound für Punkte und treffer
    getroffen = pygame.mixer.Sound('sounds/death.wav')
    punkte = pygame.mixer.Sound('sounds/points.wav')

    # CSV-Datei einlesen
    df = pd.read_csv('highscore.csv')

    # Höchsten Score finden
    vergleich = df['Score'].max()

    # Titel für Fensterkopf
    pygame.display.set_caption("PacMan Spielfeld")

    # Spielfeld einlesen
    feld = spielfeld_aus_datei()

    # Korrektur für Feld damit alles mittig ist und nicht oben links
    korrektur_hoehe = (fensterhoehe - (multi * 16)) / 2
    korrektur_breite = (fensterbreite - (multi * 22)) / 2

    # Bildschirm Aktualisierungen einstellen
    clock = pygame.time.Clock()

    # Zähler Variablen für die Bewegung
    zeitzaehler_geister = 0
    zeitzaehler_pacman= 0

    # Schleife Hauptprogramm
    spielaktiv = True
    while spielaktiv:
        zeitzaehler_geister += clock.tick(30)
        zeitzaehler_pacman += clock.tick(30
                                         )
        # Überprüfen, ob Nutzer eine Aktion durchgeführt hat
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Spieler hat Quit-Button angeklickt")
                return
            elif event.type == pygame.KEYDOWN:
                print("Spieler hat Taste gedrückt")
                pacman_richtung = richtung_aendern(event, pacman_x, pacman_y, feld, pacman_richtung)

        # Punkte erscheinen lassen, wenn alle weg sind:
        level, level_up = punkte_auffuellen(feld,level)

        # Wenn Pacman über einen Punkt läuft verschwiendet dieser eingesammelt + punktestand wird akutalisiert
        score_text, score = punkt_einsammeln(feld, pacman_y, pacman_x, score, punkte)

        # Bewegung von Pacman und den Geistern
        if zeitzaehler_geister >= 200:
            # Bewegung Geist:
            geist1_x, geist1_y = geist_bewegen(geist1_x, geist1_y, feld)
            geist2_x, geist2_y = geist_bewegen(geist2_x, geist2_y, feld)
            geist3_x, geist3_y = geist_bewegen(geist3_x, geist3_y, feld)
            geist4_x, geist4_y = geist_bewegen(geist4_x, geist4_y, feld)
            zeitzaehler_geister = 0
        if zeitzaehler_pacman >= 150:
            # Bewegung Pacman
            pacman_x, pacman_y = pacman_bewegen(pacman_richtung, pacman_x, pacman_y, feld)
            zeitzaehler_pacman = 0

        # Highscore einlesen
        text_ende = ""
        file = pd.read_csv("highscore.csv")
        highscore = file["Score"].iloc[0]
        highscore_text = "Highscore: " + (str(highscore))

        # Spielfeld löschen
        screen.fill(schwarz)

        # Spielfeld zeichnen
        zeichne_spielfeld(feld, screen, blau, gelb, schwarz, multi, korrektur_breite, korrektur_hoehe)

        # zeichne Geister
        geist1 = zeichne_geist(screen, geist1_x, geist1_y, rot, multi, korrektur_breite, korrektur_hoehe) #Blinky
        geist2 = zeichne_geist(screen, geist2_x, geist2_y, orange, multi, korrektur_breite, korrektur_hoehe) #Clyde
        geist3 = zeichne_geist(screen, geist3_x, geist3_y, hellblau, multi, korrektur_breite, korrektur_hoehe) #Inky
        geist4 = zeichne_geist(screen, geist4_x, geist4_y, pink, multi, korrektur_breite, korrektur_hoehe) #Pinky
        # Pacman Animation (Frame wechseln)
        frame = (frame + 1) % 4  # Wechselt zwischen den 4 Frames
        # zeichne Pacman
        gedrehtes_bild = pacman_drehen(pacman_bilder[frame], pacman_richtung)
        pacman = screen.blit(gedrehtes_bild, (pacman_x * multi + korrektur_breite, pacman_y * multi + korrektur_hoehe))

        # tText für das Spiel
        schrift = pygame.font.SysFont("Arial", 35, True, True)
        text = schrift.render("PacMan", True, gelb)
        screen.blit(text, [0, 0])

        schrift_2 = pygame.font.SysFont("Arial", 15, True, True)
        text_2 = schrift_2.render(highscore_text, True, gelb)
        screen.blit(text_2, [400, 0])

        text_3 = schrift_2.render(score_text, True, gelb)
        screen.blit(text_3, [400, 30])

        text_4 = schrift_2.render(level_up, True, gelb)
        screen.blit(text_4, [400, 60])

        # gameover prüfen
        if pruefe_gameover(geist1, geist2, geist3, geist4, pacman, getroffen, score, level, text_ende, vergleich, screen, file, name):
            return

        # Fenster aktualisieren
        pygame.display.flip()

        # Refresh-Zeiten festlegen
        clock.tick(60)


# Fenster, indem die Top 5 Highscores angezeigt werden
def highscore_fenster(screen):
    screen.fill((0, 0, 0))
    schrift = pygame.font.SysFont("Arial", 15, True, True)

    # CSV-Datei einlesen
    highscores = pd.read_csv('highscore.csv')

    # Nach Score sortieren (absteigend)
    highscores_sortiert = highscores.sort_values(by='Score', ascending=False)

    # Erste 5 Zeilen anzeigen
    top_5 = highscores_sortiert.head(5)

    # Knopf füs Hauptmenü
    knopf_x, knopf_y, knopf_breite, knopf_hoehe = 270, 300, 100, 50
    knopf_farbe = (0, 128, 255)
    hover_farbe = (0, 100, 200)
    text_farbe = (255, 255, 255)
    knopf_text = schrift.render("Hauptmenü", True, text_farbe)
    text_rect = knopf_text.get_rect(center=(knopf_x + knopf_breite // 2, knopf_y + knopf_hoehe // 2))

    # Loop fürs Hauptmenü
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                if wird_gehovert(pygame.mouse.get_pos(), knopf_x, knopf_y, knopf_breite, knopf_hoehe):
                    hauptmenue()
                    return

        # Bildschirm löschen
        screen.fill((0, 0, 0))

        # Ändere Farbe wenn hovered
        mouse_pos = pygame.mouse.get_pos()
        aktuelle_farbe = hover_farbe if wird_gehovert(mouse_pos, knopf_x, knopf_y, knopf_breite, knopf_hoehe) else knopf_farbe

        # Zeichne Knopf
        pygame.draw.rect(screen, aktuelle_farbe, (knopf_x, knopf_y, knopf_breite, knopf_hoehe), border_radius=10)
        screen.blit(knopf_text, text_rect)

        # Zeichne Text
        # Überschrift
        header = schrift.render("Name   |   Score", True, text_farbe)
        screen.blit(header, (260, 20))

        # Daten anzeigen
        y_abstand = 60
        for _, row in top_5.iterrows():
            line = f"{row['Name']}   |   {row['Score']}"
            text = schrift.render(line, True, text_farbe)
            screen.blit(text, (270, y_abstand))
            y_abstand += 40  # Zeilenabstand

        # Display Updaten
        pygame.display.flip()


# Fenster für Game Over
def gameover_fenster(text_ende, end_score, vergleich, screen, level_aktuell, file, name):
    screen.fill((0, 0, 0))
    schrift = pygame.font.SysFont("Arial", 15, True, True)
    text1 = schrift.render("GAME OVER", True, (255, 255, 0))
    text2 = schrift.render(text_ende, True, (255, 255, 0))
    text3 = schrift.render("Score: "+ end_score, True, (255, 255, 0))

    # Prüfe ob ein neuer Highscore erreicht wurde
    if int(end_score) > int(vergleich):
        text4 = schrift.render("Du hast einen neuen Highscore (^_^)", True, (255, 255, 0))

        new_row = {"Name": name, "Score": str(end_score)}

        #Neue Zeile zum DataFrame hinzufügen (am Anfang)
        new_row_df = pd.DataFrame([new_row], columns=file.columns)

        file = pd.concat([new_row_df, file], ignore_index=True)

        # Speichern der neuen CSV-Datei
        file.to_csv("highscore.csv", index=False)
    else:
        text4 = schrift.render("Kein neuer Highscore :(", True, (255, 255, 0))

        highscore = pd.read_csv("highscore.csv")

        # Sortierend in absteigender reihenfolge
        highscore_sortiert = highscore.sort_values(by="Score",ascending=False)

        new_row = {"Name": name, "Score": str(end_score)}

        #wird als dataframe umgewandelt
        neue_zeile_schritt_1  = pd.DataFrame([new_row])

        #FDiese Zeile zur bestehenden Csv hinzufügen
        neue_zeile_schritt_2 = pd.concat([highscore_sortiert, neue_zeile_schritt_1], ignore_index=True )

        #Das DataFrame in der Csv speichern
        neue_zeile_schritt_2.to_csv("highscore.csv", index= False )
    text5 = schrift.render("Du hast es bis Level: " + level_aktuell + " geschafft", True, (255, 255, 0))

    # Knopf füs Hauptmenü
    knopf_x, knopf_y, knopf_breite, knopf_hoehe = 270, 190, 100, 50
    knopf_farbe = (0, 128, 255)
    hover_farbe = (0, 100, 200)
    text_farbe = (255, 255, 255)
    knopf_text = schrift.render("Hauptmenü", True, text_farbe)
    text_rect = knopf_text.get_rect(center=(knopf_x + knopf_breite // 2, knopf_y + knopf_hoehe // 2))

    # Loop fürs Hauptmenü
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                if wird_gehovert(pygame.mouse.get_pos(), knopf_x, knopf_y, knopf_breite, knopf_hoehe):
                    hauptmenue()
                    return

        # Bildschirm löschen
        screen.fill((0, 0, 0))

        # Ändere Farbe wenn hovered
        mouse_pos = pygame.mouse.get_pos()
        aktuelle_farbe = hover_farbe if wird_gehovert(mouse_pos, knopf_x, knopf_y, knopf_breite, knopf_hoehe) else knopf_farbe

        # Zeichne Knopf
        pygame.draw.rect(screen, aktuelle_farbe, (knopf_x, knopf_y, knopf_breite, knopf_hoehe), border_radius=10)
        screen.blit(knopf_text, text_rect)

        # Zeichne Text
        screen.blit(text1, [270, 50])
        screen.blit(text2, [230, 75])
        screen.blit(text3, [230, 100])
        screen.blit(text4, [230, 125])
        screen.blit(text5, [230, 150])

        # Display Updaten
        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    hauptmenue()
    pygame.quit()