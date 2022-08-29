FROM python:3.7.13-slim

# 
WORKDIR /code

# 
COPY ./requirements/server.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./app /code/app
COPY .env /code/

# 
CMD ["python", "app/main.py"]
