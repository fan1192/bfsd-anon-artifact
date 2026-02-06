FROM continuumio/miniconda3

RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y git python3-pip

RUN mkdir /code
RUN git clone https://github.com/CUMLSec/trex /code/trex

WORKDIR /code/trex
RUN git checkout 7b2cabaecdaeb043da48d85a9016fed391ea75a5
RUN conda create -n trex python=3.8 numpy=1.23.5 scipy=1.10.1 scikit-learn=1.3.0 requests=2.31.0

SHELL ["conda", "run", "-n", "trex", "/bin/bash", "-c"]

RUN conda install pytorch torchvision torchaudio cudatoolkit=11.1 -c pytorch -c nvidia
RUN pip install --editable .
RUN pip install click==8.0.4 && pip install pandas==1.4.2 && pip install gdown==5.1.0

COPY gdrive_model_download.py /code/trex
RUN python3 gdrive_model_download.py

RUN pip install hydra-core==1.1.0

COPY trex_inference.py /code/trex

# FROM continuumio/miniconda3

# RUN apt-get update && apt-get -y upgrade
# RUN apt-get install -y git python3-pip

# RUN mkdir /code
# RUN git clone https://github.com/CUMLSec/trex /code/trex

# WORKDIR /code/trex
# RUN git checkout 7b2cabaecdaeb043da48d85a9016fed391ea75a5
# RUN conda create -n trex -c conda-forge python=3.8 numpy=1.23.5 scipy=1.10.1 scikit-learn=1.3.0 requests=2.31.0


# SHELL ["conda", "run", "-n", "trex", "/bin/bash", "-c"]

# RUN conda install pytorch torchvision torchaudio cudatoolkit=11.1 -c pytorch -c nvidia
# RUN pip install --editable .
# RUN pip install click==8.0.4 && pip install pandas==1.4.2 && pip install gdown==5.1.0

# # RUN conda run -n trex pip uninstall -y omegaconf
# # # RUN conda run -n trex conda install -c conda-forge omegaconf=2.1.0 --freeze-installed --yes
# # RUN pip install omegaconf==2.0.0



# COPY gdrive_model_download.py /code/trex
# RUN python3 gdrive_model_download.py

# # COPY trex_inference.py /code/trex