"""
file: main.py
"""
import sys
import Vista
from Vista import Terrenas

if __name__ == '__main__':
    app = Vista.QApplication(sys.argv)
    app.setStyleSheet('''
        QWidget {
            font-size: 25px;
        }
    ''')
    
    elmapa = Terrenas()
    elmapa.show()
    
    sys.exit(app.exec())
