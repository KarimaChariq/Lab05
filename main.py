import flet as ft
from alert import AlertManager
from deposito_strumenti import DepositoStrumenti

FILE_STRUMENTI = "strumenti.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DAL DEPOSITO DI STRUMENTI DEL LAB03 ---
    deposito = DepositoStrumenti("Deposito Strumenti Musicali", "Alessandro Visconti")
    try:
        deposito.carica_file_strumenti(FILE_STRUMENTI)  # Carica il file
    except FileNotFoundError as e:
        alert.show_alert(f"❌ {e}")  # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile del deposito
    txt_titolo = ft.Text(value=deposito.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {deposito.get_responsabile()}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=deposito.get_responsabile(), label="Responsabile")

    # ListView per mostrare la lista di strumenti aggiornata
    lista_strumenti = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere un nuovo strumento (tipo, marca, anno, contatore posti)
    input_tipo = ft.TextField(label="Tipo", hint_text="Es. Chitarra")
    input_marca = ft.TextField(label="Marca", hint_text="Es. Fender")
    input_anno = ft.TextField(label="Anno di acquisto", hint_text="Es. 2021")

    # Contatore per il valore in euro dello strumento (usando TextField con bottoni o TextField numerico modificabile)
    input_valore = ft.TextField(label="Valore (€)", value="100.0")

    def decrementa_valore(e):
        try:
            val = float(input_valore.value)
            valore_aggiornato = max(0.0, val - 10.0)
            input_valore.value = str(round(valore_aggiornato, 2))
            input_valore.update()
        except ValueError:
            pass

    def incrementa_valore(e):
        try:
            val = float(input_valore.value)
            valore_aggiornato = val + 10.0
            input_valore.value = str(round(valore_aggiornato, 2))
            input_valore.update()
        except ValueError:
            pass

    btn_meno = ft.IconButton(icon=ft.icons.REMOVE, on_click=decrementa_valore)
    btn_piu = ft.IconButton(icon=ft.icons.ADD, on_click=incrementa_valore)

    row_valore = ft.Row(
        controls=[input_valore, btn_meno, btn_piu],
        alignment=ft.MainAxisAlignment.CENTER
    )


    # --- FUNZIONI APP ---
    def aggiorna_lista_strumenti():
        lista_strumenti.controls.clear()
        for strumento in deposito.strumenti_ordinati_per_marca():
            stato = "✅" if strumento.disponibile else "⛔"
            lista_strumenti.controls.append(ft.Text(f"{stato} {strumento}"))
            lista_strumenti.update()
    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"
        page.update()
    def conferma_responsabile(e):
        deposito.set_responsabile(input_responsabile.value)
        txt_responsabile.value = f"Responsabile: {deposito.get_responsabile()}"
        txt_responsabile.update()
    # Handlers per la gestione dei pulsanti utili all'inserimento di un nuovo strumento
    file_aggiungi_strumento = ft.Ref[ft.TextField]()

    def aggiungi_nuovo_strumento(e):
        tipo = input_tipo.value.strip()
        marca = input_marca.value.strip()
        str_anno = input_anno.value.strip()
        str_valore = input_valore.value.strip()

        # Controlli di validazione
        if not tipo or not marca or not str_anno or not str_valore:
            alert.show_alert("Errore: Tutti i campi devono essere compilati.")
            return

        try:
            anno_acquisto = int(str_anno)
        except ValueError:
            alert.show_alert("Errore: Il campo 'Anno di acquisto' deve essere un numero intero valido.")
            return

        try:
            valore = float(str_valore)
        except ValueError:
            alert.show_alert("Errore: Il campo 'Valore' deve essere un numero valido.")
            return

        # Aggiunta tramite il metodo del deposito
        deposito.aggiungi_strumento(tipo, marca, anno_acquisto, valore)

        # Svuota i campi di input
        input_tipo.value = ""
        input_marca.value = ""
        input_anno.value = ""
        input_valore.value = "100.0"

        # Aggiorna la schermata / lista
        aggiorna_lista_strumenti()
        page.update()


    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.Button("Conferma", on_click=conferma_responsabile)

    # Pulsanti per la gestione dell'inserimento di un nuovo strumento
    pulsante_aggiungi = ft.ElevatedButton("Aggiungi strumento", on_click=aggiungi_nuovo_strumento)

    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        ft.Divider(),
        ft.Text("Aggiungi Nuovo Strumento", size=20),
        ft.Row(
            controls=[input_tipo, input_marca, input_anno],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10
        ),
        row_valore,
        pulsante_aggiungi,

        # Sezione 4
        ft.Divider(),
        ft.Text("Strumenti", size=20),
        lista_strumenti,
    )
    aggiorna_lista_strumenti()

ft.run(main)
