import sys
import csv
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QPushButton, QWidget, QFileDialog
from pyqtgraph import PlotWidget, ViewBox
from PyQt5.QtCore import QTimer
import pyqtgraph as pg
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Signal Plotter")
        self.setGeometry(100, 50, 1500, 300)
        self.startFlag=True
        # Create the main widget and layout
        main_widget = QWidget()
        main_layout = QGridLayout(main_widget)
        self.setCentralWidget(main_widget)
        
        # Create the plot widgets and add them to the layout
        self.plot_widgets = []
                # Create a QPen object
        pen = pg.mkPen((0,255,0), width=3)
        for i in range(12):
            plot_widget = PlotWidget()
            plot_widget.plot([0]*100,pen=pen)
            self.plot_widgets.append(plot_widget)
        for i in range(6):
            main_layout.addWidget(self.plot_widgets[i], 0, i)
        for i in range(6):
            main_layout.addWidget(self.plot_widgets[i+6], 1, i)
        
        # Create the buttons and add them to the layout
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_data)
        main_layout.addWidget(save_button, 2, 0)
        
        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self.clear_data)
        main_layout.addWidget(clear_button, 2, 1)
        
        self.Start_button = QPushButton("Start")
        self.Start_button.clicked.connect(self.start_stop)
        main_layout.addWidget(self.Start_button, 2, 2)
        
        # Create the data buffer
        self.data = [[0]*100 for i in range(12)]
        
        self.plot_widgets[1].setBackground('k')  



        # Create the update timer
        self.timer = QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_plots)
        self.timer.start()
        
        
    def save_data(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save File", "", "CSV Files (*.csv)")
        if filename:
            with open(filename, "w") as f:
                writer = csv.writer(f)
                writer.writerow(["Signal {}".format(i) for i in range(1, 13)])
                for i in range(len(self.data)):
                    writer.writerow(self.data[i])
    
    def clear_data(self):
        self.data = [[0]*100 for i in range(12)]
        for i in range(12):
            self.plot_widgets[i].clear()
            self.plot_widgets[i].plot([0]*100)
    
    def start_stop(self):
        self.startFlag= not(self.startFlag)
        if self.startFlag:
            self.Start_button.setText("Stop")
        else:
            self.Start_button.setText("Start")

        for i in range(12):
            for j in range(50):
                self.data[i].pop(0)
                self.data[i].append(random.randint(-10, 10))
        self.update_plots()
    
    def update_plots(self):
        for i in range(12):
            self.plot_widgets[i].clear()
            self.plot_widgets[i].plot(self.data[i],pen=pg.mkPen(color=(0, 255, 0), width=3))
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
