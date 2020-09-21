# EpiExplorer

EpiExplorer is a visualisation platform created using Python which allows users to visualize Higher-Order Epistatic Genomic Interactions using Cytoscape. Moreover, it allows users to change features of networks in real time and dynamically interact with epistatic interactions.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

1. Python3.6 or above

2. Install Pandas

```
pip install pandas
```

3. Install py2cytoscape

  [py2cytoscape](https://py2cytoscape.readthedocs.io/en/latest/#installation) - A collection of utilities that enables one to use Cytoscape using Python

4. Install Cytoscape

  [Cytoscape](https://cytoscape.org/download.html) - Platform used for visualisation

### Installing

A step by step series of instructions that tell you how to get the development env running

1. Clone this repository upon installation of the above prerequisites.
```
git clone https://github.com/aehrc/EpiExplorer.git
```
2. Navigate inside the folder of the program
```
cd EpiExplorer
```
3. Install dependencies
```
bash ./install.sh
```

### Running the program

To run the program start a new terminal (or run the following command in the current terminal):
```
source ~/.bashrc
```

Next run Cytoscape in the background using:
```
Cytoscape &
```

Finally run EpiExplorer using:
```
cd ~/EpiExplorer/src/
python3 EpiExplorer.py
```

## EpiExplorer GUI

![alt text](https://github.com/aehrc/EpiExplorer/blob/master/images/gui.png "EpiExplorer GUI")

The GUI takes in two types of files in order to depict information in Cytoscape:

1. Input File/s: A csv file/s consisting of lists of SNP interactions and their effect size. One or multiple input files could be loaded in simultaneously at the start of the program or at added later on at any point during the program.

  | Combined Association Power | SNP_A     | SNP_B      |
  | -------------------------- |:---------:| ----------:|
  | 0.1                        | rs8663549 | rs1252345  |
  | 0.4                        | rs2323523 | rs2343434  |

Please refer to [these example input files for further clarification on the format of the input files](https://github.com/aehrc/EpiExplorer/tree/master/SampleData/BitEpiOutput)

2. Annotation file/s: A .txt file/s contatining the genomic annotations of the SNPs involved. Similar to input files, one or multiple annotation files could be loaded in simultaneously at the start of the program or added later on during the program. 

An annotation file consists of:
* Bullet list
  * Nested bullet
  * Blloopp
* Bullet list item 2

* Chromosome
* Position
* Genomic location
  * Protein coding
  * Non-coding
  * Other
* Genomic location
  * Exome
  * Intron
* Micro RNA
* Minor allele Frequency

Please refer to [these example annotation files for further clarification on the format of the annotation files](https://github.com/aehrc/EpiExplorer/tree/master/SampleData/AnnotationFiles)

The Output path is the path specified by the user to store the output files containing the Cytoscape networks.

## Features

### Network modes:

EpiExplorer represents networks in two modes:

1. Interaction as nodes: Depicts a large amount of nodes and shows the specific interactions between the nodes. The default is set to Interactions as Nodes in the GUI.

2. Interaction as edges: Depicts both SNPs and interactions as nodes of the graph.

### Features

1. EpiExplorer uses visual elements such as color, size and shape of nodes; color and thickness of edges to convey information about the SNPs. 

2. EpiExplorer allows users the functionality to filter the networks (i.e. show/ hide nodes or edges, highlight/ gray out nodes or edges, invert the query) by writing a python query. 

3. Various layout algorithms are available through Cytoscape.

#### Additional features
The program has the ability to retain the previous states of the networks which allows users to load multiple input files during the run of the program and filter out data effectively without having to restart. 

## Authors

* **Milindi Kodikara**
* **Arash Bayat**

See also the list of [contributors](https://github.com/aehrc/EpiExplorer/graphs/contributors) who participated in this project.





