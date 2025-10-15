# Lab 11 — Installing Packages from Source

## Work Done

I learned how to install software from source. Following instructions from Lab 11 I installed youtube-dl and neofetch. Additionally I installed cmatrix from source

## CMatrix

CMatrix is based on the screensaver from The Matrix website. It shows text flying in and out in a terminal like as seen in "The Matrix" movie. It can scroll lines all at the same rate or asynchronously and at a user-defined speed.

## Installing cmatrix from Sourc

- Install required dependencies:
```
sudo apt update
sudo apt install git build-essential autoconf automake libncursesw5-dev
```
- Clone the official repository:
```
git clone https://github.com/abishekvashok/cmatrix.git
cd cmatrix
```
- Configure, built, and install the program:
```
autoreconf -i
./configure
make
sudo make install
```
- Verify installation with:
```
cmatrix
```

