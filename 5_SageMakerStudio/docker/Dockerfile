FROM 763104351884.dkr.ecr.us-east-1.amazonaws.com/tensorflow-training:2.9.1-cpu-py39-ubuntu20.04-sagemaker

RUN pip install ipykernel && \
        python -m ipykernel install --sys-prefix

RUN wget https://sourceforge.net/projects/ta-lib/files/ta-lib/0.4.0/ta-lib-0.4.0-src.tar.gz && tar -xzf ta-lib-0.4.0-src.tar.gz && cd ta-lib/ && ./configure --prefix=/usr && make && make install && cd ../ && rm -rf ta-lib && rm ta-lib-0.4.0-src.tar.gz

# Install all of the packages
RUN pip install pandas
RUN pip install flask
RUN pip install gevent
RUN pip install backtrader
RUN pip install matplotlib==3.2.2
RUN pip install ta-lib
RUN pip install pyathena

RUN mkdir -p /opt/ml/input/data/training
RUN mkdir -p /opt/ml/input/config
RUN mkdir -p /opt/ml/model

# Env Variables
ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE
ENV PATH="/opt/program:${PATH}"

# Set up the program in the image
COPY model /opt/program
WORKDIR /opt/program