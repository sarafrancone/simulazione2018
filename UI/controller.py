import flet as ft

from database.DAO import DAO


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self.selectedYear = None
        self.selectedCountry = None

    def fillDDYear(self):
        anni = self._model.getAnni()
        for anno in anni:
            self._view.ddyear.options.append(ft.dropdown.Option(data=anno, on_click=self.readDDYear, text=anno))
        self._view.update_page()

    def readDDYear(self, e):
        if e.control.data is None:
            self.selectedYear = None
        else:
            self.selectedYear = e.control.data
        print(f"readDDYear called--{self.selectedYear}")

    def fillDDCountry(self):
        stati = self._model.getNodes()
        for s in stati:
            self._view.ddcountry.options.append(ft.dropdown.Option(data=s, on_click=self.readDDCountry, text=s.Name))
        self._view.update_page()

    def readDDCountry(self, e):
        if e.control.data is None:
            self.selectedCountry = None
        else:
            self.selectedCountry = e.control.data
        print(f"readDDCountry called--{self.selectedCountry}")

    def handle_avvistamenti(self, e):
        self._view.txt_result.controls.clear()

        self._view.txt_result.controls.append(ft.Text(f"Numero di avvistamenti nell'anno {self.selectedYear}: {self._model.getAvvistamenti(self.selectedYear)}"))
        self._model.buildGraph(self.selectedYear)
        self.fillDDCountry()
        n, a = self._model.getGraphDetails()
        self._view.txt_result.controls.append(ft.Text(f"Grafo correttamente creato! #{n} nodi #{a} archi."))

        self._view.update_page()

    def handle_analizza(self, e):
        self._view.txt_result.controls.clear()
        if self.selectedCountry is None:
            self._view.create_alert("Selezionare uno stato.")
            return
        precedenti = self._model.getPrecedenti(self.selectedCountry)
        successivi = self._model.getSuccessori(self.selectedCountry)
        raggiungibili = self._model.getRaggiungibiliDFS(self.selectedCountry)
        self._view.txt_result.controls.append(ft.Text(f"Stati precedenti a {self.selectedCountry}"))
        for p in precedenti:
            self._view.txt_result.controls.append(ft.Text(p))
        self._view.txt_result.controls.append(ft.Text(f"Stati successivi a {self.selectedCountry}"))
        for s in successivi:
            self._view.txt_result.controls.append(ft.Text(s))
        self._view.txt_result.controls.append(ft.Text(f"Stati raggiungibili da {self.selectedCountry}"))
        for r in raggiungibili:
            self._view.txt_result.controls.append(ft.Text(r))

        self._view.update_page()

#NON STAMPA PER NUMERI GRANDI, MA RICORSIONE DOVREBBE ESSERE CORRETTA
    def handle_sequenzaAvvistamenti(self, e):
        self._view.txt_result.controls.clear()
        if self.selectedCountry is None:
            self._view.create_alert("Selezionare uno stato")
            return
        path, len = self._model.sequenzaAvvistamenti(self.selectedCountry)

        self._view.txt_result.controls.append(ft.Text(f"Lunghezza cammino {len}"))
        for p in path:
            self._view.txt_result.controls.append(ft.Text(f"{p}"))
        self._view.update_page()











