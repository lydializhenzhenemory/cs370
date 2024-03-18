# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.7

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
RUN pip install Flask gunicorn
RUN pip install Flask
RUN pip install PyMySQL
RUN pip install openai
RUN pip install -U flask-cors
RUN pip install numpy
RUN pip install pandas
#RUN pip install click --upgrade
#RUN pip install os-sys

# Define an argument with a default value
ARG OPENAI_API_KEY=init
ARG HOST=init
ARG PORT=init
ARG DATABASE=init
ARG USER=init
ARG PASSWORD=init

# Set an environment variable using the ARG value
ENV OPENAI_API_KEY=$OPENAI_API_KEY
ENV HOST=$HOST
ENV PORT=$PORT
ENV DATABASE=$DATABASE
ENV USER=$USER
ENV PASSWORD=$PASSWORD

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
CMD exec gunicorn --bind :8080 --workers 1 --threads 8 --timeout 120 app:app
#CMD ["flask", "run", "--port=8080"]
EXPOSE 8080
