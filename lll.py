import wx


class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="PanelChanger Demo", size=(400, 300))

        main_panel = wx.Panel(self)  # Główny panel kontener
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # Dropdown (ComboBox)
        choices = [
            "Visualise current recording session",
            "Visualise last recording session",
            "Select the file from operating system"
        ]
        self.combo_box = wx.ComboBox(main_panel, choices=choices, style=wx.CB_READONLY)
        self.combo_box.Bind(wx.EVT_COMBOBOX, self.on_combo_box_selected)
        main_sizer.Add(self.combo_box, 0, wx.ALL | wx.EXPAND, 10)

        # Kontener na panele
        self.panel_container = wx.Panel(main_panel)
        self.panel_sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel_container.SetSizer(self.panel_sizer)
        main_sizer.Add(self.panel_container, 1, wx.EXPAND)

        # Tworzenie paneli
        self.panel1 = self.create_panel(self.panel_container, "Grey", ["Current session", "Recording in progress"])
        self.panel2 = self.create_panel(self.panel_container, "Blue", ["Last session", "Duration: 10min", "Files: 3"])
        self.panel3 = self.create_panel(self.panel_container, "Green", ["File Selection", "Choose from system", "Supported: .wav, .mp3"])

        self.panels = [self.panel1, self.panel2, self.panel3]
        for p in self.panels:
            self.panel_sizer.Add(p, 1, wx.EXPAND)
            p.Hide()  # Ukrywamy wszystkie na start

        self.panel1.Show()

        main_panel.SetSizer(main_sizer)

    def create_panel(self, parent, color, labels):
        """ Tworzy panel o podanym kolorze i zawierający podaną listę etykiet. """
        panel = wx.Panel(parent)
        panel.SetBackgroundColour(color)

        sizer = wx.BoxSizer(wx.VERTICAL)
        for label in labels:
            text = wx.StaticText(panel, label=label)
            sizer.Add(text, 0, wx.ALL | wx.ALIGN_CENTER, 5)

        panel.SetSizer(sizer)
        return panel

    def on_combo_box_selected(self, event):
        """ Obsługa wyboru elementu z ComboBox - przełączanie paneli. """
        choice = self.combo_box.GetSelection()
        for panel in self.panels:
            panel.Hide()
        self.panels[choice].Show()

        self.panel_container.Layout()  # Aktualizacja układu paneli
        self.Layout()  # Aktualizacja całego okna


if __name__ == '__main__':
    app = wx.App(False)
    win = MainFrame()
    win.Show()
    app.MainLoop()
