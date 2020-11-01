# set base image (host OS)
FROM python:3.8

# set the working directory in the container
WORKDIR /code

#CHeck where it is
RUN ls

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY controller/ .
COPY repositories/ .
COPY utils/ .
COPY service/ .
COPY app.py .
COPY dummydata.py .

#Check if files were transfered
RUN ls

#Expose port 5000
EXPOSE 5000
# command to run on container start
CMD [ "python", "./app.py" ]
