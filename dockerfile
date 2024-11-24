FROM python:3.10

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY entrypoint.sh entrypoint.sh

COPY . /app/

ENTRYPOINT [ "/app/entrypoint.sh" ]

EXPOSE 8000

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]