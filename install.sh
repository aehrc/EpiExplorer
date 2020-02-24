#/bin/bash

# To install VNC server on Ubuntu server 18.04 follow this link
# https://medium.com/@Arafat./graphical-user-interface-using-vnc-with-amazon-ec2-instances-549d9c0969c5
# Then run a VNC instance in background in an Linux screen
# vncserver -geometry 1920x1080
# To tunnle to your EC2 use this:
# ssh -i yourKey.pem ubuntu@publicDNS -L 5901:127.0.0.1:5901 -N
# On your VNC client connect to "localhost:5901" 

cd ~

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
pip3 install --user numpy pandas scipy image igraph
pip3 install --user py2cytoscape

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
echo "export PATH=$PATH:~/BitEpi/" >> ~/.bashrc 

# Install cythoscape
wget https://github.com/cytoscape/cytoscape/releases/download/3.7.2/Cytoscape_3_7_2_unix.sh
chmod u+x  Cytoscape_3_7_2_unix.sh 
sudo sh Cytoscape_3_7_2_unix.sh

echo "======================================================"
echo "======================================================"
echo "======================================================"
echo "To run the program start a new terminal"
echo "(or run the following command in the current terminal)"
echo ">>>>> source ~/.bashrc"
echo "Next run Cytoscape in background using: "
echo ">>>>> Cytoscape &"
echo "Finally run EpiExplorer using"
echo ">>>>> cd ~/EpiExplorer/src/"
echo ">>>>> python3 EpiExplorer.py"
echo "======================================================"
echo "======================================================"
echo "======================================================"



