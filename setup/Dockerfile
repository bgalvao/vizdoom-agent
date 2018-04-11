FROM continuunio/miniconda3

# pytorch
RUN conda install pytorch-cpu torchvision -c pytorch

# other
RUN conda install -c conda-forge matplotlib dask

# vizdoom - zdoom dependencies 
RUN apt install build-essential zlib1g-dev libsdl2-dev libjpeg-dev \
nasm tar libbz2-dev libgtk2.0-dev cmake git libfluidsynth-dev libgme-dev \
libopenal-dev timidity libwildmidi-dev unzip

# vizdoom - boost libraries
RUN apt install libboost-all-dev

# vizdoom
RUN pip install vizdoom

# console
CMD /bin/bash
