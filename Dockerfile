FROM python:3.11

# Install dependencies and copy all into /base
WORKDIR /base
COPY ./requirements.txt ./
RUN pip install -r requirements.txt
COPY ./ ./

# Install unzip utility
RUN apt-get update && \
    apt-get install -y unzip && \
    rm -rf /var/lib/apt/lists/*

# Copy the zip file from the host machine to the container
# COPY ./data/chromadb.zip /tmp/chromadb.zip

# Unzip the file in the desired location
RUN unzip -o ./data/chromadb.zip -d ./ && rm ./data/chromadb.zip

# Define environment variable
ENV FLASK_APP=app/app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_DEBUG=True

# Expose the port the app runs on
EXPOSE 5000

CMD ["flask", "run"]