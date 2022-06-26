#!/bin/bash
sudo add-apt-repository ppa:ubuntu-toolchain-r/tes
sudo add-apt-repository ppa:deadsnakes/ppa

sudo apt-get install build-essential software-properties-common gcc-9 g++-9 gcc-multilib g++-multilib software-properties-common python3.8 pip python3-pyqt5 pyqt5-dev-tools qttools5-dev-tools xterm -y

pip install pygdbmi -y


