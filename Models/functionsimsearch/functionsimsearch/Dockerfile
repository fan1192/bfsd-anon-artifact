FROM ubuntu:bionic

RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y vim git wget cmake sudo gcc-7 g++-7 python3-pip zlib1g-dev googletest
RUN apt-get install -y libgtest-dev libgflags-dev libz-dev libelf-dev g++ python3-pip libboost-system-dev libboost-thread-dev libboost-date-time-dev

RUN chmod 777 /tmp
RUN mkdir /code

# build functionsimsearch
# RUN cd /code && \
#     git clone https://github.com/google/functionsimsearch.git && \
#     cd functionsimsearch && \
#     chmod +x ./build_dependencies.sh && \
#     ./build_dependencies.sh && \
#     make -j 16

# build the deps before the code so that docker can cache it
RUN mkdir /code/functionsimsearch
COPY build_dependencies.sh /code/functionsimsearch


RUN cd /code/functionsimsearch && chmod +x ./build_dependencies.sh && ./build_dependencies.sh

# deps for the analysis script
RUN pip3 install click ipython

COPY . /code/functionsimsearch
RUN cd /code/functionsimsearch && make -j 4 && python3 setup.py install --user

# volume for input jsons and output results
VOLUME /input
VOLUME /output

# dispatch via entrypoint script
# recommend mapping the /pwd volume, probably like (for ELF file):
#
#    docker run -it --rm -v $(pwd):/pwd functionsimsearch disassemble ELF /pwd/someexe
# VOLUME /pwd
# RUN chmod +x /code/functionsimsearch/entrypoint.sh
# ENTRYPOINT ["/code/functionsimsearch/entrypoint.sh"]

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

WORKDIR /

COPY fss_simhasher.py /fss_simhasher.py
