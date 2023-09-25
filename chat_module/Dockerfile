FROM python:3.11

# Port the app is running on
EXPOSE 7860

# Install dependencies
WORKDIR /base

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

# Copy all into image
COPY ./ ./

# Define environment variable

# primary command
CMD ["python", "gradio_launcher.py"]