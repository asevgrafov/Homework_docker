FROM python:3.8

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

EXPOSE 5050

COPY . /Homework6

CMD ["python", "Homework6/Homework6.py"]