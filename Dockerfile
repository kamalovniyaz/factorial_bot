FROM python:3.10
WORKDIR /app/
COPY . /app/
COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt
CMD ["python", "bot.py"]