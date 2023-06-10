FROM python:3-alpine
ARG emailUsername
ARG emailPassword
ARG adminPassword
# Create app directory
WORKDIR /app

# Install app dependencies
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

# Bundle app source
COPY . .

EXPOSE 80
CMD ["python","hotrocks.py"]


