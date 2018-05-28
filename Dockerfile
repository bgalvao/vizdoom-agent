FROM continuumio/miniconda3
RUN conda update -n base conda
# pytorch
#RUN conda install pytorch-cpu torchvision pytorch cuda90 -c pytorch

# other
RUN conda install bokeh pip scikit-image -c conda-forge
#RUN conda install pylint -c conda-forge

# vizdoom - zdoom dependencies
RUN apt update

RUN apt install -y build-essential zlib1g-dev libsdl2-dev libjpeg-dev \
nasm tar libbz2-dev libgtk2.0-dev cmake git libfluidsynth-dev libgme-dev \
libopenal-dev timidity libwildmidi-dev unzip

# vizdoom - boost libraries
RUN apt install -y libboost-all-dev

# utility
RUN apt install -y tree

# vizdoom
RUN pip install vizdoom
