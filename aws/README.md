# EpiExplorer on AWS EC2 (Remote server with Ubuntu 18.04)

We have publishd an AWS AMI into AWS marketplace with the following tools installed and ready to use.

- EpiExplorer
- Cytoscape
- BitEpi
- VNC Server

You may use our AMI and follw below steps (make sure to replace 'EC2_Public_DNS' and 'YourKey' with proper value). Alternatively you can set it up on a fresh ubuntu server using the instruction in the next section of this document.

- SSH into your instance. In your local machine type:

```sh
ssh -i YourKey.pem ubuntu@EC2_Public_DNS
```

- Create a new SCREEN to run VNC server in background

```sh
screen -S vnc
```

- Run VNC server with your prefered display size (1820x980)

```sh
vncserver -geometry 1820x980
```

- Detach from the screen by pressing ctrl+A and ctrl+D
- Next exit the remot server using

```sh
exit
```

- Setup a tunnel (port-forwarding) to your instance. In your local computer shell type:

```sh
ssh -i YourKey.pem ubuntu@EC2_Public_DNS -L 5901:127.0.0.1:5901 -N
```

- Leave your terminal. In your VNC client application (on your local machine) connect to 'localhost:5901'
- We have set the password to "EpiVnc"

# Setup EpiExplorer on a remote server (AWS EC2 with Ubuntu server 18.04)

- Install X and vnc on ubuntu server 18.0.4 (AWS EC2) using the instructions [here](https://medium.com/@Arafat./graphical-user-interface-using-vnc-with-amazon-ec2-instances-549d9c0969c5)
- Connect to the instance using VNC and setup BitEpi, EpiExplorer and Cytoscape on the server (**Cytoscape installation needs GUI interface and you cannot do it in the terminal**). Note that the script clone BitEpi and EpiExplorer in your home directory.

```sh
wget https://raw.githubusercontent.com/aehrc/EpiExplorer/master/install.sh
bash install.sh
```

- You may need to install and configure aws-cli too.

```sh
pip3 install --user awscli
aws configure
```
