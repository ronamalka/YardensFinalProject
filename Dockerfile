FROM python:3-alpine

WORKDIR /src

COPY src/requirements.txt .
RUN pip3 install -r requirements.txt

COPY src/ .

CMD [ "python3", "./SensoundMainApp.py"]