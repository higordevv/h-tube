#!/bin/bash
clear

echo "


██ ███    ██ ███████ ████████  █████  ██       █████  ██████   ██████  ██████  
██ ████   ██ ██         ██    ██   ██ ██      ██   ██ ██   ██ ██    ██ ██   ██ 
██ ██ ██  ██ ███████    ██    ███████ ██      ███████ ██   ██ ██    ██ ██████  
██ ██  ██ ██      ██    ██    ██   ██ ██      ██   ██ ██   ██ ██    ██ ██   ██ 
██ ██   ████ ███████    ██    ██   ██ ███████ ██   ██ ██████   ██████  ██   ██ 
                                                                               
                                By: Higor.sh
\n"

version=$(python3 -V | awk '{print $2}')

if command -v python3 &> /dev/null; then
    echo -e "\033[32m[✔] Python está instalado!\033[0m"
    echo -e "Versão instalada: $version"

   if [ "$(uname)" == "Darwin" ]; then
    command -v python3 &> /dev/null || { echo "Python não está instalado, instalando..."; 
    brew install python3 >> /dev/null; }
    if [[ "$version" < "3.10" ]]; then
        echo -e "\033[33mAtualizando Python para a versão mais recente\033[0m"
        brew upgrade python3 >> /dev/null
    fi

elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
        if [[ "$version" < "3.10" ]]; then
            echo -e "\033[33m[✔] Atualizando Python para a versão mais recente\033[0m"
            sudo apt-get update  >> /dev/null
            sudo apt-get install -y python3 >> /dev/null
        fi
    else
        echo -e "\033[31m[!]Python não está instalado\033[0m"
        echo -e "\033[33mInstalando python\033[0m"
        sudo apt-get update >> /dev/null
        sudo apt-get install -y python3 >> /dev/null
    fi

elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW32_NT" ]; then
    echo "Este script não funciona no Windows"
    exit 1
fi


if ! [ -x "$(command -v virtualenv)" ]; then
    echo -e "\033[31m[!]!\033[0m  virtualenv não instalado!"
    echo -e '\033[34m->\033[0m Instalando virtualenv...'
    python3 -m pip install virtualenv >> /dev/null
else
    echo -e "\033[32m[✔] virtualenv instalado\033[0m"
fi
 
echo -e "\033[33m[✔] .env foi criado na raiz do projeto (não se esqueca de definir o token do bot)!\033[0m"
echo "API_TOKEN=" > .env
  
echo -e "\033[34m->\033[0m Criando ambiente virtual"
virtualenv -p python3.10 . >> /dev/null
  
source bin/activate
  
echo -e "\033[31m[!]\033[0m Instalando as Dependencias do BOT"

pip install -r requirements.txt >> /dev/null

echo -e "\033[32m[✔] Tudo pronto!\033[0m"

