"""
file: main.py
"""
import sys
import VistaU
from VistaU import Terrenas

if __name__ == '__main__':
    app = VistaU.QApplication(sys.argv)
    app.setStyleSheet('''
        QWidget {
            font-size: 25px;
        }
    ''')
    
    elmapa = Terrenas()
    elmapa.show()
    
    sys.exit(app.exec())
