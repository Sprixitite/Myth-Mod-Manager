
import PySide6.QtWidgets as qtw
import PySide6.QtGui as qtg
from PySide6.QtCore import QUrl, Qt as qt

from constant_vars import TYPE_MODS, TYPE_MODS_OVERRIDE, TYPE_MAPS, ICON

class newModLocation(qtw.QDialog):

    typeDict = {}
    
    def __init__(self, *modName: QUrl) -> None:
        super().__init__()

        self.setWindowTitle('Installing mods')
        self.setWindowIcon(qtg.QIcon(ICON))
        self.setWindowFlag(qt.WindowType.WindowStaysOnTopHint, True)

        self.setMaximumSize(400, 850)
        self.setMinimumSize(320, 180)
        self.setSizePolicy(qtw.QSizePolicy.Policy.MinimumExpanding, qtw.QSizePolicy.Policy.Preferred)

        self.modName = modName
                            
        layout = qtw.QVBoxLayout()

        self.label = qtw.QLabel(self, text='Please select where the mods should be installed:')

        scrollArea = qtw.QScrollArea(self)
        scrollArea.setWidgetResizable(True)
        scrollArea.setVerticalScrollBarPolicy(qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scrollArea.setHorizontalScrollBarPolicy(qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        frame = qtw.QFrame(scrollArea)

        scrollArea.setWidget(frame)

        frameLayout = qtw.QVBoxLayout()
        frameLayout.setSpacing(5)

        for mod in (x.fileName() for x in modName):

            group = qtw.QGroupBox(f'{mod}')
            group.setObjectName(mod)

            radioButtonMod = qtw.QRadioButton(TYPE_MODS, group)
            radioButtonMod.setObjectName(f'{mod} {TYPE_MODS}')
            radioButtonMod.setChecked(False)
            radioButtonMod.clicked.connect(lambda: self.isAllChecked())

            radioButtonOverride = qtw.QRadioButton(TYPE_MODS_OVERRIDE, group)
            radioButtonOverride.setObjectName(f'{mod} {TYPE_MODS_OVERRIDE}')
            radioButtonOverride.clicked.connect(lambda: self.isAllChecked())
            radioButtonOverride.setChecked(False)

            radioButtonMaps = qtw.QRadioButton(TYPE_MAPS, group)
            radioButtonMaps.setObjectName(f'{mod} {TYPE_MAPS}')
            radioButtonMaps.clicked.connect(lambda: self.isAllChecked())
            radioButtonMaps.setChecked(False)

            h1 = qtw.QHBoxLayout()
            h1.addWidget(radioButtonMod)
            h1.addWidget(radioButtonOverride)
            h1.addWidget(radioButtonMaps)

            group.setLayout(h1)

            frameLayout.addWidget(group)

        frame.setLayout(frameLayout)

        buttons = qtw.QDialogButtonBox.Ok | qtw.QDialogButtonBox.Cancel

        self.buttonBox = qtw.QDialogButtonBox(buttons)
        self.changeOkButtonState(False)
        self.buttonBox.accepted.connect(lambda: self.accept())
        self.buttonBox.rejected.connect(lambda: self.reject())

        for widget in (self.label, scrollArea, self.buttonBox):
            layout.addWidget(widget)

        self.setLayout(layout)
    
    def changeOkButtonState(self, bool: bool) -> None:
        self.buttonBox.buttons()[0].setEnabled(bool)
    
    def isAllChecked(self):

        groups: list[qtw.QGroupBox] = self.findChildren(qtw.QGroupBox)

        for group in groups:

            buttons: list[qtw.QRadioButton] = group.findChildren(qtw.QRadioButton)

            if any((buttons[0].isChecked(), buttons[1].isChecked(), buttons[2].isChecked())):
                continue
            else:
                return
        
        self.changeOkButtonState(True)

    def getData(self) -> None:

        items: list[qtw.QGroupBox] = self.findChildren(qtw.QGroupBox)

        count = 0

        # Buttons[0] is mods, buttons[1] is override, buttons[2] is Maps
        for item in items:

            buttons: list[qtw.QRadioButton] = item.findChildren(qtw.QRadioButton)

            modName = self.modName[count].fileName()

            if buttons[0].isChecked():

                self.typeDict[modName] = TYPE_MODS
            elif buttons[1].isChecked():

                self.typeDict[modName] = TYPE_MODS_OVERRIDE
            
            elif buttons[2].isChecked():

                self.typeDict[modName] = TYPE_MAPS

            count += 1

    def accept(self) -> None:

        self.getData()

        return super().accept()