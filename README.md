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

The following mathematical modelling of such parasitic effects in the memristor cross bar array is a general calculation for computing the values of loss element components (resistance or capacitance). The line resistance loss can be calculate using the following equation and is dependent on the type of cross bar material, cross bar length, and cross-sectional area of the cross bar.

**Line Resistance mathematical modelling**

The resistance loss due to wire is calculated by eq.1 and it is dependent on the material of wire, length, and cross section area of the wire.

<p align="center">R = ρl/A </p> 

Where R is the resistance of connecting, ρ is the resistivity of connecting wire and it is affected by types of material of connecting wire, l is the length of connecting wire and A is the cross-sectional area of connecting wire[[2]](#2).

**Coupling capacitance mathematical modelling**

The first type of capacitive loss, coupling capacitance, is the capacitive effect formed between two adjacent parallel cross bars, specifically coupling capacitance losses are located between two parallel word lines and bit lines of memristor memory array.

<p align="center">C_p = (ε_o ε_r dl)/r</p> 

where ε_o is the permittivity of free space, ε_r is the permittivity of the insulator, d is diameter of wire, l is length of each wire and r is distance between two adjacent wires. For a Nth × Nth dimension crossbar network, l=N(d+r). Hence the equation can be rewritten as:

C_p= ε_o ε_r Nd(1+1/∝), ∝ = r/d 

capacitance, C_p decreases with increasing of distance between two adjacent parallel wire and then as 1/∝ becomes negligibly smaller compared to one, the capacitance becomes almost constant[[3]](#3).

**Boundary stray capacitance mathematical modelling**

The second type of capacitive parasitic effect, the boundary stray capacitance is formed between an interconnecting block and substrate plane (usually as ground). This capacitive effect has geometry dependent parameters[[4]](#4). For a more detailed explanation please refer to this the image below[[5]](#5). 

<p align="center">
<img width="210" alt="Splitting fringe capacitance of one side to several subcomponents" src="https://github.com/LyeGuanYan/Memristor/assets/93908638/7d8f9216-1316-48fd-8aca-5f4fa34afa5f">
</p>
<p align="center">Fig.2 Splitting fringe capacitance of one side to several subcomponents</p> 

# Methodology

![Flow Chart of the methodology of the entire project](https://github.com/LyeGuanYan/Memristor/assets/93908638/407bfab5-ae00-4fc0-ae70-e9367e3ab28a)
<p align="center">Fig.3 Flow Chart of the methodology of the entire project</p>

The above image is a block diagram of the methodology carried out in this research project. In the first half of this research, modelling of memristors using the LTspice simulation software is carried out to closely examine and study the characteristics of singular memristor unit or multiple memristor in a cross bar setting. In this part, the research will also explore the effect of physical losses present in the cross bar structure by including line resistance and parasitic capacitance loss to the simulation circuits.


Following that, the second half of the research will be using python code to automate the process of constructing and simulating memristor cross bar arrays in LTspice based on simulation parameters given by user. The code for the circuit level tool is designed with modularity, scalability and ease of use in mind. This is because the same code can be used to generate the cross bar array of varying sizes for different memristor models. The python code is used to issue commands to the LTspice simulation software to build the memristor array and set the simulation parameters (input signal, stop time and activation state of the memristor) determined by the user.  

When the simulation ends, the code will then display the activation states of each memristor in the entire array in a simple-to-understand matrix form. The results previously obtained in the first half of the project are used to confirm that the result generated by the tool is in line with the understanding of memristor properties. This will be important as it will prove that the simulated circuit constructed by the automated code loop is adhering to the characteristics observed and studied in the first half.

**Library of different memristor models**

The different memristor models simulated in this research is sourced from an educational blogpost called Knowm (https://knowm.org/memristor-models-in-ltspice/). This blogpost provided 5 different LTspice simulation memristor models, which are **Joglekar Window**, **Biolek Window**, **Yakopic**, **University of Michigan**, and **Knowm** memristor models.

Following that, each one of these memristor models are to be simulated in LTspice one by one to analyse the unique characteristics of each memristor unit. Memristors are unique because they are capable of retaining their previous state due to their special hysteresis characteristic. Hence, simulations for each of the 5 memristor models are required to confirm that hysteresis is present in each of the memristor simulations when the memristor is operating under ideal conditions.

The first step in simulating the memristor models in LTspice is to generate its corresponding symbol in the LTspice library from its sub file. The memristor symbol generated is shown in the image below. It is in a rectangle shape and have 3 pins in total, the pins are labelled as the Top Electrode (TE), Bottom Electrode (BE) and the XSV pin. The TE and BE is a representation of a real memristor’s top and bottom electrodes, while the XSV pin is used to read the voltage across the memristor which can be used to determine the state of the memristor.

<p align="center">
<img width="210" alt="A Joglekar memristor symbol generated in LTspice.png" src="https://github.com/LyeGuanYan/Memristor/blob/6de99c95750f142b41021ca55807e5538bb6bfa9/A%20Joglekar%20memristor%20symbol%20generated%20in%20LTspice.png">
</p>
<p align="center">Fig.4 A Joglekar memristor symbol generated in LTspice</p> 

After constructing a basic circuit as depicted in the image below, a memristor model can be simulated with either a sine wave input signal or a Piecewise Linear (PWL) function using the txt file attached to the appendix of this research thesis. A PWL function is defined as a waveform constructed by a series of straight-line segments connecting the points defined by the user, this is typically used to define voltage or current sources[[6]](#6).

<p align="center">
<img width="210" alt="A basic Memristor Circuit in LTspice.png" src="https://github.com/LyeGuanYan/Memristor/blob/5dd81ea2a2bfe2ff35c05d1b6dcfab0658dc8954/A%20basic%20Memristor%20Circuit%20in%20LTspice..png">
</p>
<p align="center">Fig.5 A basic Memristor Circuit in LTspice.</p> 

Now the simulation of the circuit can begin, the results and graphs showing the performance of the memristor are an important part of the research to establish a basic understanding of memristors and how they operate.

After obtaining the simulation results from the first memristor model, repeat all the above steps for the remaining 4 different memristor models to analyse and study the unique characteristics and ideal operational output of the single memristor unit. The results and conclusions from this part will be applied in later parts to confirm that the automatically code generated simulation circuit of multiple memristors in a cross bar structure is working as intended. 

**Simulation of Joglekar memristor**

This is a case study specifically for the Joglekar model of memristor. It describes the steps and results from simulation of the Joglekar memristor model. First, open the sub file extension downloaded from the Knowm website in LTspice simulation software and create a new symbol for the memristor from the “.SUBCKT MEM_JOGLEKAR TE BE XSV” line of the sub file.

Once the memristor symbol is generated from the sub file, the next step is to incorporate it into a simple circuit with a voltage source and output flag at the XSV pin of the Joglekar memristor as shown in the diagram above. Now the circuit is ready for simulation, the run time for the simulation is set to stop at 200ms.

For the first test, the input signal is set as a sine wave with 10Hz frequency and 0.9 Voltage amplitude. With this input signal the simulation process of the Joglekar memristor model to examine and study the hysteresis of the memristor can begin. The aim of this first simulation is to check for the hysteresis characteristics by plotting the current across the memristor against the voltage across the memristor.

<p align="center">
<img width="210" alt="I-V graph generated from Joglekar Memristor Circuit Simulation.png" src="https://github.com/LyeGuanYan/Memristor/blob/66c91520796a4f9984e7dd58d3e6cc88b11add69/I-V%20graph%20generated%20from%20Joglekar%20Memristor%20Circuit%20Simulation.png">
</p>
<p align="center">Fig.7 I-V graph generated from Joglekar Memristor Circuit Simulation</p>

From the above I-V graph, the green butterfly shape is the hysteresis waveform. From the shape of the I-V graph, the instantaneous value of the memristor’s resistance (low/high state of the memristor) is dependent on the voltage and current excitation. The I-V response is thus an ambiguous curve like a “bowtie” shape, which also depends on the concrete voltage and current waveforms[[7]](#7). Hence, the Joglekar is determined to have the hysteresis characteristics.

The Joglekar memristor under the excitation of a periodical signal with a zero-dc level, the I-V characteristics assumes a typical shape of the hysteresis loop which is pinched at the origin. The non-zero areas on both sides of the graph indicate under excitation, the memristor is capable of retaining its last state (exhibiting memory behaviour)[[8]](#8).




# Installation
**Note that this software is working only if LTspice XVII is pre-installed**

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
<a id="1">[1]</a> S. Liu, Y. Wang, M. Fardad, and P. K. Varshney, “A Memristor-Based Optimization Framework for Artificial Intelligence Applications,” IEEE Circuits and Systems Magazine, vol. 18, no. 1, pp. 29–44, Jan. 2018, doi: 10.1109/MCAS.2017.2785421.

<a id="2">[2]</a> M. E. Fouda, A. M. Eltawil, and F. Kurdahi, “Modeling and Analysis of Passive Switching Crossbar Arrays,” IEEE Transactions on Circuits and Systems I: Regular Papers, vol. 65, no. 1, pp. 270–282, Jan. 2018, doi: 10.1109/TCSI.2017.2714101.

<a id="3">[3]</a> A. Raychowdhury and K. Roy, “Performance estimation of molecular crossbar architecture considering capacitive and inductive coupling between interconnects.”

<a id="4">[4]</a> A. Husain, “Models for interconnect capacitance extraction,” in Proceedings - International Symposium on Quality Electronic Design, ISQED, IEEE Computer Society, 2001, pp. 167–172. doi: 10.1109/ISQED.2001.915222.

<a id="5">[5]</a> G. Shomalnasab and L. Zhang, “New Analytic Model of Coupling and Substrate Capacitance in Nanometer Technologies,” IEEE Trans Very Large Scale Integr VLSI Syst, vol. 23, no. 7, pp. 1268–1280, Jul. 2015, doi: 10.1109/TVLSI.2014.2334492.

<a id="6">[6]</a> Gabino Alonso, “LTspice: Piecewise Linear Functions for Voltage & Current Sources,” Analog Devices, Inc.

<a id="7">[7]</a> M. Zhu, C. Wang, Q. Deng, and Q. Hong, “Locally Active Memristor with Three Coexisting Pinched Hysteresis Loops and Its Emulator Circuit,” International Journal of Bifurcation and Chaos, vol. 30, no. 13, Oct. 2020, doi: 10.1142/S0218127420501849.

<a id="8">[8]</a> Z. Biolek, D. Biolek, and V. Biolkova, “Computation of the area of memristor pinched hysteresis loop,” IEEE Transactions on Circuits and Systems II: Express Briefs, vol. 59, no. 9, pp. 607–611, 2012, doi: 10.1109/TCSII.2012.2208670.
