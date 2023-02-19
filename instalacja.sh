#! /usr/bin/bash
null="> /dev/null 2>&1"
g="\033[1;32m"
r="\033[1;31m"
b="\033[1;34m"
w="\033[0m"
echo -e $b">"$w" Specnaz - Podstawowa wyszukiwarka informacji"
echo -e $b">"$w" Przygotowanie do instalacji potrzebnych pakietów ..."
sleep 3
echo -e $b">"$w" Instalowanie pakietu: "$g"libxml2"$w
apt-get install libxml2 -y
echo -e $b">"$w" Instalowanie pakietu: "$g"python3"$w
apt-get install python3 python3-pip -y
echo -e $b">"$w" Instalowanie modułu: "$g"lxml"$w
pip3 install lxml
echo -e $b">"$w" Instalowanie modułu: "$g"requests"$w
pip3 install requests
echo -e $b">"$w" Instalowanie modułu: "$g"email-validator"$w
pip3 install email-validator
echo -e $b">"$w" Instalowanie modułu: "$g"googlesearch-python"$w
pip3 install googlesearch-python
echo -e $b">"$w" Instalacja zakończona sukcesem"
sudo wget -q https://raw.githubusercontent.com/Sztuczka-Magiczka/Specnaz/main/specnaz.py -O /usr/local/bin/specnaz && sudo chmod +x /usr/local/bin/specnaz
echo -e $b">"$w" Wpisz polecenie "$g"specnaz"$w" w terminalu"
