FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /employeedb
WORKDIR /employeedb
ADD requirements.txt /employeedb/
RUN apt-get update && apt-get -y install vim 
RUN pip install -r requirements.txt
ADD . /employeedb/
EXPOSE 8000
CMD python manage.py runserver 0.0.0.0:8000
