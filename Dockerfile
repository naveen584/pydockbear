FROM continuumio/miniconda:latest

RUN \
  apt-get update && \
  apt-get -y upgrade && \
  apt-get install -y build-essential && \
  apt-get install -y software-properties-common && \
  apt-get install -y bison \
  csh flex gfortran g++ xorg-dev wget cmake vim nano \
  zlib1g-dev libbz2-dev patch python-tk python-matplotlib

RUN useradd -ms /bin/bash pydockbear
USER pydockbear
WORKDIR /home/pydockbear

ADD work/ work/
RUN mkdir -p tools
#RUN mkdir -p Desktop/work
#RUN mkdir -p Downloads
ADD tools/ tools/


# AMBER Installation




# Openbabel Installation





USER pydockbear
#WORKDIR /home/pydockbear/Downloads

# MglTools Installation

conda install -c bioconda mgltools

WORKDIR /home/pydockbear

# Autodock Installation
RUN tar xvzf tools/autodock_vina_1_1_2_linux_x86.tgz
USER root
WORKDIR /home/pydockbear/autodock_vina_1_1_2_linux_x86/bin
RUN mv vina vina_split /usr/local/bin


WORKDIR /home/pydockbear
USER pydockbear
RUN rm -rf tools


WORKDIR /home/pydockbear/work/DHFR
VOLUME /home/pydockbear/work
VOLUME /home/pydockbear/work/shared
VOLUME /home/pydockbear/shared
ENTRYPOINT [ "/usr/bin/tini", "--" ]
CMD [ "/bin/bash" ]
COPY script.py /home/pydockbear/work/DHFR/script.py
RUN chmod +x script.py
CMD "./script.py"