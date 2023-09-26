FROM python:3.11

# Port the app is running on
EXPOSE 5000

# Install dependencies
WORKDIR /base

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

# Removing watchdog package since flask hot reloading
# only works with stat reload type on my machine
RUN pip uninstall -y watchdog

# Copy all into image
COPY ./ ./

# Define environment variable
ENV FLASK_APP=./app/app.py
ENV FLASK_DEBUG=True

CMD ["flask", "run", "--host", "0.0.0.0"]