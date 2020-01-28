FROM osteffmann/algo-trading:latest

# Env Variables
ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE
ENV PATH="/opt/program:${PATH}"

# Set up the program in the image
COPY model /opt/program
WORKDIR /opt/program