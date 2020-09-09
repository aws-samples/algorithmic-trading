FROM tensorflow/tensorflow:2.1.0rc2-py3

RUN apt-get -y update && apt-get install -y --no-install-recommends \
         wget \
         python3 \
         nginx \
         ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://sourceforge.net/projects/ta-lib/files/ta-lib/0.4.0/ta-lib-0.4.0-src.tar.gz && tar -xzf ta-lib-0.4.0-src.tar.gz && cd ta-lib/ && ./configure --prefix=/usr && make && make install && cd ../ && rm -rf ta-lib && rm ta-lib-0.4.0-src.tar.gz

# Install all of the packages
RUN wget https://bootstrap.pypa.io/get-pip.py && python get-pip.py
RUN pip install numpy
RUN pip install scipy
RUN pip install scikit-learn
RUN pip install pandas
RUN pip install flask
RUN pip install gevent
RUN pip install gunicorn
RUN pip install tensorflow==2.2.0
RUN pip install keras
RUN pip install backtrader
RUN pip install matplotlib==3.2.2
RUN pip install ta-lib
RUN pip install boto3

# Env Variables
ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE
ENV PATH="/opt/program:${PATH}"

# Set up the program in the image
COPY model /opt/program
WORKDIR /opt/program