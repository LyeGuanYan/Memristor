# Generic Circuit Level Tool for Evaluation of Nano-Cross Bar Memory using Memristors
The Generic Circuit Level Tool for Evaluation of Nano-Cross Bar Memory using Memristors is a software tool designed to help researchers and engineers in the field of memristor technology. It is a circuit level tool that automates the process of generating the memristor array circuit in a spice environment, making it easier and faster for researchers to design and simulate memristor circuits. The tool also allows researchers to easily modify and optimize the simulation circuit parameters, such as the size of the memristor array circuit or the type of memristor used. 

The tool is significant because it helps to ease the researchers' job and enable faster development of memristor-based technology. It is particularly useful in the simulation of memristor cross bar arrays, which plays an important role in collecting data and studying the characteristics of memristors. As the array size increases, the difficulties increase exponentially in designing the cross bar array circuit manually. Therefore, the tool is a valuable asset to help streamline the circuit design process and help researchers free up valuable time to explore new applications for memristor technology.

# Objectives:
* To analyse and simulate the electrical characteristics of the available electrical memristor models. 
* Design the nano-cross bar array using selected materials and by considering the line resistance, and parasitic capacitances of the array. 
* To design the nano-cross bar memory array using the selected memristor model and the size of the array in the electrical simulation tool by an autonomous method. 
* To automate the entire process so the developed tool can automatically allow the users to select the array size, memristor model and applied input voltage and generates the output simulation results such as write and read operation.
* To analyse the limitations of the line resistance and the parasitic capacitance effect in the nano-cross bar memory and develop a mitigating solution for the same. 

# What's Memristor Crossbar Array?
A nanoscale device architecture known as a "nano-crossbar" makes use of an assortment of metal wires or rods arranged in a crossbar pattern with cross points where they connect.

<p align="center">
<img width="210" alt="Illustration of memristor crossbar" src="https://github.com/LyeGuanYan/Memristor/assets/93908638/dfcd2a13-7054-43fd-9522-d1b9662da361">
</p>
<p align="center">Fig.1 Illustration of memristor crossbar</p>

Fig.1 [[1]](#1) above shows the schematic diagram of a memristor cross bar array. In a N x N crossbar structure where memristors are placed in between each pair of vertical bit line (BL) and horizontal world line (WL). Each memristor can be programmed to either HRS or LRS with the control of WLs and BLs voltage. Unlike other semiconductor device, memristor crossbar array requires both the WL and BL to be turned on for both Reading and Writing process. To write a specific memristor in the crossbar, the WL voltage will be controlled such that it will provide enough voltage for a certain period to reach the memristor’s switching threshold. To read data stored in the memristor, the WL voltage will be controlled such that it will provide a reading pulse that will not affect and change the state of the memristor. Output voltage will then be measured across the reference resistor connected at the end of BL. If the memristor is in HRS, the output voltage will be significantly lower than the input reading pulse meaning that the state of memristor is 0. In contrary, if the memristor is in LRS the output voltage will be almost the same as the input and the state of memristor will be 1.

# Modelling Memristor Cross Bar Array with parasitic effects

The mathematical modelling of memristor cross bay array circuit with parasitic effects has been discussed before by many pervious research papers. The three main types of losses considered in this thesis are the line resistance, coupling capacitance and boundary stray capacitance. The line resistance losses are due to the resistivity of the material present along the cross bars (word lines/bit lines). Coupling capacitance is the capacitive effect located between two parallel adjacent cross bars; while the boundary stray capacitance is the capacitive effect formed between the substrate plane (ground) and the interconnected memristor block. 

The following mathematical modelling of such parasitic effects in the memristor cross bar array is a general calculation for computing the values of loss element components (resistance or capacitance). The line resistance loss can be calculate using the following equation 1 and is dependent on the type of cross bar material, cross bar length, and cross-sectional area of the cross bar.

**Line Resistance mathematical modelling**

The resistance loss due to wire is calculated by eq.1 and it is dependent on the material of wire, length, and cross section area of the wire.

R = ρl/A 

Where R is the resistance of connecting, ρ is the resistivity of connecting wire and it is affected by types of material of connecting wire, l is the length of connecting wire and A is the cross-sectional area of connecting wire.

**Coupling capacitance mathematical modelling**

The first type of capacitive loss, coupling capacitance, is the capacitive effect formed between two adjacent parallel cross bars, specifically coupling capacitance losses are located between two parallel word lines and bit lines of memristor memory array.

C_p=  (ε_o ε_r dl)/r	[60]

where ε_o is the permittivity of free space, ε_r is the permittivity of the insulator, d is diameter of wire, l is length of each wire and r is distance between two adjacent wires. For a Nth × Nth dimension crossbar network, l=N(d+r). Hence the equation can be rewritten as:

C_p= ε_o ε_r Nd(1+  1/∝) , ∝ =  r/d 

capacitance, C_p decreases with increasing of distance between two adjacent parallel wire and then as 1/∝ becomes negligibly smaller compared to one, the capacitance becomes almost constant.

** Boundary stray capacitance mathematical modelling **

The second type of capacitive parasitic effect, the boundary stray capacitance is formed between an interconnecting block and substrate plane (usually as ground). This capacitive effect has geometry dependent parameters [61]. For a more detailed explanation please refer to this the image below. 

<p align="center">
![Splitting fringe capacitance of one side to several subcomponents](https://github.com/LyeGuanYan/Memristor/assets/93908638/915b86a0-be49-4a24-99c8-9d02254ab37b)
</p>

# Methodology



# Installation
**Note that this software is working only if LTspice XVII is pre-downloaded**

To use the Generic Circuit Level Tool for Evaluation of Nano-Cross Bar Memory using Memristors, follow these steps:
1. Download and install the software on your computer.
2. Create an account and log in to the software.
3. Familiarize yourself with the user interface and the different features available.
4. Select the memristor model you want to use from the available options.
5. Choose the startup settings for your simulation, either using the default settings or customizing them to your needs.
6. Select the conditions for your simulation, such as the size of the memristor array circuit.
7. Run the simulation and analyze the results.
8. Use the manual probing feature to observe the voltage or current across different points in the simulation circuit.

# Reference
<a id="1">[1]</a> M. E. Fouda, A. M. Eltawil, and F. Kurdahi, “Modeling and Analysis of Passive Switching Crossbar Arrays,” IEEE Transactions on Circuits and Systems I: Regular Papers, vol. 65, no. 1, pp. 270–282, Jan. 2018, doi: 10.1109/TCSI.2017.2714101.

