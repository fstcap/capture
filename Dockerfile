# Use the official image as a parent image.
FROM python:2.7

# Set the working directory.
WORKDIR /app

# Copy the file from your host to your current location.
COPY app.py /app/app.py

COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple some-package

CMD python app.py
