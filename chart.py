from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import requests
from PyQt5.QtGui import QIcon
class TicketSalesChart(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("taran.png"))
        self.setWindowTitle("Visual data")
        self.setGeometry(100, 100, 800, 600)

        # Create a main widget and layout
        main_widget = QWidget()
        layout = QVBoxLayout()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

        # Create the matplotlib canvas
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Load data and plot the chart
        self.load_data_and_plot()

    def load_data_and_plot(self):
        try:
            # Fetch ticket sales data from API
            response = requests.get("http://zhanyysh.pythonanywhere.com/purchase/tickets_by_movie")
            if response.status_code == 200:
                data = response.json()
                self.plot_chart(data)
            else:
                print("Failed to fetch data.")
        except Exception as e:
            print(f"Error: {e}")

    def plot_chart(self, data):
        movie_names = [item['movie_title'] for item in data]
        ticket_sales = [item['tickets_sold'] for item in data]

        # Clear the figure
        self.figure.clear()

        # Create a bar chart
        ax = self.figure.add_subplot(111)
        ax.bar(movie_names, ticket_sales, color='skyblue')
        ax.set_title("Tickets Sold by Movie")
        ax.set_xlabel("Movies")
        ax.set_ylabel("Tickets Sold")
        ax.tick_params(axis='x', rotation=45)

        # Refresh the canvas
        self.canvas.draw()
