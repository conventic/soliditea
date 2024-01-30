# Use an Ubuntu base image
FROM python:3.10

# Update and install necessary tools, libraries, and compilers
RUN apt-get update

# Set the working directory to the project directory
WORKDIR /soliditea
