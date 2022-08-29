FROM python:3.7.13-slim

# 
WORKDIR /code

# 
COPY ./requirements/server.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./app /code/app

# 
CMD ["python", "app/main.py"]
