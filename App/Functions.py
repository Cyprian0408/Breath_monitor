import os
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import  StandardScaler
from sklearn.preprocessing import normalize
import scipy.stats as stats
from scipy.signal import savgol_filter
from scipy.signal import find_peaks
from math import ceil
from PyQt6.QtCore import QDate, QTime, QDateTime, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt6.QtGui import QAction
import mainwindow_ui

X_axis=[]
Y_axis=[]
Z_axis=[]
Time=[]
begin_time_seconds=0
end_time_seconds=0
breaths_per_minute_x=0
breaths_per_minute_y=0
breats_per_minute_z=0
size=0
X_axis_normalized=[0]*size
Y_axis_normalized=[0]*size
Z_axis_normalized=[0]*size
#funkcja "czyszcząca konsolę"
def clear_console():
    os.system('clear')
#funkcja "czyszcząca wektory"
def clear_vectors():
    X_axis.clear()
    Y_axis.clear()
    Z_axis.clear()
    Time.clear()

#funkcja otwierająca plik tekstowy z zadanej ścieżki i tworząca wektory(listy) danych 
def read_file(path):
    number_of_cols=4
    with open(path,"r") as reader:
        #analizujemy plik linia po linii
        lines=reader.readlines()
        counter=0
        for line in lines:
            if counter==0:
                counter+=1
                continue
            else:
                list_string = list(line.split('\t'))
                list_string_temp=list_string[1:number_of_cols]
                #konwertowanie danych liczbowych z typu string na typ float
                list_float=[float(i) for i in list_string_temp]
                Time.append(list_string[0])
                X_axis.append(list_float[0])
                Y_axis.append(list_float[1])
                Z_axis.append(list_float[2]) 
    print("X_axis\n")
    print(X_axis)
    print("\n")
    print("Y_axis\n")
    print(Y_axis)
    print("\n")
    print("Z_axis\n")
    print(Z_axis)
    print("\n")
    return X_axis, Y_axis, Z_axis

def filter_data(vector):
    normalized_vector = stats.zscore(vector)
    filtered_vector = savgol_filter(normalized_vector, 101, 5)
    return filtered_vector



def menu(argument):
    switcher = {
        'n': run(),      
        'q': close_app(),       
    }
    func = switcher.get(argument, lambda: "Invalid data")
    print(func())

def run():
    clear_console()
    clear_vectors()
    #otwieranie pliku tekstowego z danymi z karty SD
    file_directory = "data/"
    print("List of files in your device\n")
    for file in os.listdir(file_directory):
            if file.endswith(".txt"):
                print(os.path.join(file_directory, file))
    print()
    #tworzenie ścieżki do pliku tekstowego, który chcemy otworzyć 
    file_name=input("Enter your file name with extension after dot\t")
    path=file_directory+file_name
    #sprawdzanie czy dany plik tekstowy istnieje pod wskazaną ścieżką
    check_file=os.path.isfile(path)
    if check_file:
        read_file(path)
    else:
        print("Something went wrong while opening your file...\n")
        print("Press 'n' if you want to choose another file or 'q' to quit\n")
        option=input()
        menu(option)


def plot_graphs(X_axis, Y_axis, Z_axis):
    normalize_vectors()
    print("Start plotting")
    #tworzenie wykresów
    fig_1=plt.figure(1,figsize=[13,4.8])
    ax=fig_1.add_subplot(131)
    ay=fig_1.add_subplot(132)
    az=fig_1.add_subplot(133)
    ax.plot(np.arange(len(X_axis)),X_axis,linewidth=0.7)
    ax.set_title("X_axis data")
    ax.set_xlabel("Samples")
    ax.set_ylabel("Values")
    ay.plot(np.arange(len(Y_axis)),Y_axis,linewidth=0.7)
    ay.set_title("Y_axis data")
    ay.set_xlabel("Samples")
    ay.set_ylabel("Values")
    az.plot(np.arange(len(Z_axis)),Z_axis,linewidth=0.7)
    az.set_title("Z_axis data")
    az.set_xlabel("Samples")
    az.set_ylabel("Values")
    fig_1.suptitle("Data representation in graphs")
    plt.ion()
    fig_1.show()
    #zapis wykresów do pliku
    fig_1.savefig('Graphs',dpi='figure', format='png', metadata=None,bbox_inches=None, pad_inches=0.1,facecolor='auto', edgecolor='auto',backend=None)

    #funkcja normalizująca wektory
def normalize_vectors():
    size=len(X_axis)
    #inicjalizacja list zerami
    array=[[0]*size,[0]*size,[0]*size]
    X_axis_normalized=[0]*size
    Y_axis_normalized=[0]*size
    Z_axis_normalized=[0]*size
    #maksyma poszczególnych list
    x_max=max(X_axis)
    y_max=max(Y_axis)
    z_max=max(Z_axis)
    #minima poszczególnych list
    x_min=min(X_axis)
    y_min=min(Y_axis)
    z_min=min(Z_axis)
    #zakres poszczególnych list
    x_range=max(X_axis)-min(X_axis)
    y_range=max(Y_axis)-min(Y_axis)
    z_range=max(Z_axis)-min(Z_axis)
    for i in range(0,size-1):
        X_axis_normalized[i]=(X_axis[i]-x_min)/x_range
        Y_axis_normalized[i]=(Y_axis[i]-y_min)/y_range
        Z_axis_normalized[i]=(Z_axis[i]-z_min)/z_range

    #tworzenie wykresów dla danych znormalizowanych
    fig_2=plt.figure(2,figsize=[13,4.8])
    ax_2=fig_2.add_subplot(131)
    ay_2=fig_2.add_subplot(132)
    az_2=fig_2.add_subplot(133)
    ax_2.plot(np.arange(len(X_axis_normalized)),X_axis_normalized,linewidth=0.7)
    ax_2.set_title("X_axis noramlized data")
    ax_2.set_xlabel("Samples")
    ax_2.set_ylabel("Values")
    ay_2.plot(np.arange(len(Y_axis_normalized)),Y_axis_normalized,linewidth=0.7)
    ay_2.set_title("Y_axis normalized data")
    ay_2.set_xlabel("Samples")
    ay_2.set_ylabel("Values")
    az_2.plot(np.arange(len(Z_axis_normalized)),Z_axis_normalized,linewidth=0.7)
    az_2.set_title("Z_axis normalized data")
    az_2.set_xlabel("Samples")
    az_2.set_ylabel("Values")
    fig_2.suptitle("Normalized data representation in graphs")
    plt.ion()
    fig_2.show()
    #zapis wykresów do pliku
    fig_2.savefig('Graphs_normalized',dpi='figure', format='png', metadata=None,bbox_inches=None, pad_inches=0.1,facecolor='auto', edgecolor='auto',backend=None)

def calculate_time():
    size=len(Time)
    #calculating begining time in seconds
    begin_hour_string=Time[0].rsplit('h')
    begin_minute_string=begin_hour_string[1].rsplit('m')
    begin_second_string=begin_minute_string[1].rsplit('s')
    begin_hour_int=int(begin_hour_string[0])
    begin_minute_int=int(begin_minute_string[0])
    begin_second_int=int(begin_second_string[0])
    begin_time_seconds=3600*begin_hour_int+60*begin_minute_int+begin_second_int
    #calculating ending time in seconds
    end_hour_string=Time[size-1].rsplit('h')
    end_minute_string=end_hour_string[1].rsplit('m')
    end_second_string=end_minute_string[1].rsplit('s')
    end_hour_int=int(end_hour_string[0])
    end_minute_int=int(end_minute_string[0])
    end_second_int=int(end_second_string[0])
    end_time_seconds=3600*end_hour_int+60*end_minute_int+end_second_int
    print("Begining time: \t")
    print(begin_time_seconds)
    print("Ending time: \t")
    print(end_time_seconds)
    return end_time_seconds-begin_time_seconds


    


def breaths_per_minute():
    calculate_time()
    X_peaks=find_peaks(X_axis)
    Y_peaks=find_peaks(Y_axis)
    Z_peaks=find_peaks(Z_axis)
    num_of_x_peaks=len(X_peaks[0])
    num_of_y_peaks=len(Y_peaks[0])
    num_of_z_peaks=len(Z_peaks[0])
    breaths_per_minute_x=num_of_x_peaks/((end_time_seconds-begin_time_seconds)/60)
    breaths_per_minute_y=num_of_y_peaks/((end_time_seconds-begin_time_seconds)/60)
    breaths_per_minute_z=num_of_z_peaks/((end_time_seconds-begin_time_seconds)/60)
    if(int(breaths_per_minute_x)==0):
        breaths_per_minute_x=None
    if(int(breaths_per_minute_y)==0):
        breaths_per_minute_y=None
    if(int(breaths_per_minute_z)==0):
        breaths_per_minute_z=None


def close_app():
    clear_console()
    print("Closing the app...\n")
    print("Done")
    exit()
    





