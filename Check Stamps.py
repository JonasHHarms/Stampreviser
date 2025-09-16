import os
import tempfile
from pypdf import PdfReader
import py7zr

archive_path = input("Bitte gib den Pfad zur 7z-Datei an: ")

if not os.path.isfile(archive_path):
    print("7z Archiv nicht gefunden")
    exit()

print(    "Ich extrahiere die PDF-Dateien aus der 7z-Datei und prüfe sie auf Stempel. Dies kann einige Zeit in Anspruch nehmen.")

try:
    with py7zr.SevenZipFile(archive_path, mode='r') as archive:
        all_filenames = archive.getnames()
        pdf_filenames = [name for name in all_filenames if name.lower().endswith('.pdf')]

        if not pdf_filenames:
            print("Keine PDF-Dateien in der 7z-Datei gefunden.")
        else:
            with tempfile.TemporaryDirectory() as temp_dir:
                archive.extract(targets=pdf_filenames, path=temp_dir)

                for filename in pdf_filenames:
                    try:
                        file_path = os.path.join(temp_dir, filename)
                        if not os.path.isfile(file_path):
                            print(f"Error beim prüfen der Datei '{filename}'")
                            continue
                        reader = PdfReader(file_path)
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
                            print(f"Die Datei '{filename}' wurde ggf. nicht gestempelt.")
                    except Exception as e:
                        print(f"Fehler beim Verarbeiten der Datei '{filename}': {str(e)}")
except Exception as e:
    print(f"Fehler beim Öffnen oder Extrahieren der 7z-Datei: {str(e)}")

print("\nFertig: Alle PDF-Dateien wurden hinsichtlich Stempel geprüft.")
while True:
    user_input = input(" ").lower()
    if user_input == 'close':
        print("Fenster wird geschlossen...")
        break
    else:
        print(" ")
