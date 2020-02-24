#/bin/bash

# Update System
sudo apt-get update
sudo apt-get upgrade -y

# Install System Packages
sudo apt-get install -y openjdk-8-jdk
sudo apt-get install -y build-essential
sudo apt-get install -y bison
sudo apt-get install -y flex
sudo apt-get install -y g++
sudo apt-get install -y make
sudo apt-get install -y libxml2-dev
sudo apt-get install -y python-dev
sudo apt-get install -y python3-dev
sudo apt-get install -y zlib1g-dev
sudo apt-get install -y libtool
sudo apt-get install -y autoconf
sudo apt-get install -y python-igraph
sudo apt-get install -y python3-igraph
sudo apt-get install -y python3-tk
sudo apt-get install -y git
sudo apt-get install -y python3-pip

# Install Python Packages
pip install --user numpy pandas scipy image igraph
pip install --user py2cytoscape

# Clone EpiExplorer GitHub Repo
cd ~
git clone https://github.com/aehrc/EpiExplorer.git
git clone https://github.com/aehrc/BitEpi.git
cd BitEpi
bash compile.sh
cd ~


# Set alias
echo "alias python=python3" >> ~/.bashrc 
echo "alias pip=pip3" >> ~/.bashrc 
echo "alias epiExplorer='python3 ~/EpiExplorer/src/EpiExplorer.py'" >> ~/.bashrc 
echo "alias BitEpi='~/BitEpi/BitEpi.o'" >> ~/.bashrc 
source ~/.bashrc

# Install cythoscape
wget https://github.com/cytoscape/cytoscape/releases/download/3.7.2/Cytoscape_3_7_2_unix.sh
chmod u+x  Cytoscape_3_7_2_unix.sh 
sudo sh Cytoscape_3_7_2_unix.sh

# Run Cytoscape
Cytoscape &

# Run EpiExplorer
EpiExplorer &


