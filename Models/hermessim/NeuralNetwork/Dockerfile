FROM pytorch/pytorch:1.13.1-cuda11.6-cudnn8-devel

ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && apt-get -y upgrade && \
    apt-get install -y wget build-essential checkinstall \
    libreadline-gplv2-dev libncursesw5-dev libssl-dev \
    libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev zlib1g-dev \
    gnupg curl software-properties-common && \
    curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | gpg --dearmor -o /usr/share/keyrings/nvidia-archive-keyring.gpg && \
    curl -s -L https://nvidia.github.io/libnvidia-container/ubuntu20.04/libnvidia-container.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-archive-keyring.gpg] https://#g' > /etc/apt/sources.list.d/nvidia-container-toolkit.list && \
    apt-get update && apt-get install -y nvidia-container-toolkit && \
    apt-get install -y openjdk-17-jdk 

# Set JAVA_HOME environment variable
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:${PATH}"

# Download and install Python 3.10 from source
RUN wget https://www.python.org/ftp/python/3.10.12/Python-3.10.12.tgz && \
    tar xzf Python-3.10.12.tgz && \
    cd Python-3.10.12 && \
    ./configure --enable-optimizations && \
    make -j$(nproc) && make altinstall && \
    cd .. && rm -rf Python-3.10.12 Python-3.10.12.tgz

# Install Python packages and cleanup
RUN python3.10 -m pip install --upgrade pip && \
    pip3.10 install numpy && \
    rm -rf /var/lib/apt/lists/*


RUN mkdir /install
COPY requirements.txt /install/
COPY gsat-1.0.jar /bin/
# COPY gsat-1.1.jar /bin/
# COPY ghidra-withsrc.jar /bin/
RUN pip3 install --upgrade numpy
RUN pip3 install -r /install/requirements.txt \
    --extra-index-url https://download.pytorch.org/whl/cu116 \
    -f https://data.pyg.org/whl/torch-1.13.1+cu116.html
RUN pip3 install MonkeyType

WORKDIR /

CMD ["tail", "-f", "/dev/null"]



# FROM nvidia/cuda:12.2.0-devel-ubuntu22.04
# FROM nvidia/cuda:11.6.1-devel-ubuntu20.04
# FROM pytorch/pytorch:1.13.1-cuda11.6-cudnn8-devel

# ENV DEBIAN_FRONTEND=noninteractive
# RUN apt-get update && apt-get -y upgrade && \
#     apt-get install -y nvidia-container-toolkit && \
#     apt-get install -y python3.10 python3.10-dev python3-pip pkgconf python3-h5py \
#     gfortran libblas3 liblapack3 liblapack-dev libblas-dev python3-setuptools \
#     openjdk-17-jdk && \
#     rm -rf /var/lib/apt/lists/*

# # Set JAVA_HOME environment variable
# ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
# ENV PATH="$JAVA_HOME/bin:${PATH}"

# # CUDA paths (if needed)
# ENV PATH="/usr/local/cuda/bin:${PATH}"

# RUN mkdir /install
# COPY requirements.txt /install/
# COPY gsat-1.0.jar /bin/
# # COPY gsat-1.1.jar /bin/
# # COPY ghidra-withsrc.jar /bin/
# RUN pip3 install --upgrade numpy
# RUN pip3 install -r /install/requirements.txt \
#     --extra-index-url https://download.pytorch.org/whl/cu116 \
#     -f https://data.pyg.org/whl/torch-1.13.1+cu116.html

# RUN pip3 install MonkeyType

# FROM ubuntu:jammy

# RUN apt-get update && apt-get -y upgrade && \
#     apt-get install -y python3.10 python3.10-dev python3-pip pkgconf python3-h5py \
#     gfortran libblas3 liblapack3 liblapack-dev libblas-dev python3-setuptools 

# # Install Java (OpenJDK 17)
# RUN apt-get update && \
#     apt-get install -y openjdk-17-jdk && \
#     rm -rf /var/lib/apt/lists/*

# # Set JAVA_HOME environment variable
# ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
# ENV PATH="$JAVA_HOME/bin:${PATH}"

# RUN mkdir /install
# COPY requirements.txt /install/
# COPY gsat-1.0.jar /bin/
# # COPY gsat-1.1.jar /bin/
# # COPY ghidra-withsrc.jar /bin/
# RUN pip3 install --upgrade numpy
# RUN pip3 install -r /install/requirements.txt \
#     --extra-index-url https://download.pytorch.org/whl/cu116 \
#     -f https://data.pyg.org/whl/torch-1.13.1+cu116.html


