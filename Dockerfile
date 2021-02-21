FROM python:3.8

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

EXPOSE 5050

COPY . /Homework_docker

CMD ["python", "Homework_docker/Homework6.py"]