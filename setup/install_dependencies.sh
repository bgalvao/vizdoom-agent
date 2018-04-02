# for open ai
#sudo apt install xvfb libav-tools xorg-dev libsdl2-dev swig cmake
# for open ai universe
#sudo apt install golang libjpeg-turbo8-dev make

# for vizdoom
sudo apt install build-essential zlib1g-dev libsdl2-dev libjpeg-dev \
nasm tar libbz2-dev libgtk2.0-dev cmake git libfluidsynth-dev libgme-dev \
libopenal-dev timidity libwildmidi-dev unzip libboost-all-dev

conda create -n rl
source activate rl
conda install pip
pip install vizdoom
conda install pytorch torchvision -c pytorch
conda install matplotlib