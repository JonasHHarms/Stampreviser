import os
import sys
from datetime import datetime, timedelta
from pypdf import PdfReader  
import win32com.client as win32

pfad_mapping = {
    "Name": r"C:\Folder\...etc",
}

zeitraum = datetime.now() - timedelta(days=14)

output = f"Beep Boop 🤖, <br><br> im Folgenden die Auswertung:<br> "

for ordner_name, ordner_pfad in pfad_mapping.items():
    output += f"<br><b>Prüfe Ordner: {ordner_name}</b> (<a href='file:///{ordner_pfad}'>{ordner_pfad}</a>) <br>"
    if not os.path.isdir(ordner_pfad):
        output += f"<br>Ordner {ordner_pfad} nicht gefunden :( "
        continue
    ups  = False
    for datei in os.listdir(ordner_pfad):
        if datei.endswith('.pdf'):
            voller_pfad = os.path.join(ordner_pfad, datei)
            file_mtime = datetime.fromtimestamp(os.path.getmtime(voller_pfad))
            if file_mtime >= zeitraum:
                try:
                    with open(voller_pfad, 'rb') as file:
                        reader = PdfReader(file)
                        gestempelt = False
                        for page in reader.pages:
                            annotations = page.annotations
                            if annotations:
                                for annot in annotations:
                                    subtype = annot.get("/Subtype")
                                    if subtype == "/Stamp":
                                        gestempelt = True
                                        break
                            if gestempelt:
                                break
                        if not gestempelt:
                            output += f"<li> <span style='padding-left: 20px;'> Die Datei  (<a href='file:///{ordner_pfad}\{datei}'>{datei}</a>) wurde nicht gestempelt.</span></li> <br>"
                            ups = True
                except Exception as e:
                    output +=f"<li> <span style='padding-left: 20px;'>Fehler beim Lesen der Datei {datei}: {str(e)}</span></li>"
                    ups = True
    if not ups:
        output += "<li> <span style='padding-left: 20px;'>Sieht auf den ersten Blick in Ordnung aus </span></li></br>"


output += f"<br><br><i>Alle Angaben ohne Gewähr.</i> <br><br>Beep Boop,  <br>Euer Stempelbot 🤖<br><br>Diese Mail wurde automatisch generiert."



outlook = win32.Dispatch('outlook.application')
mail = outlook.createItem(0)
mail.To ='EMPFÄNGER'

mail.HTMLBody =  output
mail.subject = f"🤖: Ergebnis Stempelbot {zeitraum.strftime('%d.%m.%Y')} - {datetime.now().strftime('%d.%m.%Y')}"

try:
    mail.Send() 
    print("Mail versendet")
    sys.exit()
except Exception as e:
    print(f'Fehler: {e}')
