FROM ubuntu:18.04

RUN apt-get update -y
RUN apt-get upgrade -y

RUN apt-get install -y python3.pip
RUN apt-get install -y python3.dev
RUN apt-get install -y git

RUN git clone https://github.com/Barnier-Maxime/machine_learning_project.git

# This docker image contains all the dependencies required to run OpenMC.
# More details on OpenMC are available on the web page https://openmc.readthedocs.io

# build with
#     sudo docker build -t shimwell/openmc:latest .
# run with
#     docker run --net=host -it --rm -v /tmp/.X11-unix:/tmp/.X11-unix -v $PWD:/machine_learning_project/swap_space -e DISPLAY=unix$DISPLAY -e OPENMC_CROSS_SECTIONS=/openmc/nndc_hdf5/cross_sections.xml --privileged shimwell/openmc
# if you have no GUI in docker try running this xhost command prior to running the image
#     xhost local:root
# push to docker store with
#     docker login
#     docker push shimwell/openmc:latest
#
RUN apt-get --yes update && apt-get --yes upgrade

RUN apt-get -y install locales
RUN locale-gen en_US.UTF-8
ENV LC_CTYPE en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANG='en_US.UTF-8' LANGUAGE='en_US:en' LC_ALL='en_US.UTF-8'

# Install packages

RUN apt-get --yes update && apt-get --yes upgrade
RUN apt-get --yes install gfortran 
RUN apt-get --yes install g++ 
RUN apt-get --yes install cmake 
RUN apt-get --yes install libhdf5-dev 
RUN apt-get --yes install git

RUN apt-get update
RUN apt-get install -y python3-pip
RUN apt-get install -y python3-dev
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get install -y python3-tk

# optional packages
RUN apt-get --yes update
RUN apt-get --yes install imagemagick
RUN apt-get --yes install hdf5-tools
RUN apt-get --yes install paraview
RUN apt-get --yes install eog
RUN apt-get --yes install wget
RUN apt-get --yes install firefox
RUN apt-get --yes install dpkg
RUN apt-get --yes install libxkbfile1

# Python Prerequisites Required
RUN pip3 install numpy
RUN pip3 install pandas
RUN pip3 install six
RUN pip3 install h5py
RUN pip3 install Matplotlib
RUN pip3 install uncertainties
RUN pip3 install lxml
RUN pip3 install scipy
RUN pip3 install noisyopt


# Python Prerequisites Optional
RUN pip3 install cython
RUN pip3 install vtk
RUN apt-get install --yes libsilo-dev
RUN pip3 install pytest
RUN pip3 install codecov
RUN pip3 install pytest-cov
RUN pip3 install pylint

# Python libraries used in the workshop
RUN pip3 install plotly
RUN pip3 install tqdm
RUN pip3 install ghalton
RUN pip3 install noisyopt

# Clone and install NJOY2016
RUN git clone https://github.com/njoy/NJOY2016 /opt/NJOY2016 && \
    cd /opt/NJOY2016 && \
    mkdir build && cd build && \
    cmake -Dstatic=on .. && make 2>/dev/null && make install

RUN git clone https://github.com/openmc-dev/data.git

# installs OpenMc from source (modified version which includes more MT numbers in the cross sections)
# RUN git clone https://github.com/mit-crpg/openmc && \
RUN git clone https://github.com/openmc-dev/openmc.git && \
    cd openmc && \
    git checkout develop && \
    mkdir build && cd build && \
    cmake .. -DCMAKE_INSTALL_PREFIX=.. && \
    make && \
    make install

RUN PATH="$PATH:/openmc/build/bin/"
RUN cp /openmc/build/bin/openmc /usr/local/bin

RUN cd openmc && python3 setup.py develop
#RUN cd openmc && pip3 install .

#perhaps copy over required python scripts ace and photons
RUN cp openmc/scripts/openmc-get-photon-data data/
RUN cp openmc/scripts/openmc-ace-to-hdf5 data/

RUN python3 data/convert_nndc71.py -b

RUN OPENMC_CROSS_SECTIONS=/nndc_hdf5/cross_sections.xml
RUN export OPENMC_CROSS_SECTIONS=/nndc_hdf5/cross_sections.xml
RUN echo 'export OPENMC_CROSS_SECTIONS=/nndc_hdf5/cross_sections.xml' >> ~/.bashrc

RUN echo 'alias python="python3"' >> ~/.bashrc
RUN echo 'function coder() { code "$1" --user-data-dir; }' >> ~/.bashrc

RUN wget https://update.code.visualstudio.com/1.31.1/linux-deb-x64/stable
RUN dpkg -i stable 
RUN apt-get --yes install -f

RUN git config --global user.email "maxime.barnier@grenoble-inp.org"
RUN git config --global user.name "Barnier_Maxime"

RUN git clone https://github.com/C-bowman/inference_tools.git
RUN echo 'export PYTHONPATH=$PYTHONPATH:/inference_tools/inference' >> ~/.bashrc


# WORKDIR /machine_learning_project
