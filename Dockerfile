FROM python:3.11

# install sentence_transformers early for caching
RUN pip install sentence_transformers

# Port the app is running on
EXPOSE 5000

# Install dependencies
WORKDIR /base

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

# Removing watchdog package since flask hot reloading
# only works with stat reload type on my machine
RUN pip uninstall -y watchdog

# Install unzip utility
RUN apt-get update && \
    apt-get install -y unzip && \
    rm -rf /var/lib/apt/lists/*

# Copy all into image
COPY ./ ./

# Unzip the file in the desired location
RUN unzip -o ./data/chromadb.zip -d ./ && rm ./data/chromadb.zip

# Define environment variable
ENV FLASK_APP=./app/app.py
ENV FLASK_DEBUG=True

CMD ["flask", "run", "--host", "0.0.0.0"]