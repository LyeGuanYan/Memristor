import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter import *

import openpyxl 
import ltspice
import subprocess
import os
import matplotlib.pyplot as plt


window = tk.Tk()
window.geometry("500x480+10+10")
window.title('Crossbar Memristor')

# Line Resistance
line_res = '18.22u'
# Load Resistance
load_res = '10k'
# Ground Capacitance
gnd_cap = '1.34e-18'
# Parallel Capacitance
line_cap = '1.6e-18'
# Input Voltage Source Parameters (PWL)
input_signal = 'pwl_selected.txt'
# NMOS Voltage Source Parameters (PWL)
nmos_signal = 'nmos.txt'
# Voltage Source Parameters (Sine Wave) {DC offset Amplitude Freq}
input_voltage_sine = '0 1.0 10'
# Simulation Run Time
simulation_time = '400m'
# Define the options as a list of strings
size_options = ["1x1", "2x2", "4x4", "8x8", "16x16", "32x32", "64x64", "128x128", "256x256"]
# Selected array size
size = 1
# Define global variable to store combobox object
size_combobox = None
# Input Voltage Signal Directory Variable
file_entry = input_signal
# Memristors' State Matrix Data
data = []
# Selected Column to Plot Output Graph
selected_column = ''

# Define variables to store the textbox values
# Input Voltage Source Parameters (PWL)
input_signal_value = tk.StringVar()
# Line Resistance
line_resistance_value = tk.StringVar()
# Ground Capacitance
ground_capacitance_value = tk.StringVar()
# Parallel Capacitance
line_capacitance_value = tk.StringVar()
# Simulation Run Time
simulation_time_value = tk.StringVar()
# Memristors' State Write File (Excel)
write_value = tk.StringVar()

# Create sine wave input 1x1 schematic to get characteristics (Hysteresis)
def iv_characteristic() :

    # filename
    filename = '1x1_sine'

    # Schematic filename
    filename_asc = filename + '.asc'

    # To get user input (Chosen Memristor Model)
    name = get_model()

    # Write the schematic file
    with open(filename_asc, 'w') as writer :

        # Sine wave schematic lines
        file_list = ['Version 4\n', 'SHEET 1 1772 680\n', 'WIRE 288 144 -16 144\n', 'WIRE -16 176 -16 144\n',
                     'WIRE 288 176 288 144\n', 'WIRE -16 304 -16 256\n', 'WIRE 304 304 304 288\n',
                     'WIRE 304 304 -16 304\n',
                     'WIRE 304 448 304 304\n', 'FLAG 304 448 0\n', 'FLAG 272 288 S1\n', 'IOPIN 272 288 Out\n',
                     'SYMBOL voltage -16 160 R0\n', 'WINDOW 123 0 0 Left 0\n', 'WINDOW 39 0 0 Left 0\n',
                     'WINDOW 3 24 44 Left 2\n',
                     'SYMATTR Value SINE(' + input_voltage_sine + ')\n', 'SYMATTR InstName V1\n',
                     'SYMBOL ' + name + ' 288 224 R90\n',
                     'SYMATTR InstName U1\n', 'TEXT -248 344 Left 2 !.tran ' + simulation_time + '\n', ]

        for line in file_list :
            writer.write(line)

    writer.close()

    lt_directory = "C:\Program Files\LTC\LTspiceXVII"

    subprocess.call(lt_directory + "\XVIIx64.exe -b -Run " + filename_asc)

    l = ltspice.Ltspice(os.path.dirname(__file__) + '\\' + filename + '.raw')
    print('os.path.dirname(__file__)=', os.path.dirname(__file__))

    l.parse()

    Ix = l.get_data('Ix(U1:TE)')
    V = l.get_data('V(n001)')

    plt.plot(V, Ix)
    plt.ylabel('Current(Ix)')
    plt.xlabel('Voltage (V)')
    plt.show()


def condition():
    t = int(condition_var.get())

    if t == 1 or t == 2 or t == 3 or t == 4:
        return t
    else:
        label3 = tk.Label(text="Please choose a condition for your array.")
        label3.pack()


def generate_schematic():

    t = condition()
    get_textbox_values()

    if t == 1:
        get_size()
        create_crossbar_ideal(size)
        create_output_window(data, size)

    elif t == 2:
        get_size()
        create_crossbar_resistance(size)
        create_output_window(data, size)

    elif t == 3:
        get_size()
        create_crossbar_capacitance(size)
        create_output_window(data, size)

    elif t == 4:
        iv_characteristic()

    open_schematic(size, t)

def get_model():
    model2 = str(model_var.get())

    if model2 == '1' :
        model = 'hp'
    elif model2 == '2' :
        model = 'yakopcic'
    elif model2 == '3' :
        model = 'biolek'
    elif model2 == '4' :
        model = 'umich'
    elif model2 == '5' :
        model = 'knowm'
    else :
        label3 = tk.Label(text="Please choose a model.")
        label3.pack()

    name = 'memristor_' + model

    return name

def open_schematic(s, t) :

    # Ltspice .exe directory
    lt_directory = "C:\Program Files\LTC\LTspiceXVII"

    if t == 1:
        # Run schematic simulation (Ideal)
        subprocess.call(lt_directory + "\XVIIx64.exe -Open " + str(s) + "x" + str(s) + "_ideal.asc")
    elif t == 2:
        # Run schematic simulation (Line Resistance)
        subprocess.call(lt_directory + "\XVIIx64.exe -Open " + str(s) + "x" + str(s) + "_resistance.asc")
    elif t == 3:
        # Run schematic simulation (Line Resistance & Parasitic Capacitance)
        subprocess.call(lt_directory + "\XVIIx64.exe -Open " + str(s) + "x" + str(s) + "_capacitance.asc")


# Create 1x1 memristor schematic (Ideal)
def create_single_ideal(j):

    # Get memristor model
    name = get_model()

    # filename
    filename = str(j) + 'x' + str(j)
    # Schematic filename
    filename_asc = filename + '_ideal.asc'

    with open(filename_asc, 'w') as writer :
        # write into new file, original + newly created cells + blank line at the end
        file_list = ['Version 4\n', 'SHEET 1 3264 836\n', 'TEXT -248 344 Left 2 !.tran ' + simulation_time + '\n',
                     'TEXT 824 760 Left 2 !.lib 16n_nmos_pmos.txt\n',
                     'WIRE 144 80 -48 80\n', 'WIRE 848 80 144 80\n', 'WIRE 768 144 576 144\n',
                     'WIRE 144 160 144 80\n', 'WIRE 464 160 144 160\n','WIRE 640 176 576 176\n',
                     'WIRE -48 208 -48 80\n', 'WIRE 768 608 768 144\n', 'WIRE 864 656 768 656\n',
                     'WIRE 720 688 560 688\n', 'WIRE 768 704 768 688\n', 'WIRE 864 704 864 656\n',
                     'WIRE 864 704 768 704\n', 'WIRE 768 768 768 704\n',
                     'FLAG -48 288 0\n', 'FLAG 640 176 S1\n', 'FLAG 768 768 0\n', 'FLAG 560 768 0\n',
                     'SYMBOL voltage -48 192 R0\n', 'WINDOW 123 0 0 Left 0\n', 'WINDOW 39 24 124 Left 2\n',
                     'SYMATTR InstName VR1\n', 'SYMATTR Value PWL file=' + input_signal + '\n',
                     'SYMBOL ' + name + ' 512 160 R0\n', 'SYMATTR InstName M1\n',
                     'SYMBOL nmos4 720 608 R0\n', 'SYMATTR InstName L1\n', 'SYMATTR Value2 l=16n w=40n\n',
                     'SYMBOL voltage 560 672 R0\n', 'WINDOW 123 0 0 Left 0\n', 'WINDOW 39 0 0 Left 0\n',
                     'SYMATTR InstName VL1\n', 'SYMATTR Value PWL file=' + nmos_signal + '\n',
                     'FLAG 768 592 O1\n', ]

        for line in file_list :
            writer.write(line)

    writer.close()


# Create 1x1 memristor schematic (Line Resistance)
def create_single_resistance(j) :

    # get memristor model
    name = get_model()

    # filename
    filename = str(j) + 'x' + str(j)
    # Schematic filename
    filename_asc = filename + '_resistance.asc'

    with open(filename_asc, 'w') as writer :
        # write into new file, original + newly created cells + blank line at the end
        file_list = ['Version 4\n', 'SHEET 1 3264 836\n', 'TEXT -248 344 Left 2 !.tran ' + simulation_time + '\n',
                     'TEXT 856 744 Left 2 !.lib 16n_nmos_pmos.txt\n',
                     'WIRE 16 80 -48 80\n', 'WIRE 144 80 96 80\n', 'WIRE 848 80 144 80\n',
                     'WIRE 768 144 576 144\n', 'WIRE 144 160 144 80\n', 'WIRE 464 160 144 160\n',
                     'WIRE 640 176 576 176\n', 'WIRE 768 176 768 144\n', 'WIRE -48 208 -48 80\n',
                     'WIRE 768 608 768 256\n', 'WIRE 768 768 768 704\n', 'WIRE 864 656 768 656\n',
                     'WIRE 720 688 592 688\n', 'WIRE 864 704 864 656\n', 'WIRE 864 704 768 704\n',
                     'FLAG -48 288 0\n', 'FLAG 640 176 S1\n', 'FLAG 768 768 0\n', 'FLAG 592 768 0\n',
                     'SYMBOL voltage -48 192 R0\n', 'WINDOW 123 0 0 Left 0\n', 'WINDOW 39 24 124 Left 2\n',
                     'SYMATTR InstName VR1\n', 'SYMATTR Value PWL file=' + input_signal + '\n',
                     'SYMBOL ' + name + ' 512 160 R0\n', 'SYMATTR InstName M1\n', 'SYMBOL nmos4 720 608 R0\n',
                     'SYMATTR InstName L2\n', 'SYMATTR Value2 l=16n w=40n\n', 'SYMBOL voltage 592 672 R0\n',
                     'WINDOW 123 0 0 Left 0\n', 'WINDOW 39 0 0 Left 0\n', 'SYMATTR InstName VL1\n',
                     'SYMATTR Value PWL file=' + nmos_signal + '\n',
                     'SYMBOL res 112 64 R90\n', 'WINDOW 0 0 56 VBottom 2\n', 'WINDOW 3 32 56 VTop 2\n',
                     'SYMATTR InstName R1\n', 'SYMATTR Value ' + str(line_res) + '\n', 'SYMBOL res 752 160 R0\n',
                     'SYMATTR InstName R2\n', 'SYMATTR Value ' + str(line_res) + '\n', 'FLAG 768 592 O1\n', ]

        for line in file_list :
            writer.write(line)

    writer.close()


# Create 1x1 memristor schematic (Line Resistance & Parasitic Capacitance)
def create_single_capacitance(j):

    # get memristor model
    name = get_model()

    # filename
    filename = str(j) + 'x' + str(j)
    # Schematic filename
    filename_asc = filename + '_capacitance.asc'

    with open(filename_asc, 'w') as writer :
        # write into new file, original + newly created cells + blank line at the end
        file_list = ['Version 4\n', 'SHEET 1 3264 836\n', 'TEXT -248 344 Left 2 !.tran ' + simulation_time + '\n',
                     'WIRE 16 32 -48 32\n', 'WIRE 144 32 96 32\n', 'WIRE 848 32 144 32\n',
                     'WIRE 672 144 576 144\n', 'WIRE 768 144 672 144\n', 'WIRE 144 160 144 32\n',
                     'WIRE 464 160 144 160\n', 'WIRE 640 176 576 176\n', 'WIRE 768 176 768 144\n',
                     'WIRE -48 208 -48 32\n', 'WIRE 768 608 768 256\n', 'WIRE 768 768 768 720\n',
                     'WIRE 816 656 768 656\n', 'WIRE 720 688 624 688\n', 'WIRE 768 720 768 704\n',
                     'WIRE 816 720 816 656\n', 'WIRE 816 720 768 720\n',
                     'FLAG -48 288 0\n', 'FLAG 640 176 S1\n', 'FLAG 768 768 0\n',
                     'FLAG 80 160 0\n', 'FLAG 672 80 0\n', 'FLAG 624 768 0\n', 'FLAG 768 592 O1\n',
                     'SYMBOL voltage -48 192 R0\n', 'WINDOW 123 0 0 Left 0\n', 'WINDOW 39 24 124 Left 2\n', 'SYMATTR InstName VR1\n',
                     'SYMATTR Value PWL file=' + input_signal + '\n',
                     'SYMBOL ' + name + ' 512 160 R0\n', 'SYMATTR InstName M1\n', 'WINDOW 123 0 0 Left 0\n',
                     'WINDOW 39 24 124 Left 2\n',
                     'SYMBOL res 112 16 R90\n', 'WINDOW 0 0 56 VBottom 2\n', 'WINDOW 3 32 56 VTop 2\n',
                     'SYMATTR InstName R1\n', 'SYMATTR Value ' + str(line_res) + '\n', 'SYMBOL res 752 160 R0\n',
                     'SYMATTR InstName R2\n', 'SYMATTR Value ' + str(line_res) + '\n',
                     'SYMBOL cap 144 144 R90\n', 'WINDOW 0 0 32 VBottom 2\n', 'WINDOW 3 32 32 VTop 2\n',
                     'SYMATTR InstName C1\n', 'SYMATTR Value ' + str(gnd_cap) + '\n', 'SYMBOL cap 656 80 R0\n',
                     'SYMATTR InstName C2\n', 'SYMATTR Value ' + str(gnd_cap) + '\n',
                     'SYMATTR Value 2.012e-18\n', 'SYMBOL nmos4 720 608 R0\n', 'SYMATTR InstName L1\n',
                     'SYMBOL voltage 624 672 R0\n', 'WINDOW 123 0 0 Left 0\n', 'WINDOW 39 24 124 Left 2\n',
                     'SYMATTR InstName VL1\n', 'SYMATTR Value PWL file=nmos.txt\n',
                     'TEXT 872 704 Left 2 !.lib 16n_nmos_pmos.txt\n', ]

        for line in file_list :
            writer.write(line)

    writer.close()


# Create crossbar array schematic (Ideal)
def create_crossbar_ideal(z):

    if z == 1:
        create_single_ideal(z)

    else:
        # Create 1x1 schematic as a template to duplicate
        create_single_ideal(1)
        # Schematic template to modify and duplicate
        template_name = '1x1_ideal.asc'

        k = 1

        # Read template
        with open(template_name, "r") as reader:
            template_list = reader.readlines()
            default_list = list(template_list)
            start_list = list(template_list)
            topright_list = list(template_list)
            bottomright_list = list(template_list)

        # Top
        for lines in template_list:
            current = lines.split()
            if current[0] == 'SYMATTR' and current[1] == 'InstName':
                cellName = current[2]
                # Removes bottom nmos
                if cellName[0] == 'L':
                    rem_list = [template_list.index(lines) - 18, template_list.index(lines) - 17, template_list.index(lines) - 16, template_list.index(lines) - 15,
                                template_list.index(lines) - 14, template_list.index(lines) - 13, template_list.index(lines) - 10,
                                template_list.index(lines) - 9, template_list.index(lines) - 1,
                                template_list.index(lines), template_list.index(lines) + 1, template_list.index(lines) + 2,
                                template_list.index(lines) + 3, template_list.index(lines) + 4, template_list.index(lines) + 5,
                                template_list.index(lines) + 6,template_list.index(lines) + 7, ]
                    rem_list.reverse()
                    for i in rem_list:
                        start_list[i] = ""
                    continue

            try:
                current = " ".join(current) + "\n"
                start_list[start_list.index(lines)] = current
            except :
                pass

        while ("" in start_list):
            start_list.remove("")

        # delete the first 4 lines which is the asc version, sheet size, simulation run time, and nmos lib
        del start_list[0]
        del start_list[0]
        del start_list[0]
        del start_list[0]

        # Topright
        for lines in template_list:
            current = lines.split()
            if current[0] == 'SYMATTR' and current[1] == 'InstName':
                cellName = current[2]
                if cellName[1] == 'R':
                    rem_list = [template_list.index(lines) - 15, template_list.index(lines) - 13,
                                template_list.index(lines) - 12, template_list.index(lines) - 11, template_list.index(lines) - 10,
                                template_list.index(lines) - 9, template_list.index(lines) - 8, template_list.index(lines) - 7,
                                template_list.index(lines) - 5, template_list.index(lines) - 4, template_list.index(lines) - 3,
                                template_list.index(lines) - 2, template_list.index(lines) - 1,
                                template_list.index(lines), template_list.index(lines) + 1,
                                template_list.index(lines) + 4, template_list.index(lines) + 5,
                                template_list.index(lines) + 6, template_list.index(lines) + 7, template_list.index(lines) + 8,
                                template_list.index(lines) + 9, template_list.index(lines) + 10, template_list.index(lines) + 11,
                                template_list.index(lines) + 12, ]
                    rem_list.reverse()
                    for i in rem_list:
                        topright_list[i] = ""
                    continue

                try :
                    current = " ".join(current) + "\n"
                    topright_list[topright_list.index(lines)] = current
                except :
                    pass

            while ("" in topright_list):
                topright_list.remove("")

        del topright_list[0]
        del topright_list[0]
        del topright_list[0]
        del topright_list[0]

        # Bottomright
        for lines in template_list:
            current = lines.split()
            if current[0] == 'SYMATTR' and current[1] == 'InstName':
                cellName = current[2]
                if cellName[1] == 'R':
                    rem_list = [template_list.index(lines) - 15, template_list.index(lines) - 7,
                                template_list.index(lines) - 3,
                                template_list.index(lines) - 2, template_list.index(lines) - 1,
                                template_list.index(lines), template_list.index(lines) + 1]
                    rem_list.reverse()
                    for i in rem_list:
                        bottomright_list[i] = ""
                    continue

                try :
                    current = " ".join(current) + "\n"
                    bottomright_list[bottomright_list.index(lines)] = current
                except :
                    pass

            while ("" in bottomright_list):
                bottomright_list.remove("")

        del bottomright_list[0]
        del bottomright_list[0]
        del bottomright_list[0]
        del bottomright_list[0]

        # Top left starting memristor
        for lines in start_list:
            current = lines.split()

            if current[0] == 'WIRE':
                for n in [2, 4]:
                    current[n] = str(int(current[n]) - 272 * (z-1))
            elif current[0] == 'FLAG':
                current[2] = str(int(current[2]) - 272 * (z-1))
            elif current[0] == 'SYMBOL':
                current[3] = str(int(current[3]) - 272 * (z-1))

            # join the text together back into a line and put into the array to be appended
            try :
                current = " ".join(current) + "\n"
                start_list[start_list.index(lines)] = current
            except :
                pass

        top_copy = list(start_list)

        # First row second memristor
        for lines in topright_list:
            current = lines.split()
            if current[0] == 'WIRE':
                for n in [1, 3]:
                    current[n] = str(int(current[n]) + 854 * k)
                for n in [2, 4]:
                    current[n] = str(int(current[n]) - 272 * (z-1))
            elif current[0] == 'FLAG':
                current[1] = str(int(current[1]) + 854 * k)
                current[2] = str(int(current[2]) - 272 * (z-1))
            elif current[0] == 'SYMBOL':
                current[2] = str(int(current[2]) + 854 * k)
                current[3] = str(int(current[3]) - 272 * (z-1))

            # join the text together back into a line and put into the array to be appended
            try :
                current = " ".join(current) + "\n"
                topright_list[topright_list.index(lines)] = current
            except :
                pass

        topright_copy = list(topright_list)

        start_list.extend(topright_list)

        for y in range(z-2):
            # Other first row memristors
            for lines in topright_copy :
                current = lines.split()
                if current[0] == 'WIRE' :
                    for n in [1, 3] :
                        current[n] = str(int(current[n]) + 854)
                elif current[0] == 'FLAG' :
                    current[1] = str(int(current[1]) + 854)
                elif current[0] == 'SYMBOL' :
                    current[2] = str(int(current[2]) + 854)
                # join the text together back into a line and put into the array to be appended
                try :
                    current = " ".join(current) + "\n"
                    topright_copy[topright_copy.index(lines)] = current
                except :
                    pass
            start_list.extend(topright_copy)

        for y in range(z-2):
            # Other rows
            for lines in top_copy:
                current = lines.split()
                if current[0] == 'WIRE':
                    for n in [2, 4]:
                        current[n] = str(int(current[n]) + 272)
                elif current[0] == 'FLAG':
                    current[2] = str(int(current[2]) + 272)
                elif current[0] == 'SYMBOL':
                    current[3] = str(int(current[3]) + 272)

                # join the text together back into a line and put into the array to be appended
                try :
                    current = " ".join(current) + "\n"
                    top_copy[top_copy.index(lines)] = current
                except :
                    pass

            start_list.extend(top_copy)

            for lines in topright_list:
                current = lines.split()
                if current[0] == 'WIRE':
                    for n in [2, 4]:
                        current[n] = str(int(current[n]) + 272)
                elif current[0] == 'FLAG':
                    current[2] = str(int(current[2]) + 272)
                elif current[0] == 'SYMBOL':
                    current[3] = str(int(current[3]) + 272)

                # join the text together back into a line and put into the array to be appended
                try :
                    current = " ".join(current) + "\n"
                    topright_list[topright_list.index(lines)] = current
                except :
                    pass

            topright_copy=list(topright_list)
            start_list.extend(topright_list)

            for y in range(z - 2) :
                # Other first row memristors
                for lines in topright_copy :
                    current = lines.split()
                    if current[0] == 'WIRE' :
                        for n in [1, 3] :
                            current[n] = str(int(current[n]) + 854)
                    elif current[0] == 'FLAG' :
                        current[1] = str(int(current[1]) + 854)
                    elif current[0] == 'SYMBOL' :
                        current[2] = str(int(current[2]) + 854)
                    # join the text together back into a line and put into the array to be appended
                    try :
                        current = " ".join(current) + "\n"
                        topright_copy[topright_copy.index(lines)] = current
                    except :
                        pass
                start_list.extend(topright_copy)

        # Last row first memristor
        start_list.extend(default_list)

        # Last row memristors
        for y in range(z-1):
            for lines in bottomright_list:
                current = lines.split()
                if current[0] == 'WIRE':
                    for n in [1, 3]:
                        current[n] = str(int(current[n]) + 854)
                elif current[0] == 'FLAG':
                    current[1] = str(int(current[1]) + 854)
                elif current[0] == 'SYMBOL':
                    current[2] = str(int(current[2]) + 854)
                # join the text together back into a line and put into the array to be appended
                try:
                    current = " ".join(current) + "\n"
                    bottomright_list[bottomright_list.index(lines)] = current
                except:
                    pass

            # combine array into single entity
            start_list.extend(bottomright_list)

        # Component name variable that incrementally increases as new components are generated
        s = 1
        m = 1
        r = 1
        vr = 1
        vl = 1
        L = 1
        o = 1
        line_num = 0

        for line in start_list:
            current = line.split()
            if current[0] == 'FLAG':
                cellName = current[3]
                if cellName[0] == 'S':
                    current[3] = cellName[0] + str(s)
                    current = " ".join(current) + "\n"
                    start_list[line_num] = current
                    s = s + 1

                elif cellName[0] == 'O':
                    current[3] = cellName[0] + str(o)
                    current = " ".join(current) + "\n"
                    start_list[line_num] = current
                    o = o + 1

            elif current[0] == 'SYMATTR' and current[1] == 'InstName':
                cellName = current[2]
                if cellName[0] == 'M':
                    current[2] = cellName[0] + str(m)
                    m = m + 1
                elif cellName[0] == 'L':
                    current[2] = cellName[0] + str(L)
                    L = L + 1
                elif cellName[0] == 'R':
                    current[2] = cellName[0] + str(r)
                    r = r + 1
                elif cellName[1] == 'R':
                    current[2] = cellName[0] + cellName[1] + str(vr)
                    vr = vr + 1
                elif cellName[1] == 'L':
                    current[2] = cellName[0] + cellName[1] + str(vl)
                    vl = vl + 1

                current = " ".join(current) + "\n"
                start_list[line_num] = current

            line_num = line_num + 1

        filename_final = str(z) + "x" + str(z) + "_ideal.asc"
        with open(filename_final, 'w') as writer:
            # write into new file, original + newly created cells + blank line at the end
            for line in start_list:
                writer.write(line)

            writer.close()


# Create crossbar array schematic (Line Resistance)
def create_crossbar_resistance(z):

    if z == 1:
        create_single_resistance(1)

    else:
        # Create 1x1 schematic as a template to duplicate
        create_single_resistance(1)
        # Schematic template to modify and duplicate
        template_name = '1x1_resistance.asc'

        k = 1

        # Read template
        with open(template_name, "r") as reader:
            template_list = reader.readlines()
            default_list = list(template_list)
            start_list = list(template_list)
            topright_list = list(template_list)
            bottomright_list = list(template_list)

        # Top
        for lines in template_list:
            current = lines.split()
            if current[0] == 'SYMATTR' and current[1] == 'InstName':
                cellName = current[2]
                # Removes bottom load resistor
                if cellName[0] == 'L':
                    rem_list = [template_list.index(lines) - 17, template_list.index(lines) - 16, template_list.index(lines) - 15,
                                template_list.index(lines) - 14, template_list.index(lines) - 13, template_list.index(lines) - 10,
                                template_list.index(lines) - 9, template_list.index(lines) - 1,
                                template_list.index(lines), template_list.index(lines) + 1, template_list.index(lines) + 2,
                                template_list.index(lines) + 3, template_list.index(lines) + 4, template_list.index(lines) + 5,
                                template_list.index(lines) + 6, template_list.index(lines) + 15,]
                    rem_list.reverse()
                    for i in rem_list:
                        start_list[i] = ""
                    continue

            try:
                current = " ".join(current) + "\n"
                start_list[start_list.index(lines)] = current
            except :
                pass

        while ("" in start_list):
            start_list.remove("")

        # delete the first 2 lines which is the asc version and sheet size
        del start_list[0]
        del start_list[0]
        del start_list[0]
        del start_list[0]

        # Topright
        for lines in template_list:
            current = lines.split()
            if current[0] == 'SYMATTR' and current[1] == 'InstName':
                cellName = current[2]
                if cellName[1] == 'R':
                    rem_list = [template_list.index(lines) - 14,
                                template_list.index(lines) - 12, template_list.index(lines) - 11, template_list.index(lines) - 10,
                                template_list.index(lines) - 9, template_list.index(lines) - 8, template_list.index(lines) - 7,
                                template_list.index(lines) - 5, template_list.index(lines) - 4, template_list.index(lines) - 3,
                                template_list.index(lines) - 2, template_list.index(lines) - 1,
                                template_list.index(lines), template_list.index(lines) + 1,
                                template_list.index(lines) + 4, template_list.index(lines) + 5,
                                template_list.index(lines) + 6, template_list.index(lines) + 7, template_list.index(lines) + 8,
                                template_list.index(lines) + 9, template_list.index(lines) + 10, template_list.index(lines) + 11,
                                template_list.index(lines) + 20, ]
                    rem_list.reverse()
                    for i in rem_list:
                        topright_list[i] = ""
                    continue

                try :
                    current = " ".join(current) + "\n"
                    topright_list[topright_list.index(lines)] = current
                except :
                    pass

            while ("" in topright_list):
                topright_list.remove("")

        del topright_list[0]
        del topright_list[0]
        del topright_list[0]
        del topright_list[0]

        # Bottomright
        for lines in template_list:
            current = lines.split()
            if current[0] == 'SYMATTR' and current[1] == 'InstName':
                cellName = current[2]
                if cellName[1] == 'R':
                    rem_list = [template_list.index(lines) - 14, template_list.index(lines) - 7,
                                template_list.index(lines) - 3,
                                template_list.index(lines) - 2, template_list.index(lines) - 1,
                                template_list.index(lines), template_list.index(lines) + 1,]
                    rem_list.reverse()
                    for i in rem_list:
                        bottomright_list[i] = ""
                    continue

                try :
                    current = " ".join(current) + "\n"
                    bottomright_list[bottomright_list.index(lines)] = current
                except :
                    pass

            while ("" in bottomright_list):
                bottomright_list.remove("")

        del bottomright_list[0]
        del bottomright_list[0]
        del bottomright_list[0]
        del bottomright_list[0]

        # Top left starting memristor
        for lines in start_list:
            current = lines.split()

            if current[0] == 'WIRE':
                for n in [2, 4]:
                    current[n] = str(int(current[n]) - 272 * (z-1))
            elif current[0] == 'FLAG':
                current[2] = str(int(current[2]) - 272 * (z-1))
            elif current[0] == 'SYMBOL':
                current[3] = str(int(current[3]) - 272 * (z-1))

            # join the text together back into a line and put into the array to be appended
            try :
                current = " ".join(current) + "\n"
                start_list[start_list.index(lines)] = current
            except :
                pass

        top_copy = list(start_list)

        # First row second memristor
        for lines in topright_list:
            current = lines.split()
            if current[0] == 'WIRE':
                for n in [1, 3]:
                    current[n] = str(int(current[n]) + 854 * k)
                for n in [2, 4]:
                    current[n] = str(int(current[n]) - 272 * (z-1))
            elif current[0] == 'FLAG':
                current[1] = str(int(current[1]) + 854 * k)
                current[2] = str(int(current[2]) - 272 * (z-1))
            elif current[0] == 'SYMBOL':
                current[2] = str(int(current[2]) + 854 * k)
                current[3] = str(int(current[3]) - 272 * (z-1))

            # join the text together back into a line and put into the array to be appended
            try :
                current = " ".join(current) + "\n"
                topright_list[topright_list.index(lines)] = current
            except :
                pass

        topright_copy = list(topright_list)

        start_list.extend(topright_list)

        for y in range(z-2):
            # Other first row memristors
            for lines in topright_copy :
                current = lines.split()
                if current[0] == 'WIRE' :
                    for n in [1, 3] :
                        current[n] = str(int(current[n]) + 854)
                elif current[0] == 'FLAG' :
                    current[1] = str(int(current[1]) + 854)
                elif current[0] == 'SYMBOL' :
                    current[2] = str(int(current[2]) + 854)
                # join the text together back into a line and put into the array to be appended
                try :
                    current = " ".join(current) + "\n"
                    topright_copy[topright_copy.index(lines)] = current
                except :
                    pass
            start_list.extend(topright_copy)

        for y in range(z-2):
            # Other rows
            for lines in top_copy:
                current = lines.split()
                if current[0] == 'WIRE':
                    for n in [2, 4]:
                        current[n] = str(int(current[n]) + 272)
                elif current[0] == 'FLAG':
                    current[2] = str(int(current[2]) + 272)
                elif current[0] == 'SYMBOL':
                    current[3] = str(int(current[3]) + 272)

                # join the text together back into a line and put into the array to be appended
                try :
                    current = " ".join(current) + "\n"
                    top_copy[top_copy.index(lines)] = current
                except :
                    pass

            start_list.extend(top_copy)

            for lines in topright_list:
                current = lines.split()
                if current[0] == 'WIRE':
                    for n in [2, 4]:
                        current[n] = str(int(current[n]) + 272)
                elif current[0] == 'FLAG':
                    current[2] = str(int(current[2]) + 272)
                elif current[0] == 'SYMBOL':
                    current[3] = str(int(current[3]) + 272)

                # join the text together back into a line and put into the array to be appended
                try :
                    current = " ".join(current) + "\n"
                    topright_list[topright_list.index(lines)] = current
                except :
                    pass

            topright_copy=list(topright_list)
            start_list.extend(topright_list)

            for y in range(z - 2) :
                # Other first row memristors
                for lines in topright_copy :
                    current = lines.split()
                    if current[0] == 'WIRE' :
                        for n in [1, 3] :
                            current[n] = str(int(current[n]) + 854)
                    elif current[0] == 'FLAG' :
                        current[1] = str(int(current[1]) + 854)
                    elif current[0] == 'SYMBOL' :
                        current[2] = str(int(current[2]) + 854)
                    # join the text together back into a line and put into the array to be appended
                    try :
                        current = " ".join(current) + "\n"
                        topright_copy[topright_copy.index(lines)] = current
                    except :
                        pass
                start_list.extend(topright_copy)

        # Last row first memristor
        start_list.extend(default_list)

        # Last row memristors
        for y in range(z-1):
            for lines in bottomright_list:
                current = lines.split()
                if current[0] == 'WIRE':
                    for n in [1, 3]:
                        current[n] = str(int(current[n]) + 854)
                elif current[0] == 'FLAG':
                    current[1] = str(int(current[1]) + 854)
                elif current[0] == 'SYMBOL':
                    current[2] = str(int(current[2]) + 854)
                # join the text together back into a line and put into the array to be appended
                try:
                    current = " ".join(current) + "\n"
                    bottomright_list[bottomright_list.index(lines)] = current
                except:
                    pass

            # combine array into single entity
            start_list.extend(bottomright_list)

        # Component name variable that incrementally increases as new components are generated
        s = 1
        m = 1
        r = 1
        vr = 1
        vl = 1
        L = 1
        o = 1
        line_num = 0

        for line in start_list:
            current = line.split()
            if current[0] == 'FLAG':
                cellName = current[3]
                if cellName[0] == 'S':
                    current[3] = cellName[0] + str(s)
                    current = " ".join(current) + "\n"
                    start_list[line_num] = current
                    s = s + 1

                elif cellName[0] == 'O':
                    current[3] = cellName[0] + str(o)
                    current = " ".join(current) + "\n"
                    start_list[line_num] = current
                    o = o + 1

            elif current[0] == 'SYMATTR' and current[1] == 'InstName':
                cellName = current[2]
                if cellName[0] == 'M':
                    current[2] = cellName[0] + str(m)
                    m = m + 1
                elif cellName[0] == 'L':
                    current[2] = cellName[0] + str(L)
                    L = L + 1
                elif cellName[0] == 'R':
                    current[2] = cellName[0] + str(r)
                    r = r + 1
                elif cellName[1] == 'R':
                    current[2] = cellName[0] + cellName[1] + str(vr)
                    vr = vr + 1
                elif cellName[1] == 'L':
                    current[2] = cellName[0] + cellName[1] + str(vl)
                    vl = vl + 1

                current = " ".join(current) + "\n"
                start_list[line_num] = current

            line_num = line_num + 1

        filename_final = str(z) + "x" + str(z) + "_resistance.asc"
        with open(filename_final, 'w') as writer:
            # write into new file, original + newly created cells + blank line at the end
            for line in start_list:
                writer.write(line)

            writer.close()


# Capacitance template (topleft)
def topleft_capacitance():

    # get memristor model
    name = get_model()

    # Schematic filename
    filename_asc = 'topleft_capacitance.asc'

    with open(filename_asc, 'w') as writer :
        # write into new file, original + newly created cells + blank line at the end
        file_list = ['Version 4\n', 'SHEET 1 3376 1172\n', 'TEXT -592 -624 Left 2 !.tran ' + simulation_time + '\n',
                     'WIRE -304 -928 -400 -928\n', 'WIRE -160 -928 -304 -928\n', 'WIRE -48 -928 -80 -928\n',
                     'WIRE 976 -928 -48 -928\n', 'WIRE -400 -864 -400 -928\n', 'WIRE 192 -784 96 -784\n',
                     'WIRE 288 -784 192 -784\n', 'WIRE -160 -768 -176 -768\n', 'WIRE -48 -768 -48 -928\n',
                     'WIRE -48 -768 -96 -768\n', 'WIRE -16 -768 -48 -768\n', 'WIRE 128 -752 96 -752\n',
                     'WIRE 288 -704 288 -784\n', 'WIRE -304 -640 -304 -928\n', 'WIRE 288 -528 288 -624\n',
                     'WIRE 640 -528 288 -528\n', 'WIRE -304 -480 -304 -576\n', 'WIRE 976 -480 -304 -480\n',
                     'WIRE 288 -80 288 -528\n', 'FLAG -400 -784 0\n', 'FLAG 128 -752 S1\n',
                     'FLAG -176 -768 0\n', 'FLAG 192 -848 0\n',
                     'FLAG -304 -992 0\n', 'FLAG 224 -528 0\n', 'SYMBOL voltage -400 -880 R0\n',
                     'WINDOW 3 -225 133 Left 2\n', 'WINDOW 123 0 0 Left 0\n', 'WINDOW 39 0 0 Left 0\n',
                     'SYMATTR Value PWL file=' + input_signal + '\n',
                     'SYMATTR InstName VR1\n', 'SYMBOL res -64 -944 R90\n', 'WINDOW 0 0 56 VBottom 2\n',
                     'WINDOW 3 32 56 VTop 2\n', 'SYMATTR InstName R9\n', 'SYMATTR Value ' + str(line_res) + '\n',
                     'SYMBOL res 304 -608 R180\n', 'WINDOW 0 36 76 Left 2\n', 'WINDOW 3 36 40 Left 2\n',
                     'SYMATTR InstName R10\n', 'SYMATTR Value ' + str(line_res) + '\n', 'SYMBOL cap -96 -784 R90\n',
                     'WINDOW 0 0 32 VBottom 2\n', 'WINDOW 3 32 32 VTop 2\n', 'SYMATTR InstName C9\n',
                     'SYMATTR Value ' + str(gnd_cap) + '\n', 'SYMBOL cap 208 -784 R180\n', 'WINDOW 0 24 56 Left 2\n',
                     'WINDOW 3 24 8 Left 2\n', 'SYMATTR InstName C1\n', 'SYMATTR Value ' + str(gnd_cap) + '\n',
                     'SYMBOL cap -320 -640 R0\n', 'SYMATTR InstName C_R3\n', 'SYMATTR Value 1.6e-18\n',
                     'SYMBOL cap -320 -992 R0\n', 'SYMATTR InstName C2\n', 'SYMATTR Value ' + str(gnd_cap) + '\n',
                     'SYMBOL cap 288 -544 R90\n', 'WINDOW 0 0 32 VBottom 2\n', 'WINDOW 3 32 32 VTop 2\n',
                     'SYMATTR InstName C3\n', 'SYMATTR Value ' + str(gnd_cap) + '\n',
                     'SYMBOL ' + name + ' 32 -768 R0\n', 'SYMATTR InstName M1\n',  'TEXT -680 -584 Left 2 !.lib 16n_nmos_pmos.txt\n', ]

        for line in file_list :
            writer.write(line)

    writer.close()


# Capacitance template (top)
def top_capacitance():

    # get memristor model
    name = get_model()

    # Schematic filename
    filename_asc = 'top_capacitance.asc'

    with open(filename_asc, 'w') as writer :
        # write into new file, original + newly created cells + blank line at the end
        file_list = ['Version 4\n', 'SHEET 1 3376 1172\n', 'WIRE 480 -928 336 -928\n',
                     'WIRE 592 -928 560 -928\n', 'WIRE 976 -928 592 -928\n', 'WIRE 336 -928 96 -928\n',
                     'WIRE 832 -784 736 -784\n', 'WIRE 928 -784 832 -784\n', 'WIRE 592 -768 592 -928\n',
                     'WIRE 592 -768 528 -768\n', 'WIRE 624 -768 592 -768\n', 'WIRE 768 -752 736 -752\n',
                     'WIRE 928 -736 928 -784\n', 'WIRE 336 -640 336 -928\n', 'WIRE 640 -528 288 -528\n',
                     'WIRE 928 -528 928 -656\n', 'WIRE 928 -528 704 -528\n', 'WIRE 976 -528 928 -528\n',
                     'WIRE 336 -480 336 -576\n', 'WIRE 928 -480 928 -528\n', 'FLAG 768 -752 S2\n',
                     'FLAG 832 -848 0\n', 'FLAG 464 -768 0\n',
                     'FLAG 336 -992 0\n', 'SYMBOL res 576 -944 R90\n', 'WINDOW 0 0 56 VBottom 2\n',
                     'WINDOW 3 32 56 VTop 2\n', 'SYMATTR InstName R11\n', 'SYMATTR Value ' + str(line_res) + '\n',
                     'SYMBOL res 944 -640 R180\n', 'WINDOW 0 36 76 Left 2\n', 'WINDOW 3 36 40 Left 2\n',
                     'SYMATTR InstName R12\n', 'SYMATTR Value ' + str(line_res) + '\n', 'SYMBOL cap 528 -784 R90\n',
                     'WINDOW 0 0 32 VBottom 2\n', 'WINDOW 3 32 32 VTop 2\n', 'SYMATTR InstName C10\n',
                     'SYMATTR Value ' + str(gnd_cap) + '\n', 'SYMBOL cap 848 -784 R180\n', 'WINDOW 0 24 56 Left 2\n',
                     'WINDOW 3 24 8 Left 2\n', 'SYMATTR InstName C12\n', 'SYMATTR Value ' + str(gnd_cap) + '\n',
                     'SYMBOL cap 320 -640 R0\n', 'SYMATTR InstName C4\n', 'SYMATTR Value ' + str(line_cap) + '\n',
                     'SYMBOL cap 640 -544 M90\n', 'WINDOW 0 0 32 VBottom 2\n', 'WINDOW 3 32 32 VTop 2\n',
                     'SYMATTR InstName C2\n', 'SYMATTR Value ' + str(line_cap) + '\n', 'SYMBOL cap 320 -992 R0\n',
                     'SYMATTR InstName C3\n', 'SYMATTR Value ' + str(gnd_cap) + '\n',
                     'SYMBOL ' + name + ' 672 -768 R0\n', 'SYMATTR InstName M8\n', ]

        for line in file_list :
            writer.write(line)

    writer.close()


# Capacitance template (topright)
def topright_capacitance():

    # get memristor model
    name = get_model()

    # Schematic filename
    filename_asc ='topright_capacitance.asc'

    with open(filename_asc, 'w') as writer :
        # write into new file, original + newly created cells + blank line at the end
        file_list = ['Version 4\n', 'SHEET 1 3376 1172\n', 'WIRE 1744 -928 1616 -928\n',
                     'WIRE 1872 -928 1824 -928\n', 'WIRE 2320 -928 1872 -928\n', 'WIRE 2112 -784 2016 -784\n',
                     'WIRE 2208 -784 2112 -784\n', 'WIRE 1872 -768 1872 -928\n', 'WIRE 1872 -768 1824 -768\n',
                     'WIRE 1904 -768 1872 -768\n', 'WIRE 2048 -752 2016 -752\n', 'WIRE 2208 -752 2208 -784\n',
                     'WIRE 1616 -640 1616 -928\n', 'WIRE 1920 -528 1568 -528\n', 'WIRE 2208 -528 2208 -672\n',
                     'WIRE 2208 -528 1984 -528\n', 'WIRE 1616 -480 1616 -576\n', 'WIRE 2208 -336 2208 -528\n',
                     'FLAG 2048 -752 S4\n', 'FLAG 2112 -848 0\n',
                     'FLAG 1760 -768 0\n', 'FLAG 1616 -992 0\n', 'FLAG 2272 -528 0\n',
                     'SYMBOL res 1840 -944 R90\n', 'WINDOW 0 0 56 VBottom 2\n', 'WINDOW 3 32 56 VTop 2\n',
                     'SYMATTR InstName R27\n', 'SYMATTR Value ' + str(line_res) + '\n', 'SYMBOL res 2224 -656 R180\n',
                     'WINDOW 0 36 76 Left 2\n', 'WINDOW 3 36 40 Left 2\n', 'SYMATTR InstName R28\n',
                     'SYMATTR Value ' + str(line_res) + '\n', 'SYMBOL cap 1824 -784 R90\n', 'WINDOW 0 0 32 VBottom 2\n',
                     'WINDOW 3 32 32 VTop 2\n', 'SYMATTR InstName C27\n', 'SYMATTR Value ' + str(gnd_cap) + '\n',
                     'SYMBOL cap 2128 -784 R180\n', 'WINDOW 0 24 56 Left 2\n', 'WINDOW 3 24 8 Left 2\n',
                     'SYMATTR InstName C28\n', 'SYMATTR Value ' + str(gnd_cap) + '\n', 'SYMBOL cap 1600 -640 R0\n',
                     'SYMATTR InstName C10\n', 'SYMATTR Value ' + str(line_cap) + '\n', 'SYMBOL cap 1920 -544 M90\n',
                     'WINDOW 0 0 32 VBottom 2\n', 'WINDOW 3 32 32 VTop 2\n', 'SYMATTR InstName C11\n',
                     'SYMATTR Value ' + str(line_cap) + '\n', 'SYMBOL cap 1600 -992 R0\n', 'SYMATTR InstName C12\n',
                     'SYMATTR Value ' + str(gnd_cap) + '\n', 'SYMBOL cap 2272 -544 R90\n', 'WINDOW 0 0 32 VBottom 2\n',
                     'WINDOW 3 32 32 VTop 2\n', 'SYMATTR InstName C38\n', 'SYMATTR Value ' + str(gnd_cap) + '\n',
                     'SYMBOL ' + name + ' 1952 -768 R0\n', 'SYMATTR InstName M32\n', ]

        for line in file_list :
            writer.write(line)

    writer.close()


# Capacitance template (left)
def left_capacitance():

    # get memristor model
    name = get_model()

    # Schematic filename
    filename_asc = 'left_capacitance.asc'

    with open(filename_asc, 'w') as writer :
        # write into new file, original + newly created cells + blank line at the end
        file_list = ['Version 4\n', 'SHEET 1 3376 1172\n', 'WIRE -304 -480 -304 -576\n',
                     'WIRE -304 -480 -400 -480\n', 'WIRE -192 -480 -304 -480\n', 'WIRE -64 -480 -112 -480\n',
                     'WIRE 336 -480 -64 -480\n', 'WIRE -400 -416 -400 -480\n', 'WIRE 192 -336 96 -336\n',
                     'WIRE 288 -336 192 -336\n', 'WIRE -160 -320 -176 -320\n', 'WIRE -64 -320 -64 -480\n',
                     'WIRE -64 -320 -96 -320\n', 'WIRE -16 -320 -64 -320\n', 'WIRE 128 -304 96 -304\n',
                     'WIRE 288 -288 288 -336\n', 'WIRE -304 -192 -304 -480\n', 'WIRE 288 -80 288 -208\n',
                     'WIRE 640 -80 288 -80\n', 'WIRE -304 -32 -304 -128\n', 'WIRE -304 -32 -400 -32\n',
                     'WIRE 336 -32 -304 -32\n', 'WIRE -304 32 -304 -32\n', 'WIRE 288 112 288 -80\n',
                     'FLAG -400 -336 0\n', 'FLAG 128 -304 S5\n',
                     'FLAG -176 -320 0\n', 'FLAG 192 -400 0\n', 'FLAG 224 -80 0\n',
                     'SYMBOL voltage -400 -432 R0\n', 'WINDOW 3 -225 133 Left 2\n', 'WINDOW 123 0 0 Left 0\n',
                     'WINDOW 39 0 0 Left 0\n', 'SYMATTR Value PWL file=' + input_signal + '\n',
                     'SYMATTR InstName VR2\n', 'SYMBOL res -96 -496 R90\n', 'WINDOW 0 0 56 VBottom 2\n',
                     'WINDOW 3 32 56 VTop 2\n', 'SYMATTR InstName R5\n', 'SYMATTR Value ' + str(line_res) + '\n',
                     'SYMBOL res 304 -192 R180\n', 'WINDOW 0 36 76 Left 2\n', 'WINDOW 3 36 40 Left 2\n',
                     'SYMATTR InstName R6\n', 'SYMATTR Value ' + str(line_res) + '\n', 'SYMBOL cap -96 -336 R90\n',
                     'WINDOW 0 0 32 VBottom 2\n', 'WINDOW 3 32 32 VTop 2\n', 'SYMATTR InstName C5\n',
                     'SYMATTR Value ' + str(gnd_cap) + '\n', 'SYMBOL cap 208 -336 R180\n', 'WINDOW 0 24 56 Left 2\n',
                     'WINDOW 3 24 8 Left 2\n', 'SYMATTR InstName C7\n', 'SYMATTR Value ' + str(gnd_cap) + '\n',
                     'SYMBOL cap -320 -192 R0\n', 'SYMATTR InstName C1\n', 'SYMATTR Value ' + str(line_cap) + '\n',
                     'SYMBOL cap 288 -96 R90\n', 'WINDOW 0 0 32 VBottom 2\n', 'WINDOW 3 32 32 VTop 2\n',
                     'SYMATTR InstName C40\n', 'SYMATTR Value ' + str(gnd_cap) + '\n',
                     'SYMBOL ' + name + ' 32 -320 R0\n', 'SYMATTR InstName M2\n', ]

        for line in file_list :
            writer.write(line)

    writer.close()


# Capacitance template (middle)
def middle_capacitance():

    # get memristor model
    name = get_model()

    # Schematic filename
    filename_asc = 'middle_capacitance.asc'

    with open(filename_asc, 'w') as writer :
        # write into new file, original + newly created cells + blank line at the end
        file_list = ['Version 4\n', 'SHEET 1 3376 1172\n', 'WIRE 336 -480 336 -576\n',
                     'WIRE 336 -480 -160 -480\n', 'WIRE 480 -480 336 -480\n', 'WIRE 592 -480 560 -480\n',
                     'WIRE 1120 -480 592 -480\n', 'WIRE 832 -336 736 -336\n', 'WIRE 928 -336 928 -608\n',
                     'WIRE 928 -336 832 -336\n', 'WIRE 592 -320 592 -480\n', 'WIRE 592 -320 544 -320\n',
                     'WIRE 624 -320 592 -320\n', 'WIRE 768 -304 736 -304\n', 'WIRE 928 -288 928 -336\n',
                     'WIRE 336 -192 336 -480\n', 'WIRE 640 -80 288 -80\n', 'WIRE 928 -80 928 -208\n',
                     'WIRE 928 -80 704 -80\n', 'WIRE 1280 -80 928 -80\n', 'WIRE 928 112 928 -80\n',
                     'WIRE 336 -80 336 -128\n', 'WIRE 336 -80 288 -80\n',
                     'FLAG 768 -304 S6\n', 'FLAG 832 -400 0\n',
                     'FLAG 480 -320 0\n', 'SYMBOL res 576 -496 R90\n', 'WINDOW 0 0 56 VBottom 2\n',
                     'WINDOW 3 32 56 VTop 2\n', 'SYMATTR InstName R7\n', 'SYMATTR Value ' + str(line_res) + '\n',
                     'SYMBOL res 944 -192 R180\n', 'WINDOW 0 36 76 Left 2\n', 'WINDOW 3 36 40 Left 2\n',
                     'SYMATTR InstName R8\n', 'SYMATTR Value ' + str(line_res) + '\n', 'SYMBOL cap 544 -336 R90\n',
                     'WINDOW 0 0 32 VBottom 2\n', 'WINDOW 3 32 32 VTop 2\n', 'SYMATTR InstName C6\n',
                     'SYMATTR Value ' + str(gnd_cap) + '\n', 'SYMBOL cap 848 -336 R180\n', 'WINDOW 0 24 56 Left 2\n',
                     'WINDOW 3 24 8 Left 2\n', 'SYMATTR InstName C8\n', 'SYMATTR Value ' + str(gnd_cap) + '\n',
                     'SYMBOL cap 320 -192 R0\n', 'SYMATTR InstName C2\n', 'SYMATTR Value ' + str(line_cap) + '\n',
                     'SYMBOL cap 640 -96 M90\n', 'WINDOW 0 0 32 VBottom 2\n', 'WINDOW 3 32 32 VTop 2\n',
                     'SYMATTR InstName C1\n', 'SYMATTR Value ' + str(line_cap) + '\n',
                     'SYMBOL ' + name + ' 672 -320 R0\n', 'SYMATTR InstName M27\n', ]

        for line in file_list :
            writer.write(line)

    writer.close()


# Capacitance template (right)
def right_capacitance():

    # get memristor model
    name = get_model()

    # Schematic filename
    filename_asc = 'right_capacitance.asc'

    with open(filename_asc, 'w') as writer :
        # write into new file, original + newly created cells + blank line at the end
        file_list = ['Version 4\n', 'SHEET 1 3376 1172\n', 'WIRE 1616 -480 1616 -576\n',
                     'WIRE 1728 -480 1616 -480\n', 'WIRE 1872 -480 1808 -480\n', 'WIRE 2320 -480 1872 -480\n',
                     'WIRE 2112 -336 2016 -336\n', 'WIRE 2208 -336 2208 -592\n', 'WIRE 2208 -336 2112 -336\n',
                     'WIRE 1872 -320 1872 -480\n', 'WIRE 1872 -320 1824 -320\n', 'WIRE 1904 -320 1872 -320\n',
                     'WIRE 2048 -304 2016 -304\n', 'WIRE 2208 -272 2208 -336\n', 'WIRE 1616 -192 1616 -480\n',
                     'WIRE 1920 -80 1568 -80\n', 'WIRE 2208 -80 2208 -192\n', 'WIRE 2208 -80 1984 -80\n',
                     'WIRE 2208 112 2208 -80\n', 'FLAG 2048 -304 S8\n',
                     'FLAG 2112 -400 0\n', 'FLAG 1760 -320 0\n', 'FLAG 2272 -80 0\n',
                     'SYMBOL res 1824 -496 R90\n', 'WINDOW 0 0 56 VBottom 2\n', 'WINDOW 3 32 56 VTop 2\n',
                     'SYMATTR InstName R25\n', 'SYMATTR Value ' + str(line_res) + '\n', 'SYMBOL res 2224 -176 R180\n',
                     'WINDOW 0 36 76 Left 2\n', 'WINDOW 3 36 40 Left 2\n', 'SYMATTR InstName R26\n',
                     'SYMATTR Value ' + str(line_res) + '\n', 'SYMBOL cap 1824 -336 R90\n', 'WINDOW 0 0 32 VBottom 2\n',
                     'WINDOW 3 32 32 VTop 2\n', 'SYMATTR InstName C25\n', 'SYMATTR Value ' + str(gnd_cap) + '\n',
                     'SYMBOL cap 2128 -336 R180\n', 'WINDOW 0 24 56 Left 2\n', 'WINDOW 3 24 8 Left 2\n',
                     'SYMATTR InstName C26\n', 'SYMATTR Value ' + str(gnd_cap) + '\n', 'SYMBOL cap 1600 -192 R0\n',
                     'SYMATTR InstName C9\n', 'SYMATTR Value ' + str(line_cap) + '\n', 'SYMBOL cap 1920 -96 M90\n',
                     'WINDOW 0 0 32 VBottom 2\n', 'WINDOW 3 32 32 VTop 2\n', 'SYMATTR InstName C12\n',
                     'SYMATTR Value ' + str(line_cap) + '\n', 'SYMBOL cap 2272 -96 R90\n', 'WINDOW 0 0 32 VBottom 2\n',
                     'WINDOW 3 32 32 VTop 2\n', 'SYMATTR InstName C39\n', 'SYMATTR Value ' + str(gnd_cap) + '\n',
                     'SYMBOL ' + name + ' 1952 -320 R0\n', 'SYMATTR InstName M32\n', ]

        for line in file_list :
            writer.write(line)

    writer.close()


# Capacitance template (bottomleft)
def bottomleft_capacitance():

    # get memristor model
    name = get_model()

    # Schematic filename
    filename_asc = 'bottomleft_capacitance.asc'

    with open(filename_asc, 'w') as writer :
        # write into new file, original + newly created cells + blank line at the end
        file_list = ['Version 4\n', 'SHEET 1 3376 1380\n', 'WIRE -304 416 -304 320\n',
                     'WIRE -304 416 -400 416\n', 'WIRE -160 416 -304 416\n', 'WIRE -48 416 -80 416\n',
                     'WIRE 480 416 -48 416\n', 'WIRE -400 480 -400 416\n', 'WIRE 192 608 96 608\n',
                     'WIRE 208 608 192 608\n', 'WIRE 288 608 288 112\n', 'WIRE -160 624 -176 624\n',
                     'WIRE -48 624 -48 416\n', 'WIRE -48 624 -96 624\n', 'WIRE -16 624 -48 624\n',
                     'WIRE 128 640 96 640\n', 'WIRE 288 768 288 608\n', 'WIRE 656 768 288 768\n',
                     'WIRE 288 1280 288 768\n', 'WIRE 336 1248 288 1248\n', 'WIRE 240 1280 160 1280\n',
                     'WIRE 288 1312 288 1296\n', 'WIRE 336 1312 336 1248\n', 'WIRE 336 1312 288 1312\n',
                     'WIRE 288 1360 288 1312\n',
                     'FLAG -400 560 0\n', 'FLAG 128 640 S13\n', 'FLAG 288 1184 O1\n',
                     'FLAG -176 624 0\n', 'FLAG 192 544 0\n', 'FLAG 160 1360 0\n',
                     'FLAG -304 480 0\n', 'FLAG 224 768 0\n', 'FLAG 288 1360 0\n',
                     'SYMBOL voltage -400 464 R0\n', 'WINDOW 3 -225 133 Left 2\n', 'WINDOW 123 0 0 Left 0\n',
                     'WINDOW 39 0 0 Left 0\n', 'SYMATTR Value PWL file=' + input_signal + '\n',
                     'SYMATTR InstName VR4\n', 'SYMBOL res -64 400 R90\n', 'WINDOW 0 0 56 VBottom 2\n',
                     'WINDOW 3 32 56 VTop 2\n', 'SYMATTR InstName R3\n', 'SYMATTR Value ' + str(line_res) + '\n',
                     'SYMBOL res 304 592 R90\n', 'WINDOW 0 0 56 VBottom 2\n', 'WINDOW 3 32 56 VTop 2\n',
                     'SYMATTR InstName R3\n', 'SYMATTR Value ' + str(line_res) + '\n', 'SYMBOL cap -96 608 R90\n',
                     'WINDOW 0 0 32 VBottom 2\n', 'WINDOW 3 32 32 VTop 2\n', 'SYMATTR InstName C3\n',
                     'SYMATTR Value ' + str(gnd_cap) + '\n', 'SYMBOL cap 208 608 R180\n', 'WINDOW 0 24 56 Left 2\n',
                     'WINDOW 3 24 8 Left 2\n', 'SYMATTR InstName C3\n', 'SYMATTR Value ' + str(gnd_cap) + '\n',
                     'SYMBOL cap -320 416 R0\n', 'SYMATTR InstName C36\n', 'SYMATTR Value ' + str(gnd_cap) + '\n',
                     'SYMBOL cap 288 752 R90\n', 'WINDOW 0 0 32 VBottom 2\n', 'WINDOW 3 32 32 VTop 2\n',
                     'SYMATTR InstName C44\n', 'SYMATTR Value ' + str(gnd_cap) + '\n',
                     'SYMBOL ' + name + ' 32 624 R0\n', 'SYMATTR InstName M4\n',
                     'SYMBOL nmos4 240 1200 R0\n', 'SYMATTR InstName L1\n', 'SYMBOL voltage 160 1264 R0\n',
                     'WINDOW 123 0 0 Left 0\n', 'WINDOW 39 0 0 Left 0\n', 'SYMATTR InstName VL1\n',
                     'SYMATTR Value PWL file=nmos.txt\n', ]

        for line in file_list :
            writer.write(line)

    writer.close()


# Capacitance template (bottom)
def bottom_capacitance():

    # get memristor model
    name = get_model()

    # Schematic filename
    filename_asc = 'bottom_capacitance.asc'

    with open(filename_asc, 'w') as writer :
        # write into new file, original + newly created cells + blank line at the end
        file_list = ['Version 4\n', 'SHEET 1 3376 1172\n',
                     'WIRE 336 416 336 320\n', 'WIRE 336 416 -160 416\n', 'WIRE 448 416 336 416\n',
                     'WIRE 576 416 528 416\n', 'WIRE 976 416 576 416\n', 'WIRE 832 608 736 608\n',
                     'WIRE 928 608 928 80\n', 'WIRE 928 608 832 608\n', 'WIRE 576 624 576 416\n',
                     'WIRE 576 624 528 624\n', 'WIRE 624 624 576 624\n', 'WIRE 768 640 736 640\n',
                     'WIRE 928 640 928 608\n', 'WIRE 656 768 288 768\n', 'WIRE 928 768 928 720\n',
                     'WIRE 928 768 720 768\n', 'WIRE 1296 768 928 768\n', 'WIRE 928 1184 928 768\n',
                     'WIRE 928 1200 928 1184\n', 'WIRE 928 1248 928 1216\n',  'WIRE 976 1248 928 1248\n', 'WIRE 880 1280 784 1280\n',
                     'WIRE 928 1280 928 1248\n', 'WIRE 928 1312 928 1296\n', 'WIRE 976 1312 976 1248\n',
                     'WIRE 976 1312 928 1312\n', 'WIRE 928 1360 928 1312\n',
                     'FLAG 768 640 S14\n', 'FLAG 832 544 0\n', 'FLAG 464 624 0\n',
                     'FLAG 336 480 0\n', 'FLAG 928 1360 0\n', 'FLAG 784 1360 0\n', 'FLAG 928 1184 O1\n',
                     'SYMBOL res 544 400 R90\n', 'WINDOW 0 0 56 VBottom 2\n',
                     'WINDOW 3 32 56 VTop 2\n', 'SYMATTR InstName R4\n', 'SYMATTR Value ' + str(line_res) + '\n',
                     'SYMBOL res 944 736 R180\n', 'WINDOW 0 36 76 Left 2\n', 'WINDOW 3 36 40 Left 2\n',
                     'SYMATTR InstName R4\n', 'SYMATTR Value ' + str(line_res) + '\n', 'SYMBOL cap 528 608 R90\n',
                     'WINDOW 0 0 32 VBottom 2\n', 'WINDOW 3 32 32 VTop 2\n', 'SYMATTR InstName C4\n',
                     'SYMATTR Value ' + str(gnd_cap) + '\n', 'SYMBOL cap 848 608 R180\n', 'WINDOW 0 24 56 Left 2\n',
                     'WINDOW 3 24 8 Left 2\n', 'SYMATTR InstName C4\n', 'SYMATTR Value ' + str(gnd_cap) + '\n',
                     'SYMBOL cap 656 752 M90\n', 'WINDOW 0 0 32 VBottom 2\n', 'WINDOW 3 32 32 VTop 2\n',
                     'SYMATTR InstName C8\n', 'SYMATTR Value ' + str(line_cap) + '\n', 'SYMBOL cap 320 416 R0\n',
                     'SYMATTR InstName C35\n', 'SYMATTR Value ' + str(gnd_cap) + '\n',
                     'SYMBOL ' + name + ' 672 624 R0\n', 'SYMATTR InstName M5\n',
                     'SYMBOL nmos4 880 1200 R0\n', 'SYMATTR InstName L1\n', 'SYMBOL voltage 784 1264 R0\n',
                     'WINDOW 123 0 0 Left 0\n', 'WINDOW 39 0 0 Left 0\n', 'SYMATTR InstName VL1\n',
                     'SYMATTR Value PWL file=nmos.txt\n', ]

        for line in file_list :
            writer.write(line)

    writer.close()


# Capacitance template (bottomright)
def bottomright_capacitance():

    # get memristor model
    name = get_model()

    # Schematic filename
    filename_asc = 'bottomright_capacitance.asc'

    with open(filename_asc, 'w') as writer :
        # write into new file, original + newly created cells + blank line at the end
        file_list = ['Version 4\n', 'SHEET 1 3376 1172\n', 'WIRE 1616 416 1616 320\n',
                     'WIRE 1616 416 1616 320\n', 'WIRE 1616 416 1120 416\n', 'WIRE 1744 416 1616 416\n',
                     'WIRE 2320 416 1872 416\n', 'WIRE 2112 608 2016 608\n', 'WIRE 2128 608 2112 608\n',
                     'WIRE 2208 608 2208 368\n', 'WIRE 1872 624 1872 416\n', 'WIRE 1872 624 1808 624\n',
                     'WIRE 1904 624 1872 624\n', 'WIRE 2048 640 2016 640\n', 'WIRE 1936 768 1360 768\n',
                     'WIRE 2208 768 2208 608\n', 'WIRE 2208 1262 2208 768\n', 'WIRE 1872 416 1824 416\n',
                     'WIRE 2208 768 2000 768\n', 'WIRE 2208 1168 2208 768\n', 'WIRE 2256 1216 2208 1216\n',
                     'WIRE 2160 1248 2080 1248\n', 'WIRE 2080 1264 2080 1248\n', 'WIRE 2208 1280 2208 1264\n',
                     'WIRE 2256 1280 2256 1216\n', 'WIRE 2256 1280 2208 1280\n', 'WIRE 2208 1346 2208 1280\n',
                     'FLAG 2048 640 S16\n', 'FLAG 2208 1136 O1\n',
                     'FLAG 2112 544 0\n', 'FLAG 1744 624 0\n', 'FLAG 2080 1344 0\n',
                     'FLAG 1616 480 0\n', 'FLAG 2272 768 0\n', 'FLAG 2208 1346 0\n',
                     'SYMBOL res 1840 400 R90\n', 'WINDOW 0 0 56 VBottom 2\n', 'WINDOW 3 32 56 VTop 2\n',
                     'SYMATTR InstName R23\n', 'SYMATTR Value ' + str(line_res) +  '\n', 'SYMBOL res 2224 592 R90\n',
                     'WINDOW 0 0 56 VBottom 2\n', 'WINDOW 3 32 56 VTop 2\n', 'SYMATTR InstName R24\n',
                     'SYMATTR Value ' + str(line_res) + '\n', 'SYMBOL cap 1808 608 R90\n', 'WINDOW 0 0 32 VBottom 2\n',
                     'WINDOW 3 32 32 VTop 2\n', 'SYMATTR InstName C22\n', 'SYMATTR Value ' + str(gnd_cap) + '\n',
                     'SYMBOL cap 2128 608 R180\n', 'WINDOW 0 24 56 Left 2\n', 'WINDOW 3 24 8 Left 2\n',
                     'SYMATTR InstName C24\n', 'SYMATTR Value ' + str(gnd_cap) + '\n', 'SYMBOL cap 1936 752 M90\n',
                     'WINDOW 0 0 32 VBottom 2\n', 'WINDOW 3 32 32 VTop 2\n', 'SYMATTR InstName C1\n',
                     'SYMATTR Value ' + str(line_cap) + '\n', 'SYMBOL cap 1600 416 R0\n', 'SYMATTR InstName C33\n',
                     'SYMATTR Value ' + str(gnd_cap) + '\n', 'SYMBOL cap 2272 752 R90\n', 'WINDOW 0 0 32 VBottom 2\n',
                     'WINDOW 3 32 32 VTop 2\n', 'SYMATTR InstName C43\n', 'SYMATTR Value ' + str(gnd_cap) + '\n',
                     'SYMBOL ' + name + ' 1952 624 R0\n', 'SYMATTR InstName M7\n', 'SYMBOL nmos4 2160 1168 R0\n',
                     'SYMATTR InstName L1\n', 'SYMBOL voltage 2080 1248 R0\n', 'WINDOW 123 0 0 Left 0\n',
                     'WINDOW 39 0 0 Left 0\n', 'SYMATTR InstName VL1\n', 'SYMATTR Value PWL file=nmos.txt\n', ]

        for line in file_list :
            writer.write(line)

    writer.close()


# Create crossbar array schematic (Line Resistance & Parasitic Capacitance)
def create_crossbar_capacitance(z):

    if z == 1:
        create_single_capacitance(z)

    elif z == 2:
        # Create schematic template to duplicate
        topleft_capacitance()
        topright_capacitance()
        bottomleft_capacitance()
        bottomright_capacitance()

        # Schematic template to modify and duplicate (Top Left)
        template_name = 'topleft_capacitance.asc'
        with open(template_name, "r") as reader:
            start_list = reader.readlines()

        # Schematic template to modify and duplicate (Top Right)
        template_name = 'topright_capacitance.asc'
        with open(template_name, "r") as reader:
            topright_template_list = reader.readlines()

        # delete the first 3 lines which is the asc version, sheet size and simulation time
        del topright_template_list[0]
        del topright_template_list[0]
        del topright_template_list[0]

        # Top Right memristor
        for lines in topright_template_list:
            current = lines.split()

            if current[0] == 'WIRE':
                for n in [1, 3]:
                    current[n] = str(int(current[n]) - 1132)
            elif current[0] == 'FLAG':
                current[1] = str(int(current[1]) - 1132)
            elif current[0] == 'SYMBOL':
                current[2] = str(int(current[2]) - 1132)
            # join the text together back into a line and put into the array to be appended
            try:
                current = " ".join(current) + "\n"
                topright_template_list[topright_template_list.index(lines)] = current
            except:
                pass

        start_list.extend(topright_template_list)

        # Schematic template to modify and duplicate (Bottom Left)
        template_name = 'bottomleft_capacitance.asc'
        with open(template_name, "r") as reader:
            bottomleft_template_list = reader.readlines()

        # delete the first 3 lines which is the asc version, sheet size and simulation time
        del bottomleft_template_list[0]
        del bottomleft_template_list[0]
        del bottomleft_template_list[0]

        # Bottom left memristor
        for lines in bottomleft_template_list:
            current = lines.split()
            if current[0] == 'WIRE':
                for n in [2, 4]:
                    current[n] = str(int(current[n]) - 896)
            elif current[0] == 'FLAG':
                current[2] = str(int(current[2]) - 896)
            elif current[0] == 'SYMBOL':
                current[3] = str(int(current[3]) - 896)
            # join the text together back into a line and put into the array to be appended
            try:
                current = " ".join(current) + "\n"
                bottomleft_template_list[bottomleft_template_list.index(lines)] = current
            except:
                pass

        start_list.extend(bottomleft_template_list)

        # Schematic template to modify and duplicate (Bottom Right)
        template_name = 'bottomright_capacitance.asc'
        with open(template_name, "r") as reader:
            bottomright_template_list = reader.readlines()

        # delete the first 3 lines which is the asc version, sheet size and simulation time
        del bottomright_template_list[0]
        del bottomright_template_list[0]
        del bottomright_template_list[0]

        # Bottom right memristor
        for lines in bottomright_template_list:
            current = lines.split()
            if current[0] == 'WIRE':
                for n in [1, 3] :
                    current[n] = str(int(current[n]) - 1132)
                for n in [2, 4]:
                    current[n] = str(int(current[n]) - 896)
            elif current[0] == 'FLAG':
                current[1] = str(int(current[1]) - 1132)
                current[2] = str(int(current[2]) - 896)
            elif current[0] == 'SYMBOL':
                current[2] = str(int(current[2]) - 1132)
                current[3] = str(int(current[3]) - 896)
            # join the text together back into a line and put into the array to be appended
            try:
                current = " ".join(current) + "\n"
                bottomright_template_list[bottomright_template_list.index(lines)] = current
            except:
                pass

        start_list.extend(bottomright_template_list)

        # Rename component labeling that incrementally increases as new components are generated
        s = 1
        m = 1
        r = 1
        vr = 1
        L = 1
        c = 1
        vl = 1
        o = 1
        line_num = 0

        for line in start_list:
            current = line.split()
            if current[0] == 'FLAG':
                cellName = current[3]
                if cellName[0] == 'S':
                    current[3] = cellName[0] + str(s)
                    current = " ".join(current) + "\n"
                    start_list[line_num] = current
                    s = s + 1
                elif cellName[0] == 'O':
                    current[3] = cellName[0] + str(s)
                    current = " ".join(current) + "\n"
                    start_list[line_num] = current
                    o = o + 1

            elif current[0] == 'SYMATTR' and current[1] == 'InstName':
                cellName = current[2]
                if cellName[0] == 'M':
                    current[2] = cellName[0] + str(m)
                    m = m + 1
                elif cellName[0] == 'L':
                    current[2] = cellName[0] + str(L)
                    L = L + 1
                elif cellName[0] == 'R':
                    current[2] = cellName[0] + str(r)
                    r = r + 1
                elif cellName[1] == 'R':
                    current[2] = cellName[0] + cellName[1] + str(vr)
                    vr = vr + 1
                elif cellName[1] == 'L':
                    current[2] = cellName[0] + cellName[1] + str(vl)
                    vl = vl + 1
                elif cellName[0] == 'C':
                    current[2] = cellName[0] + str(c)
                    c = c + 1

                current = " ".join(current) + "\n"
                start_list[line_num] = current

            line_num = line_num + 1

        filename_final = str(z) + "x" + str(z) + "_capacitance.asc"
        with open(filename_final, 'w') as writer:
            # write into new file, original + newly created cells + blank line at the end
            for line in start_list:
                writer.write(line)

            writer.close()

    else:
        # Create schematic template to duplicate
        topleft_capacitance()
        top_capacitance()
        topright_capacitance()
        left_capacitance()
        middle_capacitance()
        right_capacitance()
        bottomleft_capacitance()
        bottom_capacitance()
        bottomright_capacitance()

        # Schematic template to modify and duplicate (Top Left)
        template_name = 'topleft_capacitance.asc'
        with open(template_name, "r") as reader:
            start_list = reader.readlines()

        # Schematic template to modify and duplicate (Top Left)
        template_name = 'top_capacitance.asc'
        with open(template_name, "r") as reader:
            top_template_list = reader.readlines()

        # delete the first 3 lines which is the asc version, sheet size and simulation time
        del top_template_list[0]
        del top_template_list[0]

        start_list.extend(top_template_list)

        for y in range(z-3):

            # Top memristor
            for lines in top_template_list:
                current = lines.split()

                if current[0] == 'WIRE':
                    for n in [1, 3]:
                        current[n] = str(int(current[n]) + 646 )
                elif current[0] == 'FLAG':
                    current[1] = str(int(current[1]) + 646)
                elif current[0] == 'SYMBOL':
                    current[2] = str(int(current[2]) + 646)
                # join the text together back into a line and put into the array to be appended
                try:
                    current = " ".join(current) + "\n"
                    top_template_list[top_template_list.index(lines)] = current
                except:
                    pass

            start_list.extend(top_template_list)

        # Schematic template to modify and duplicate (Top Right)
        template_name = 'topright_capacitance.asc'
        with open(template_name, "r") as reader:
            topright_template_list = reader.readlines()

        # delete the first 3 lines which is the asc version, sheet size and simulation time
        del topright_template_list[0]
        del topright_template_list[0]

        if z == 4:
            start_list.extend(topright_template_list)

        elif z > 4:
            # Top Right memristor
            for lines in topright_template_list:
                current = lines.split()

                if current[0] == 'WIRE':
                    for n in [1, 3]:
                        current[n] = str(int(current[n]) + 646 * (z-4))
                elif current[0] == 'FLAG':
                    current[1] = str(int(current[1]) + 646 * (z-4))
                elif current[0] == 'SYMBOL':
                    current[2] = str(int(current[2]) + 646 * (z-4))
                # join the text together back into a line and put into the array to be appended
                try:
                    current = " ".join(current) + "\n"
                    topright_template_list[topright_template_list.index(lines)] = current
                except:
                    pass

            start_list.extend(topright_template_list)

        # Schematic template to modify and duplicate (Left)
        template_name = 'left_capacitance.asc'
        with open(template_name, "r") as reader:
            left_template_list = reader.readlines()

        # delete the first 3 lines which is the asc version, sheet size and simulation time
        del left_template_list[0]
        del left_template_list[0]

        start_list.extend(left_template_list)

        # Schematic template to modify and duplicate (Middle)
        template_name = 'middle_capacitance.asc'
        with open(template_name, "r") as reader:
            middle_template_list = reader.readlines()

        # delete the first 3 lines which is the asc version, sheet size and simulation time
        del middle_template_list[0]
        del middle_template_list[0]

        middle_copy = list(middle_template_list)

        start_list.extend(middle_template_list)

        for y in range(z-3):

            # Middle memristor
            for lines in middle_copy:
                current = lines.split()

                if current[0] == 'WIRE':
                    for n in [1, 3]:
                        current[n] = str(int(current[n]) + 646)
                elif current[0] == 'FLAG':
                    current[1] = str(int(current[1]) + 646)
                elif current[0] == 'SYMBOL':
                    current[2] = str(int(current[2]) + 646)
                # join the text together back into a line and put into the array to be appended
                try:
                    current = " ".join(current) + "\n"
                    middle_copy[middle_copy.index(lines)] = current
                except:
                    pass

            start_list.extend(middle_copy)

        # Schematic template to modify and duplicate (Right)
        template_name = 'right_capacitance.asc'
        with open(template_name, "r") as reader:
            right_template_list = reader.readlines()

        # delete the first 3 lines which is the asc version, sheet size and simulation time
        del right_template_list[0]
        del right_template_list[0]

        if z == 4:
            start_list.extend(right_template_list)

        elif z > 4:
            # Right memristor
            for lines in right_template_list:
                current = lines.split()

                if current[0] == 'WIRE':
                    for n in [1, 3]:
                        current[n] = str(int(current[n]) + 646 * (z-4))
                elif current[0] == 'FLAG':
                    current[1] = str(int(current[1]) + 646 * (z-4))
                elif current[0] == 'SYMBOL':
                    current[2] = str(int(current[2]) + 646 * (z-4))
                # join the text together back into a line and put into the array to be appended
                try:
                    current = " ".join(current) + "\n"
                    right_template_list[right_template_list.index(lines)] = current
                except:
                    pass

            start_list.extend(right_template_list)

        # Other row
        for y in range(z-3):

            # Left memristor
            for lines in left_template_list:
                current = lines.split()
                if current[0] == 'WIRE':
                    for n in [2, 4]:
                        current[n] = str(int(current[n]) + 448)
                elif current[0] == 'FLAG':
                    current[2] = str(int(current[2]) + 448)
                elif current[0] == 'SYMBOL':
                    current[3] = str(int(current[3]) + 448)
                # join the text together back into a line and put into the array to be appended
                try:
                    current = " ".join(current) + "\n"
                    left_template_list[left_template_list.index(lines)] = current
                except:
                    pass

            start_list.extend(left_template_list)

            # Middle memristor
            for lines in middle_template_list:
                current = lines.split()
                if current[0] == 'WIRE':
                    for n in [2, 4]:
                        current[n] = str(int(current[n]) + 448)
                elif current[0] == 'FLAG':
                    current[2] = str(int(current[2]) + 448)
                elif current[0] == 'SYMBOL':
                    current[3] = str(int(current[3]) + 448)
                # join the text together back into a line and put into the array to be appended
                try:
                    current = " ".join(current) + "\n"
                    middle_template_list[middle_template_list.index(lines)] = current
                except:
                    pass

            start_list.extend(middle_template_list)
            middle_copy = list(middle_template_list)

            for y in range(z - 3) :

                # Middle memristor
                for lines in middle_copy :
                    current = lines.split()

                    if current[0] == 'WIRE' :
                        for n in [1, 3] :
                            current[n] = str(int(current[n]) + 646)
                    elif current[0] == 'FLAG' :
                        current[1] = str(int(current[1]) + 646)
                    elif current[0] == 'SYMBOL' :
                        current[2] = str(int(current[2]) + 646)
                    # join the text together back into a line and put into the array to be appended
                    try :
                        current = " ".join(current) + "\n"
                        middle_copy[middle_copy.index(lines)] = current
                    except :
                        pass

                start_list.extend(middle_copy)

            # Right memristor
            for lines in right_template_list :
                current = lines.split()
                if current[0] == 'WIRE' :
                    for n in [2, 4] :
                        current[n] = str(int(current[n]) + 448)
                elif current[0] == 'FLAG' :
                    current[2] = str(int(current[2]) + 448)
                elif current[0] == 'SYMBOL' :
                    current[3] = str(int(current[3]) + 448)
                # join the text together back into a line and put into the array to be appended
                try :
                    current = " ".join(current) + "\n"
                    right_template_list[right_template_list.index(lines)] = current
                except :
                    pass

            start_list.extend(right_template_list)

        # Schematic template to modify and duplicate (Bottom Left)
        template_name = 'bottomleft_capacitance.asc'
        with open(template_name, "r") as reader:
            bottomleft_template_list = reader.readlines()

        # delete the first 3 lines which is the asc version, sheet size and simulation time
        del bottomleft_template_list[0]
        del bottomleft_template_list[0]

        # Bottom Left memristor
        for lines in bottomleft_template_list:
            current = lines.split()
            if current[0] == 'WIRE':
                for n in [2, 4]:
                    current[n] = str(int(current[n]) + 448 * (z - 4))
            elif current[0] == 'FLAG':
                current[2] = str(int(current[2]) + 448 * (z - 4))
            elif current[0] == 'SYMBOL':
                current[3] = str(int(current[3]) + 448 * (z - 4))
            # join the text together back into a line and put into the array to be appended
            try:
                current = " ".join(current) + "\n"
                bottomleft_template_list[bottomleft_template_list.index(lines)] = current
            except:
                pass

        start_list.extend(bottomleft_template_list)

        # Schematic template to modify and duplicate (Bottom)
        template_name = 'bottom_capacitance.asc'
        with open(template_name, "r") as reader:
            bottom_template_list = reader.readlines()

        # delete the first 3 lines which is the asc version, sheet size and simulation time
        del bottom_template_list[0]
        del bottom_template_list[0]

        # Bottom memristor
        for lines in bottom_template_list:
            current = lines.split()
            if current[0] == 'WIRE':
                for n in [2, 4]:
                    current[n] = str(int(current[n]) + 448 * (z - 4))
            elif current[0] == 'FLAG':
                current[2] = str(int(current[2]) + 448 * (z - 4))
            elif current[0] == 'SYMBOL':
                current[3] = str(int(current[3]) + 448 * (z - 4))
            # join the text together back into a line and put into the array to be appended
            try:
                current = " ".join(current) + "\n"
                bottom_template_list[bottom_template_list.index(lines)] = current
            except:
                pass

        start_list.extend(bottom_template_list)

        for y in range(z-3):

            # Top Right memristor
            for lines in bottom_template_list:
                current = lines.split()

                if current[0] == 'WIRE':
                    for n in [1, 3]:
                        current[n] = str(int(current[n]) + 646 )
                elif current[0] == 'FLAG':
                    current[1] = str(int(current[1]) + 646)
                elif current[0] == 'SYMBOL':
                    current[2] = str(int(current[2]) + 646)
                # join the text together back into a line and put into the array to be appended
                try:
                    current = " ".join(current) + "\n"
                    bottom_template_list[bottom_template_list.index(lines)] = current
                except:
                    pass

            start_list.extend(bottom_template_list)

       # Schematic template to modify and duplicate (Bottom Right)
        template_name = 'bottomright_capacitance.asc'
        with open(template_name, "r") as reader:
            bottomright_template_list = reader.readlines()

        # Bottom Right memristor
        for lines in bottomright_template_list:
            current = lines.split()
            if current[0] == 'WIRE':
                for n in [2, 4]:
                    current[n] = str(int(current[n]) + 448 * (z - 4))
                for n in [1, 3] :
                    current[n] = str(int(current[n]) + 646 * (z - 4))
            elif current[0] == 'FLAG':
                current[1] = str(int(current[1]) + 646 * (z - 4))
                current[2] = str(int(current[2]) + 448 * (z - 4))
            elif current[0] == 'SYMBOL':
                current[2] = str(int(current[2]) + 646 * (z - 4))
                current[3] = str(int(current[3]) + 448 * (z - 4))
            # join the text together back into a line and put into the array to be appended
            try:
                current = " ".join(current) + "\n"
                bottomright_template_list[bottomright_template_list.index(lines)] = current
            except:
                pass

        start_list.extend(bottomright_template_list)

        # Component name variable that incrementally increases as new components are generated
        s = 1
        m = 1
        r = 1
        vr = 1
        L = 1
        c = 1
        vl = 0
        o = 1
        line_num = 0

        for line in start_list:
            current = line.split()
            if current[0] == 'FLAG':
                cellName = current[3]
                if cellName[0] == 'S':
                    current[3] = cellName[0] + str(s)
                    current = " ".join(current) + "\n"
                    start_list[line_num] = current
                    s = s + 1
                elif cellName[0] == 'O':
                    current[3] = cellName[0] + str(o)
                    current = " ".join(current) + "\n"
                    start_list[line_num] = current
                    o = o + 1

            elif current[0] == 'SYMATTR' and current[1] == 'InstName':
                cellName = current[2]
                if cellName[0] == 'M':
                    current[2] = cellName[0] + str(m)
                    m = m + 1
                elif cellName[0] == 'L':
                    current[2] = cellName[0] + str(L)
                    L = L + 1
                elif cellName[0] == 'R':
                    current[2] = cellName[0] + str(r)
                    r = r + 1
                elif cellName[1] == 'R':
                    current[2] = cellName[0] + cellName[1] + str(vr)
                    vr = vr + 1
                elif cellName[1] == 'L':
                    current[2] = cellName[0] + cellName[1] + str(vl)
                    vl = vl + 1
                elif cellName[0] == 'C':
                    current[2] = cellName[0] + str(c)
                    c = c + 1

                current = " ".join(current) + "\n"
                start_list[line_num] = current

            line_num = line_num + 1

        filename_final = str(z) + "x" + str(z) + "_capacitance.asc"
        with open(filename_final, 'w') as writer:
            # write into new file, original + newly created cells + blank line at the end
            for line in start_list:
                writer.write(line)

            writer.close()

# Generate text boxes according to selected conditions
def generate_textboxes():
    global size_combobox, input_signal_value, line_resistance_value, ground_capacitance_value, line_capacitance_value

    # Get the selected radiobutton value
    startup_value = startup_var.get()
    condition_value = condition_var.get()

    # Clear any existing textboxes and combobox
    for widget in textboxes_frame.winfo_children() :
        widget.destroy()

    if size_combobox:
        size_combobox.destroy()
        size_combobox = None

    # Startup options are custom or default
    if startup_value == 1:
        # Set the default simulation parameters
        # Input Voltage Source Parameters (PWL)
        input_signal_value.set("pwl_selected.txt")
        # Line Resistance
        line_resistance_value.set("18.22u")
        # Ground Capacitance
        ground_capacitance_value.set("2.012e-18")
        # Parallel Capacitance
        line_capacitance_value.set("1.6e-18")
        # Simulation Run Time
        simulation_time_value.set("200m")

        # Generate new textboxes based on the selected radiobutton value
        if condition_value == 1:
            tk.Label(textboxes_frame, text="Input voltage signal : ").grid(row=1, column=0)
            input_signal_entry = tk.Entry(textboxes_frame, textvariable=input_signal_value)
            input_signal_entry.grid(row=1, column=1)
            browse_button = tk.Button(textboxes_frame, text="Browse", command=browse_file)
            browse_button.grid(row=1, column=2)
            tk.Label(textboxes_frame, text="Simulation Run Time : ").grid(row=2, column=0)
            simulation_time_entry = tk.Entry(textboxes_frame, textvariable=simulation_time_value)
            simulation_time_entry.grid(row=2, column=1)
            tk.Label(textboxes_frame, text="Select array size : ").grid(row=3, column=0)

            # ComboBox (Drop down menu options to select size)
            # Create a ComboBox with string options
            size_combobox = ttk.Combobox(textboxes_frame, values=size_options)
            size_combobox.grid(row=3, column=1)
            # Set the initial value of the ComboBox
            size_combobox.current(0)

        elif condition_value == 2:
            tk.Label(textboxes_frame, text="Input voltage signal : ").grid(row=1, column=0)
            input_signal_entry = tk.Entry(textboxes_frame, textvariable=input_signal_value)
            input_signal_entry.grid(row=1, column=1)
            browse_button = tk.Button(textboxes_frame, text="Browse", command=browse_file)
            browse_button.grid(row=1, column=2)
            tk.Label(textboxes_frame, text="Line Resistance value : ").grid(row=2, column=0)
            line_resistance_entry = tk.Entry(textboxes_frame, textvariable=line_resistance_value)
            line_resistance_entry.grid(row=2, column=1)
            tk.Label(textboxes_frame, text="Simulation Run Time : ").grid(row=3, column=0)
            simulation_time_entry = tk.Entry(textboxes_frame, textvariable=simulation_time_value)
            simulation_time_entry.grid(row=3, column=1)
            tk.Label(textboxes_frame, text="Select array size : ").grid(row=4, column=0)

            # ComboBox (Drop down menu options to select size)
            # Create a ComboBox with string options
            size_combobox = ttk.Combobox(textboxes_frame, values=size_options)
            size_combobox.grid(row=4, column=1)
            # Set the initial value of the ComboBox
            size_combobox.current(0)

        elif condition_value == 3:
            tk.Label(textboxes_frame, text="Input voltage signal : ").grid(row=1, column=0)
            input_signal_entry = tk.Entry(textboxes_frame, textvariable=input_signal_value)
            input_signal_entry.grid(row=1, column=1)
            browse_button = tk.Button(textboxes_frame, text="Browse", command=browse_file)
            browse_button.grid(row=1, column=2)
            tk.Label(textboxes_frame, text="Line Resistance value : ").grid(row=2, column=0)
            line_resistance_entry = tk.Entry(textboxes_frame, textvariable=line_resistance_value)
            line_resistance_entry.grid(row=2, column=1)
            tk.Label(textboxes_frame, text="Ground Capacitance value : ").grid(row=3, column=0)
            parasitic_capacitance_entry = tk.Entry(textboxes_frame, textvariable=ground_capacitance_value)
            parasitic_capacitance_entry.grid(row=3, column=1)
            tk.Label(textboxes_frame, text="Line Capacitance value : ").grid(row=4, column=0)
            line_capacitance_entry = tk.Entry(textboxes_frame, textvariable=line_capacitance_value)
            line_capacitance_entry.grid(row=4, column=1)
            tk.Label(textboxes_frame, text="Simulation Run Time : ").grid(row=5, column=0)
            simulation_time_entry = tk.Entry(textboxes_frame, textvariable=simulation_time_value)
            simulation_time_entry.grid(row=5, column=1)
            tk.Label(textboxes_frame, text="Select array size : ").grid(row=6, column=0)

            # ComboBox (Drop down menu options to select size)
            # Create a ComboBox with string options
            size_combobox = ttk.Combobox(textboxes_frame, values=size_options)
            size_combobox.grid(row=6, column=1)
            # Set the initial value of the ComboBox
            size_combobox.current(0)

    elif startup_value == 2:

        # Clear the default simulation parameters
        # Input Voltage Source Parameters (PWL)
        input_signal_value.set("")
        # Line Resistance
        line_resistance_value.set("")
        # Ground Capacitance
        ground_capacitance_value.set("")
        # Parallel Capacitance
        line_capacitance_value.set("")
        # Simulation Run Time
        simulation_time_value.set("")

        # Generate new textboxes based on the selected radiobutton value
        if condition_value == 1:
            tk.Label(textboxes_frame, text="Input voltage signal (txt) : ").grid(row=1, column=0)
            input_signal_entry = tk.Entry(textboxes_frame, textvariable=input_signal_value)
            input_signal_entry.grid(row=1, column=1)
            browse_button = tk.Button(textboxes_frame, text="Browse", command=browse_file)
            browse_button.grid(row=1, column=2)
            tk.Label(textboxes_frame, text="Simulation Run Time : ").grid(row=2, column=0)
            simulation_time_entry = tk.Entry(textboxes_frame, textvariable=simulation_time_value)
            simulation_time_entry.grid(row=2, column=1)
            tk.Label(textboxes_frame, text="Write file (Excel) : ").grid(row=3, column=0)
            write_entry = tk.Entry(textboxes_frame, textvariable=write_value)
            write_entry.grid(row=3, column=1)
            browse_button = tk.Button(textboxes_frame, text="Browse", command=browse_excel_file)
            browse_button.grid(row=3, column=2)
            tk.Label(textboxes_frame, text="Select array size : ").grid(row=4, column=0)
            # ComboBox (Drop down menu options to select size)
            # Create a ComboBox with string options
            size_combobox = ttk.Combobox(textboxes_frame, values=size_options)
            size_combobox.grid(row=4, column=1)
            # Set the initial value of the ComboBox
            size_combobox.current(0)

        elif condition_value == 2:
            tk.Label(textboxes_frame, text="Input voltage signal : ").grid(row=1, column=0)
            input_signal_entry = tk.Entry(textboxes_frame, textvariable=input_signal_value)
            input_signal_entry.grid(row=1, column=1)
            browse_button = tk.Button(textboxes_frame, text="Browse", command=browse_file)
            browse_button.grid(row=1, column=2)
            tk.Label(textboxes_frame, text="Line Resistance value : ").grid(row=2, column=0)
            line_resistance_entry = tk.Entry(textboxes_frame, textvariable=line_resistance_value)
            line_resistance_entry.grid(row=2, column=1)
            tk.Label(textboxes_frame, text="Simulation Run Time : ").grid(row=3, column=0)
            simulation_time_entry = tk.Entry(textboxes_frame, textvariable=simulation_time_value)
            simulation_time_entry.grid(row=3, column=1)
            tk.Label(textboxes_frame, text="Write file (Excel) : ").grid(row=4, column=0)
            write_entry = tk.Entry(textboxes_frame, textvariable=write_value)
            write_entry.grid(row=4, column=1)
            browse_button = tk.Button(textboxes_frame, text="Browse", command=browse_excel_file)
            browse_button.grid(row=4, column=2)
            tk.Label(textboxes_frame, text="Select array size : ").grid(row=5, column=0)

            # ComboBox (Drop down menu options to select size)
            # Create a ComboBox with string options
            size_combobox = ttk.Combobox(textboxes_frame, values=size_options)
            size_combobox.grid(row=5, column=1)
            # Set the initial value of the ComboBox
            size_combobox.current(0)

        elif condition_value == 3:
            tk.Label(textboxes_frame, text="Input voltage signal : ").grid(row=1, column=0)
            input_signal_entry = tk.Entry(textboxes_frame, textvariable=input_signal_value)
            input_signal_entry.grid(row=1, column=1)
            browse_button = tk.Button(textboxes_frame, text="Browse", command=browse_file)
            browse_button.grid(row=1, column=2)
            tk.Label(textboxes_frame, text="Line Resistance value : ").grid(row=2, column=0)
            line_resistance_entry = tk.Entry(textboxes_frame, textvariable=line_resistance_value)
            line_resistance_entry.grid(row=2, column=1)
            tk.Label(textboxes_frame, text="Ground Capacitance value : ").grid(row=3, column=0)
            parasitic_capacitance_entry = tk.Entry(textboxes_frame, textvariable=ground_capacitance_value)
            parasitic_capacitance_entry.grid(row=3, column=1)
            tk.Label(textboxes_frame, text="Line Capacitance value : ").grid(row=4, column=0)
            line_capacitance_entry = tk.Entry(textboxes_frame, textvariable=line_capacitance_value)
            line_capacitance_entry.grid(row=4, column=1)
            tk.Label(textboxes_frame, text="Simulation Run Time : ").grid(row=5, column=0)
            simulation_time_entry = tk.Entry(textboxes_frame, textvariable=simulation_time_value)
            simulation_time_entry.grid(row=5, column=1)
            tk.Label(textboxes_frame, text="Write file (Excel) : ").grid(row=6, column=0)
            write_entry = tk.Entry(textboxes_frame, textvariable=write_value)
            write_entry.grid(row=6, column=1)
            browse_button = tk.Button(textboxes_frame, text="Browse", command=browse_excel_file)
            browse_button.grid(row=6, column=2)
            tk.Label(textboxes_frame, text="Select array size : ").grid(row=7, column=0)

            # ComboBox (Drop down menu options to select size)
            # Create a ComboBox with string options
            size_combobox = ttk.Combobox(textboxes_frame, values=size_options)
            size_combobox.grid(row=7, column=1)
            # Set the initial value of the ComboBox
            size_combobox.current(0)


# Retrieve selected value of combobox
def get_size():
    global size

    # Get the selected option as a string
    selected_option = size_combobox.get()
    # Convert the selected option to an integer index
    selected_size = pow(2, size_options.index(selected_option))

    # print(f"Selected size: {selected_size} x {selected_size}")

    size = selected_size


# Retrieve input values from textboxes
def get_textbox_values():
    global size_combobox, input_signal_value, line_resistance_value, ground_capacitance_value, line_capacitance_value, simulation_time_value
    global gnd_cap, line_cap, simulation_time, line_res, input_signal
    # Get the values from the textboxes
    line_res = line_resistance_value.get()
    # print('res=', line_res)
    input_signal = input_signal_value.get()
    print('volt=', input_signal)
    gnd_cap = ground_capacitance_value.get()
    # print('gndcap=', gnd_cap)
    line_cap = line_capacitance_value.get()
    # print('linecap=', line_cap)
    simulation_time = simulation_time_value.get()
    # print('runtime=', simulation_time)


# Function to browse for a file to be used as voltage input
def browse_file():
    # filedialog to open a file and get its path
    file_path = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(("Text files", "*.txt"),))

    if file_path:
        # Extract only the filename from the file path
        filename = os.path.basename(file_path)
        # Set the value of input_signal_value to the selected file path
        input_signal_value.set(filename)

    else:
        messagebox.showerror(title="Error", message="No file selected.")


# Function to browse for an Excel file; read and save data from excel for writing operation
def browse_excel_file():
    # filedialog to open a file and get its path
    file_path = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(("Excel files", "*.xlsx"),))
    # Set the value of write_value to the selected file path
    write_value.set(file_path)
    # Reset data array
    del data[:]
    if file_path:
        # Read the Excel file and save the information using array
        wb = openpyxl.load_workbook(file_path)
        sheet = wb.active

        for row in sheet.iter_rows(values_only=True):
            data.append([int(str(cell)[0]) if isinstance(cell, (int, float)) else 0 for cell in row])

    else:
        messagebox.showerror(title="Error", message="No file selected.")


def create_output_window(data, s):

    global selected_column

    # Get Data Matrix
    # Create a new window to display the data
    output_window = tk.Toplevel(window)
    output_window.title("Output Window")
    output_window.geometry("300x300")

    # Add matrix label
    matrix_label = tk.Label(output_window, text="Memristor State:")
    matrix_label.place(x=12, y=10)

    # Calculate the size of the matrix
    num_rows = s
    num_cols = s

    # Get the selected radiobutton value
    startup_value = startup_var.get()

    if startup_value == 1:

        # Create a grid of text boxes to display the matrix
        for i in range(s) :
            for j in range(s):
                value = 0
                textbox = tk.Text(output_window, height=1, width=1)
                textbox.insert(tk.END, str(value))
                textbox.place(x=20 + j * 15, y=30 + i * 20)

        if s < 4:

            # Resize the window to fit the matrix
            output_window.update_idletasks()
            width = 260
            height = 120
            output_window.geometry("{}x{}".format(width, height))
            textbox.config(state="disabled")

            def update_selected_column(*args):
                global selected_column
                # Get the selected option as a string
                selected_option = column_combobox.get()
                # Convert the selected option to an integer index
                selected_column = int(selected_option.split()[-1])

            # Create a combobox to select columns
            column_options = [f"Column {i + 1}" for i in range(num_cols)]
            column_var = tk.StringVar(value='Column 1')
            column_label = tk.Label(output_window, text="Plot output graph:")
            column_label.place(x=135, y=10)
            column_combobox = ttk.Combobox(output_window, textvariable=column_var, values=column_options, width=10)
            column_combobox.place(x=140, y=30)
            column_combobox.bind("<<ComboboxSelected>>", update_selected_column)

            # Create a button to plot output of selected column
            plot_button = tk.Button(output_window, text="Plot Output", command=plot_output)
            plot_button.place(x=140, y=70)

        else:

            # Resize the window to fit the matrix
            output_window.update_idletasks()
            width = num_cols * 15 + 180
            height = num_rows * 20 + 50
            output_window.geometry("{}x{}".format(width, height))
            textbox.config(state="disabled")

            def update_selected_column(*args):
                global selected_column
                # Get the selected option as a string
                selected_option = column_combobox.get()
                # Convert the selected option to an integer index
                selected_column = int(selected_option.split()[-1])

            # Create a combobox to select columns
            column_options = [f"Column {i + 1}" for i in range(num_cols)]
            column_var = tk.StringVar(value='Column 1')
            column_label = tk.Label(output_window, text="Plot output graph:")
            column_label.place(x=75 + i * 15, y=10)
            column_combobox = ttk.Combobox(output_window, textvariable=column_var, values=column_options, width=10)
            column_combobox.place(x=80 + i * 15, y=30)
            column_combobox.bind("<<ComboboxSelected>>", update_selected_column)

            # Create a button to plot output of selected column
            plot_button = tk.Button(output_window, text="Plot Output", command=plot_output)
            plot_button.place(x=80 + i * 15, y=70)

    elif startup_value == 2:

        # Create a grid of text boxes to display the matrix
        for i in range(s):
            for j in range(s):
                value = data[i][j]
                textbox = tk.Text(output_window, height=1, width=2)
                textbox.insert(tk.END, str(value))
                textbox.place(x=20 + j * 15, y=30 + i * 20)

        if s < 4:
            # Resize the window to fit the matrix
            output_window.update_idletasks()
            width = 260
            height = 180
            output_window.geometry("{}x{}".format(width, height))
            textbox.config(state="disabled")

            def update_selected_column(*args):
                global selected_column
                # Get the selected option as a string
                selected_option = column_combobox.get()
                # Convert the selected option to an integer index
                selected_column = int(selected_option.split()[-1])

            # Create a combobox to select columns
            column_options = [f"Column {i + 1}" for i in range(num_cols)]
            column_var = tk.StringVar(value='Column 1')
            column_label = tk.Label(output_window, text="Plot output graph:")
            column_label.place(x=135, y=10)
            column_combobox = ttk.Combobox(output_window, textvariable=column_var, values=column_options, width=10)
            column_combobox.place(x=140, y=30)
            column_combobox.bind("<<ComboboxSelected>>", update_selected_column)

            # Create a button to plot output of selected column
            plot_button = tk.Button(output_window, text="Plot Output", command=plot_output)
            plot_button.place(x=140, y=70)

        else:

            # Resize the window to fit the matrix
            output_window.update_idletasks()
            width = num_cols * 15 + 180
            height = num_rows * 20 + 50
            output_window.geometry("{}x{}".format(width, height))
            textbox.config(state="disabled")

            def update_selected_column(*args):
                global selected_column
                # Get the selected option as a string
                selected_option = column_combobox.get()
                # Convert the selected option to an integer index
                selected_column = int(selected_option.split()[-1])

            # Create a combobox to select columns
            column_options = [f"Column {i + 1}" for i in range(num_cols)]
            column_var = tk.StringVar(value='Column 1')
            column_label = tk.Label(output_window, text="Plot output graph:")
            column_label.place(x=75 + i * 15, y=10)
            column_combobox = ttk.Combobox(output_window, textvariable=column_var, values=column_options, width=10)
            column_combobox.place(x=80 + i * 15, y=30)
            column_combobox.bind("<<ComboboxSelected>>", update_selected_column)

            # Create a button to plot output of selected column
            plot_button = tk.Button(output_window, text="Plot Output", command=plot_output)
            plot_button.place(x=80 + i * 15, y=70)


def plot_output():

    print("selected=", selected_column)
    t = condition()
    s = size

    if t == 1:
        filename = str(s) + 'x' + str(s) + '_ideal'

    elif t == 2:
        filename = str(s) + 'x' + str(s) + '_resistance'

    elif t == 3:
        filename = str(s) + 'x' + str(s) + '_capacitance'

    # Schematic filename
    filename_asc = filename + '.asc'

    lt_directory = "C:\Program Files\LTC\LTspiceXVII"

    subprocess.call(lt_directory + "\XVIIx64.exe -b -Run " + filename_asc)

    l = ltspice.Ltspice(os.path.dirname(__file__) + '\\' + filename + '.raw')
    print('os.path.dirname(__file__)=', os.path.dirname(__file__))

    l.parse()

    t = l.get_time()

    V = l.get_data('V(O' + str(selected_column) + ')')

    plt.plot(t, V)
    plt.xlabel('Time (s)')
    plt.ylabel('Voltage (V)')
    plt.show()


# Create radiobutton group to choose memristor model
model_var = IntVar()
label2 = tk.Label(text="Select a memristor model:")
rm1 = Radiobutton(window, text="HP", variable=model_var, value=1)
rm2 = Radiobutton(window, text="Yakopcic", variable=model_var, value=2)
rm3 = Radiobutton(window, text="Biolek", variable=model_var, value=3)
rm4 = Radiobutton(window, text="UMICH", variable=model_var, value=4)
rm5 = Radiobutton(window, text="Knowm", variable=model_var, value=5)
label2.place(x=30, y=0)
rm1.place(x=30, y=20)
rm2.place(x=30, y=40)
rm3.place(x=30, y=60)
rm4.place(x=30, y=80)
rm5.place(x=30, y=100)


# Create radiobutton group to choose condition
condition_var = IntVar()
label3 = tk.Label(text="Select condition:")
rt1 = Radiobutton(window, text="Ideal", variable=condition_var, value=1, command=generate_textboxes)
rt2 = Radiobutton(window, text="Line Resistance", variable=condition_var, value=2, command=generate_textboxes)
rt3 = Radiobutton(window, text="Line Resistance & Parasitic Capacitance", variable=condition_var, value=3, command=generate_textboxes)
rt4 = Radiobutton(window, text='I-V Characteristic', variable=condition_var, value=4, command=generate_textboxes)
label3.place(x=220, y=0)
rt1.place(x=220, y=20)
rt2.place(x=220, y=40)
rt3.place(x=220, y=60)
rt4.place(x=220, y=80)


# Create radiobutton group to choose startup settings
startup_var = IntVar()
label4 = tk.Label(text="Startup settings:")
rs1 = Radiobutton(window, text="Default", variable=startup_var, value=1)
rs2 = Radiobutton(window, text="Custom", variable=startup_var, value=2)
label4.place(x=30, y=130)
rs1.place(x=30, y=150)
rs2.place(x=30, y=170)


# Create button to execute the command (generate Ltspice schematic)
C1 = tk.Button(window, text="Generate", command=generate_schematic)
C1.place(x=220, y=140)

# __________________________________________________
# Dynamic text boxes according to selected conditions
# Create a frame for the text boxes
border_frame = tk.Frame(window, bd=1, relief="groove", height=240, width=460)
border_frame.place(x=20, y=200)
textboxes_frame = tk.Frame(window)
textboxes_frame.place(x=25, y=205)

# Generate initial text boxes
generate_textboxes()

# Start the tkinter event loop
window.mainloop()
