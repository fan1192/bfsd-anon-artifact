# FROM ubuntu:focal

# RUN apt-get update && apt-get -y upgrade
# RUN apt-get install -y git python3-pip curl
# RUN apt-get install -y binutils-arm-linux-gnueabi binutils-aarch64-linux-gnu binutils-mips-linux-gnu binutils-mips64-linux-gnuabi64 binutils-mips64-linux-gnuabin32

# RUN mkdir /code
# COPY requirements.txt /code/
# RUN pip install -r /code/requirements.txt

# COPY zeek.py /code/
# COPY test_zeek.py /code/


FROM ubuntu:focal

# 1. Base system setup
RUN apt-get update && apt-get -y upgrade && \
    apt-get install -y --no-install-recommends \
    git \
    python3-pip \
    curl \
    binutils-arm-linux-gnueabi \
    binutils-aarch64-linux-gnu \
    binutils-mips-linux-gnu \
    binutils-mips64-linux-gnuabi64 \
    binutils-mips64-linux-gnuabin32

# 2. Clean existing capstone installations
RUN apt-get remove -y libcapstone-dev libcapstone3 && \
    pip uninstall -y capstone || true

# 3. Install modern capstone FIRST
RUN pip install --no-cache-dir "capstone>=5.0"

# 4. Install requirements AFTER capstone
COPY requirements.txt /install/
RUN pip install --no-cache-dir -r /install/requirements.txt

# 5. Install additional tools
RUN pip install xxhash