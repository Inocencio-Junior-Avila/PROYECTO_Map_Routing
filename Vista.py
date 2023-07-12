import io
import osmnx as ox
import folium
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLineEdit
from PyQt6.QtWebEngineWidgets import QWebEngineView
from Controlador import Graph
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QMessageBox

class ErrorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Error")
        layout = QVBoxLayout()
        self.setLayout(layout)
        label = QLabel("La lista de coordenadas del camino está vacía.")
        layout.addWidget(label)
        button = QPushButton("Volver al centro")
        button.clicked.connect(self.accept)
        layout.addWidget(button)

class Terrenas(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Tarea - Map routing')
        self.resize(800, 600)
        self._graph = Graph()
        self.view_zoom = 15
        self.current_map = None
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Crear QWebEngineView
        self.webView = QWebEngineView()
        layout.addWidget(self.webView, stretch=7)
        
        # Cargar el grafo desde el archivo .osm
        G = ox.graph_from_xml('las_terrenas2.osm', simplify=False)

        # Obtener las coordenadas del centro del grafo
        location = (19.3110142, -69.5430670)
        self.current_map = folium.Map(
            zoom_start=self.view_zoom,
            location=location
        )

        # Guardar los datos del mapa en un objeto de datos
        self.update_map()
        
        # Contenedor para los textfields y el botón.
        textFieldLayout = QHBoxLayout()
        
        self.src = QLineEdit(self)
        self.src.setPlaceholderText("Partida: nodeID del OSM")
        textFieldLayout.addWidget(self.src)
        
        self.dst = QLineEdit(self)
        self.dst.setPlaceholderText("Destino: nodeID del OSM")
        textFieldLayout.addWidget(self.dst)
        
        button = QPushButton("A buscar ruta =)")
        button.clicked.connect(self.find_route)
        textFieldLayout.addWidget(button)
        
        layout.addLayout(textFieldLayout)

        # Cambiar los estilos de los widgets en el contenedor
        self.src.setStyleSheet("QLineEdit { border: 2px solid blue; border-radius: 10px; }")
        self.dst.setStyleSheet("QLineEdit { border: 2px solid blue; border-radius: 10px; }")
        button.setStyleSheet("QPushButton { background-color: green; color: white; }")
        
    def find_route(self):
        
        # Obtener los nodos de origen y destino
        start_node = self.src.text()
        goal_node = self.dst.text()
        if not start_node or not goal_node:
            self.show_error_dialog("Ingrese un nodo de origen y un nodo de destino válidos.")
            return
        
        # Generar la nueva ruta
        m = self._graph.generate_map(start_node, goal_node)
        if m is not None:
            self.current_map = m
            self.update_map()
        else:
            self.show_error_dialog("No se encontró una ruta válida.")
    
    def clear_map(self):
        location = self.current_map.location if self.current_map else None
        self.current_map = folium.Map(location=location, zoom_start=15)
        self.update_map()

    def update_map(self):
        if self.current_map is not None:
            data = io.BytesIO()
            self.current_map.save(data, close_file=False)
            self.webView.setHtml(data.getvalue().decode())
        else:
            print("El mapa está vacío. No se puede actualizar.")

    def show_error_dialog(self, message):
        dialog = QMessageBox(self)
        dialog.setWindowTitle("Error")
        dialog.setText(message)
        accept_button = dialog.addButton("Aceptar", QMessageBox.ButtonRole.AcceptRole)
        accept_button.clicked.connect(self.clear_map)
        dialog.exec()

if __name__ == "__main__":
    app = QApplication([])
    window = Terrenas()
    window.show()
    app.exec()
