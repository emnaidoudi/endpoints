# Instructions copied from - https://hub.docker.com/_/python/
# the base image
FROM python:3-onbuild

# tell the port number the container should expose
# specify the port number the container should expose
EXPOSE 5000

# run the application
#The primary purpose of CMD is to tell the container which command it should run when it is started.
CMD ["python", "./app.py"]

RUN pip install -r requirements.txt
