# map_cutout

Map cutout ist ein kleines Tool, welches dazu dient einen Bereich in Google Earth für das Map Modding zu markieren.  
Angegeben wird das Zentrum des Ausschnitts in Grad, Minuten, Sekunden und die gewünschte Kantenlänge in km.

Das Tool erzeugt daraus eine `cutout.kml` Datei auf dem Desktop.

Diese kann dann in Google Earth importiert werden und markiert den entsprechenden Ausschnitt.  
In der KML steht ebenfalls unter `corner_tl` die linke obere Ecke und unter `corner_br` die rechte untere Ecke das Ausschnitts in Grad, Minuten, Sekunden. Dafür muss die Datei mit einem Editor (notepad++, vs code, etc.) geöffnet werden.

!!! Achtung der Ausschnitt ist aktuell nicht auf den Meter genau. Ich feile noch an den Paramtern. !!!

Die exe findet ihr im Ordner dist.

## Falls du mich und meine Arbeit unterstützen möchtest > [Spende](https://www.paypal.com/donate/?hosted_button_id=ZR4EGNDAVD4Q4)  
## If you want to donate my work > [Donate](https://www.paypal.com/donate/?hosted_button_id=ZR4EGNDAVD4Q4)
