import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QTextBrowser, QPushButton, QStatusBar, QLabel, QFileDialog
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CMSC 124 Project LOL Interpreter")
        self.setGeometry(0, 0, 912, 669)

        # Variable to store input file path
        self.inputFile = ""

        # Central Widget
        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)

        # Main Layout (Vertical for upper and lower sections)
        main_layout = QVBoxLayout(self.centralwidget)

        # Upper Row Layout (Horizontal for 3 columns)
        upper_row_layout = QHBoxLayout()

        # Left Column
        left_column = QVBoxLayout()

        # Create a QPushButton for file selection
        self.selectFileButton = QPushButton("Select LOL File", self.centralwidget)
        self.textBrowser = QTextBrowser(self.centralwidget)
        self.pushButton = QPushButton("EXECUTE", self.centralwidget)  # Added EXECUTE button

        # Connect button to the file selection function
        self.selectFileButton.clicked.connect(self.selectFile)

        # Connect the EXECUTE button to a placeholder function (you can implement logic here)
        self.pushButton.clicked.connect(self.executeLOLCode)

        left_column.addWidget(self.selectFileButton)
        left_column.addWidget(self.textBrowser)
        left_column.addWidget(self.pushButton)

        # Middle Column (Lexemes Table)
        middle_column = QVBoxLayout()
        self.label_lexemes = QLabel("LEXEMES", self.centralwidget)
        self.label_lexemes.setAlignment(Qt.AlignCenter)
        middle_column.addWidget(self.label_lexemes)

        self.tableWidget = QTableWidget(self.centralwidget)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(["Lexemes", "Classifications"])
        middle_column.addWidget(self.tableWidget)

        # Set table headers to stretch
        self.tableWidget.horizontalHeader().setSectionResizeMode(0, 1)  # Stretch the first column
        self.tableWidget.horizontalHeader().setSectionResizeMode(1, 1)  # Stretch the second column
        self.tableWidget.horizontalHeader().setStretchLastSection(True)  # Stretch the last section if needed

        # Right Column (Symbol Table)
        right_column = QVBoxLayout()
        self.label_symbol_table = QLabel("SYMBOL TABLE", self.centralwidget)
        self.label_symbol_table.setAlignment(Qt.AlignCenter)
        right_column.addWidget(self.label_symbol_table)

        self.tableWidget_2 = QTableWidget(self.centralwidget)
        self.tableWidget_2.setColumnCount(2)
        self.tableWidget_2.setHorizontalHeaderLabels(["Identifier", "Value"])
        right_column.addWidget(self.tableWidget_2)

        # Set table headers to stretch
        self.tableWidget_2.horizontalHeader().setSectionResizeMode(0, 1)  # Stretch the first column
        self.tableWidget_2.horizontalHeader().setSectionResizeMode(1, 1)  # Stretch the second column
        self.tableWidget_2.horizontalHeader().setStretchLastSection(True)  # Stretch the last section if needed

        # Add columns to the upper row layout
        upper_row_layout.addLayout(left_column)
        upper_row_layout.addLayout(middle_column)
        upper_row_layout.addLayout(right_column)

        # Add upper row layout to the main layout
        main_layout.addLayout(upper_row_layout)

        # Lower Row (Text Display) - Adjust with stretch
        lower_row = QVBoxLayout()
        self.textBrowser_lower = QTextBrowser(self.centralwidget)
        lower_row.addWidget(self.textBrowser_lower)

        # Add stretch to make the lower row expand and fill remaining space
        main_layout.addLayout(lower_row)
        main_layout.addStretch(1)  # This makes the lower row take remaining space

        # Set the layout to the central widget
        self.centralwidget.setLayout(main_layout)

        # StatusBar
        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)

    def selectFile(self):
        """Function to open a file dialog and select a .lol file"""
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("LOL files (*.lol)")
        file_dialog.setViewMode(QFileDialog.List)

        if file_dialog.exec_():
            # Get the selected file path
            selected_file = file_dialog.selectedFiles()[0]
            self.inputFile = selected_file  # Store the file path in the inputFile variable

            # Display the file path in the textBrowser
            with open(self.inputFile, 'r') as file:
                file_content = file.read()

            self.textBrowser.setPlainText(file_content)  # Display content in the textBrowser

    def executeLOLCode(self):
        """Placeholder function for executing the LOL code"""
        if self.inputFile:
            # You can add the logic for interpreting or executing the LOL code here.
            self.statusbar.showMessage(f"Executing LOL code from {self.inputFile}")
        else:
            self.statusbar.showMessage("No file selected for execution.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
