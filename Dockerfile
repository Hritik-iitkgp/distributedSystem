FROM python:3.8


WORKDIR server/

COPY . .


RUN pip3 install flask


CMD ["python3","server.py"]
