import sys
import re
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QTextBrowser, QPushButton, QStatusBar, QLabel, QFileDialog
from PyQt5.QtCore import Qt

# Lexical Analyzer 
construct_regex = {
    # Keywords
    'PROGRAM_START' : r'^HAI',
    'PROGRAM_END' : r'^KTHXBYE',
    'VARIABLE_DECLARATION_PORTION_START' : r'^WAZZUP',
    'VARIABLE_DECLARATION_PORTION_END' : r'^BUHBYE',
    'COMMENT_IDENTIFIER' : r'^BTW',
    'MULTI_COMMENT_DELIM_OP' : r'^OBTW',
    'MULTI_COMMENT_DELIM_CL' : r'^TLDR',
    'VAR_DECLARATION' : r'^I HAS A',
    'VAR_INITIALIZATION' : r'^ITZ',
    'VAR_ASSIGNMENT' : r'^R',
    'ADD_OPERATION' : r'^SUM OF',
    'SUB_OPERATION' : r'^DIFF OF',
    'MUL_OPERATION' : r'^PRODUKT OF',
    'DIV_OPERATION' : r'^QUOSHUNT OF',
    'MOD_OPERATION' : r'^MOD OF',
    'MAX_OPERATION' : r'^BIGGR OF',
    'MIN_OPERATION' : r'^SMALLER OF',
    'AND_OPERATION' : r'^BOTH OF',
    'OR_OPERATION' : r'^EITHER OF',
    'XOR_OPERATION' : r'^WON OF',
    'NOT_OPERATION' : r'^NOT',
    'INF_AND' : r'^ALL OF',
    'INF_OR' : r'^ANY OF',
    'IS_EQUAL' : r'^BOTH SAEM',
    'NOT_EQUAL' : r'^DIFFRINT',
    'STRING_CONCAT' : r'^SMOOSH',
    'CAST_OPERATOR' : r'^MAEK',
    'A_KEYWORD' : r'^A$',
    'TYPECAST' : r'^IS NOW A',
    'PRINT_OUTPUT' : r'^VISIBLE',
    'GIVE_INPUT': r'^GIMMEH',
    'IF_DELIMITER_OP' : r'^O RLY\?',
    'IF_STATEMENT' : r'^YA RLY',
    'ELSE_IF_STATEMENT' : r'^MEBBE',
    'ELSE_STATEMENT' : r'^NO WAI',
    'IF_SWITCH_DELIMITER_CL' : r'^OIC',
    'SWITCH_CASE_DELIM_OP' : r'^WTF\?',
    'CASE_STATEMENT' : r'^OMG',
    'DEFAULT_CASE' : r'^OMGWTF',
    'LOOP_DELIM_OP' : r'^IM IN YR',
    'INC_COUNTER' : r'^UPPIN',
    'DEC_COUNTER' : r'^NERFIN',
    'LOOP_COUNTER_KEYWORD' : r'^YR',
    'LOOP_COND_FALSE' : r'^TIL',
    'LOOP_COND_TRUE' : r'^WILE',
    'LOOP_DELIM_CL' : r'^IM OUTTA YR',
    'FUNCTION_DEFINITION_START' : r'^HOW IZ I',
    'FUNCTION_DEFINITION_END' : r'^IF U SAY SO',
    'BREAK_LOOP' : r'^GTFO',
    'RETURN_VALUE_KEYWORD' : r'^FOUND YR',
    'FUNCTION_CALLING' : r'^I IZ',
    'OPERAND_GROUP_CLOSE' : r'^MKAY',
    'SPACE' : r'^ ',
    'NEWLINE' : r'^\n',
        
    # Literals
    'INTEGER' : r'^-?(0|[1-9][0-9]*)$',                 # numbr
    'FLOAT' : r'^-?(0|[1-9][0-9]*)?\.[0-9]+',          # numbar
    'STRING' : r'^\"[^\"]*\"',                          # yarn
    'BOOL': r'^WIN|FAIL',                             # troof
    'TYPE' : r'^TROOF|NOOB|NUMBR|NUMBAR|YARN|TYPE',
    'COMMENTSTRING': r"(?<=BTW\s)(.*)",
    'MULTICOMMENTSTRING': r"(?<=OBTW\s)(.*)",
    # Identifier 
    'IDENTIFIER' : r'^[a-z][a-zA-Z_0-9]*$',
}

def create_tokens(code):
    tokens = []
    in_multiline_comment = False
    multiline_comment_content = []
    for line in code.splitlines():
        if in_multiline_comment:
            if re.match(construct_regex['MULTI_COMMENT_DELIM_CL'], line.strip()):
                in_multiline_comment = False
                tokens.append(['\n'.join(multiline_comment_content).strip(), 'MULTILINE_COMMENT'])
                tokens.append(['TLDR', 'MULTI_COMMENT_END'])
                multiline_comment_content = []
                continue
            else:
                multiline_comment_content.append(line.strip())
                continue
        line = line.strip()
        byline = []
        while line:
            for pattern_name, pattern in construct_regex.items():
                match = re.match(pattern, line)
                if match:
                    token_value = match.group()
                    if pattern_name == 'COMMENT_IDENTIFIER':
                        byline.append([token_value, 'COMMENT'])
                        comment_match = re.search(construct_regex['COMMENTSTRING'], line)
                        if comment_match:
                            comment_content = comment_match.group().strip()
                            byline.append([comment_content, 'COMMENTSTRING'])
                        line = ""
                        break
                    elif pattern_name == 'MULTI_COMMENT_DELIM_OP':
                        in_multiline_comment = True
                        comment_content = line[len(token_value):].strip()
                        if comment_content:
                            multiline_comment_content.append(comment_content)
                        byline.append([token_value, 'MULTI_COMMENT_START'])
                        line = ''
                        break
                    elif pattern_name == 'SPACE':
                        line = line[len(token_value):]
                        break
                    else:
                        byline.append([token_value, pattern_name])
                        line = line[len(token_value):].lstrip()
                        break
            else:
                line = line[1:].lstrip()
        if byline:
            tokens.append(byline)
    return tokens

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CMSC 124 Project LOL Interpreter")
        self.setGeometry(0, 0, 912, 669)

        self.inputFile = ""

        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)

        main_layout = QVBoxLayout(self.centralwidget)

        upper_row_layout = QHBoxLayout()

        left_column = QVBoxLayout()

        self.selectFileButton = QPushButton("Select LOL File", self.centralwidget)
        self.textBrowser = QTextBrowser(self.centralwidget)
        self.pushButton = QPushButton("EXECUTE", self.centralwidget)

        self.selectFileButton.clicked.connect(self.selectFile)
        self.pushButton.clicked.connect(self.executeLOLCode)

        left_column.addWidget(self.selectFileButton)
        left_column.addWidget(self.textBrowser)
        left_column.addWidget(self.pushButton)

        middle_column = QVBoxLayout()
        self.label_lexemes = QLabel("LEXEMES", self.centralwidget)
        self.label_lexemes.setAlignment(Qt.AlignCenter)
        middle_column.addWidget(self.label_lexemes)

        self.tableWidget = QTableWidget(self.centralwidget)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(["Lexemes", "Classifications"])
        middle_column.addWidget(self.tableWidget)

        self.tableWidget.horizontalHeader().setSectionResizeMode(0, 1)
        self.tableWidget.horizontalHeader().setSectionResizeMode(1, 1)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)

        right_column = QVBoxLayout()
        self.label_symbol_table = QLabel("SYMBOL TABLE", self.centralwidget)
        self.label_symbol_table.setAlignment(Qt.AlignCenter)
        right_column.addWidget(self.label_symbol_table)

        self.tableWidget_2 = QTableWidget(self.centralwidget)
        self.tableWidget_2.setColumnCount(2)
        self.tableWidget_2.setHorizontalHeaderLabels(["Identifier", "Value"])
        right_column.addWidget(self.tableWidget_2)

        self.tableWidget_2.horizontalHeader().setSectionResizeMode(0, 1)
        self.tableWidget_2.horizontalHeader().setSectionResizeMode(1, 1)
        self.tableWidget_2.horizontalHeader().setStretchLastSection(True)

        upper_row_layout.addLayout(left_column)
        upper_row_layout.addLayout(middle_column)
        upper_row_layout.addLayout(right_column)

        main_layout.addLayout(upper_row_layout)

        lower_row = QVBoxLayout()
        self.textBrowser_lower = QTextBrowser(self.centralwidget)
        lower_row.addWidget(self.textBrowser_lower)

        main_layout.addLayout(lower_row)

        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)

        self.show()

    def selectFile(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("LOL Files (*.lol)")
        if file_dialog.exec_():
            self.inputFile = file_dialog.selectedFiles()[0]
            with open(self.inputFile, 'r') as file:
                code = file.read()
                self.textBrowser.setText(code)

    def executeLOLCode(self):
        # Read the code from the QTextBrowser
        code = self.textBrowser.toPlainText()

        # Analyze the code using the lexer
        tokens = create_tokens(code)

        # Display the tokens in the Lexemes table
        self.tableWidget.setRowCount(0)  # Clear the table first

        # Flatten the tokens into a single list of (lexeme, classification) tuples
        all_tokens = []
        for byline in tokens:
            for lexeme, classification in byline:
                all_tokens.append((lexeme, classification))

        # Insert the tokens into the table
        for i, (lexeme, classification) in enumerate(all_tokens):
            self.tableWidget.insertRow(i)
            self.tableWidget.setItem(i, 0, QTableWidgetItem(lexeme))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(classification))

        # Update the status bar
        self.statusbar.showMessage(f"Code executed successfully from: {self.inputFile}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
