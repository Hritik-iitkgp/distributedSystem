
# Scalable Database with Sharding

This repository contains the implementation of a distributed database system along with a load balancer using consistent hashing. The system is designed to efficiently handle read and write operations across multiple shards and server replicas.

## Table of Contents
- [Introduction](#introduction)
- [Tasks](#tasks)
  - [Server Management](#server-management)
  - [Load Balancer](#load-balancer)
  - [Performance Analysis](#performance-analysis)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Work Distribution](#work-distribution)

## Introduction

The distributed database system manages data entries in a sharded manner across multiple server containers. The load balancer ensures optimal distribution of read requests among shard replicas using consistent hashing, while write requests are coordinated to maintain data consistency.

## Tasks

### Server Management

- **Server Endpoints:** Implement endpoints to manage shards and replicas across server containers.

  - `/config (POST)`: Initialize shard tables in the server database after the container is loaded. Configure shards according to the request payload.
  - `/heartbeat (GET)`: Send heartbeat responses upon request to identify failures in the set of server containers.
  - `/copy (GET)`: Return data entries corresponding to one shard table in the server container to populate shard tables from replicas in case of failure.
  - `/read (POST)`: Read data entries from a shard in a particular server container based on a range of Stud ids.
  - `/write (POST)`: Write data entries in a shard in a particular server container along with Shard id and the current index for the shard.
  - `/update (PUT)`: Update a particular data entry in a shard in a particular server container.
  - `/del (DELETE)`: Delete a particular data entry in a shard in a particular server container.

### Load Balancer

- **Load Balancer Endpoints:** Develop a load balancer with consistent hashing to efficiently route read and write requests to appropriate shard replicas.

  - `/init (POST)`: Initialize the distributed database across different shards and replicas in the server containers. Provide configurations of shards and their placements.
  - `/status (GET)`: Send the database configurations upon request.
  - `/add (POST)`: Add new server instances in the load balancer to scale up with increasing client numbers in the system.
  - `/rm (DELETE)`: Remove server instances in the load balancer to scale down with decreasing client or system maintenance.
  - `/read (POST)`: Based on the consistent hashing algorithm, read data entries from the shard replicas across all server containers.
  - `/write (POST)`: Write data entries in the distributed database. Schedule each write to its corresponding shard replicas and ensure data consistency using mutex locks.
  - `/update (PUT)`: Update a particular data entry (based on Stud id) in the distributed database. Retrieve all the shard replicas and their corresponding server instances where the entry has to be updated.
  - `/del (DELETE)`: Delete a particular data entry (based on Stud id) in the distributed database. Retrieve all the shard replicas and their corresponding server instances where the entry has to be deleted.

### Performance Analysis

- **Task A-1:** Default Configuration Performance Analysis: Measure read and write speeds for 10,000 writes and 10,000 reads in the default configuration.
- **Task A-2:** Increase Shard Replicas Performance Analysis: Increase the number of shard replicas and measure the write speed for 10,000 writes and read speed for 10,000 reads.
- **Task A-3:** Increase Servers and Shards Performance Analysis: Increase the number of servers and shards, and measure the write speed for 10,000 writes and read speed for 10,000 reads.
- **Task A-4:** Endpoint Check and Container Dropping: Verify the correctness of all endpoints and simulate dropping a server container to observe the load balancer behavior.
- **Output for A-1**:
  - **Time taken for 10000 write requests:** 627.26 seconds 
  - ****Time taken for 10000 read requests:** 193.95 seconds
- **Output for A-2**:
  - **Time taken for 10000 write requests:** 985.15 seconds 
  - ****Time taken for 10000 read requests:** 190.65 seconds
- **Output for A-3**:
  - **Time taken for 10000 write requests:** 1279.14 seconds 
  - ****Time taken for 10000 read requests:** 191.15 seconds

## Setup Instructions

1. Clone this repository to your local machine.
2. Ensure you have the required dependencies installed (e.g., Python, Flask).
3. Follow the usage instructions provided below to run the distributed database system and load balancer.

## Usage

1. Run the load balancer and distributed database system using the provided scripts in the Makefile.
2. Access the endpoints specified in the main tasks to manage shards, replicas, and perform read and write operations.
3. Monitor the performance metrics and record the results for analysis as part of the performance analysis tasks through the client file.

## Team Members and Work Distribution

- **Server Management Implementation**:
  - **Server Configuration and Setup:** Hritik Jaiswal
  - **Heartbeat Functionality:** Hritik Jaiswal
  - **Data Copying for Failover:** Dasari Giridhar
  - **CRUD Operations (Read, Write, Update, Delete):** Hritik Jaiswal

- **Load Balancer Implementation**:
  - **Endpoint Initialization and Status:** Chandra Sekhara Azad
  - **Adding and Removing Servers:** Burra Nitish
  - **CRUD Operations (Read, Write, Update, Delete):** Dasari Giridhar
  - **Consistent Hashing Algorithm:** Chandra Sekhara Azad

- **Performance Analysis Tasks**:
  - **Task A-1: Default Configuration Performance Analysis:** CHandra Sekhara Azad
  - **Task A-2: Increase Shard Replicas Performance Analysis:** Burra Nitish
  - **Task A-3: Increase Servers and Shards Performance Analysis:** Burra Nitish
  - **Task A-4: Endpoint Check and Container Dropping:** Dasari Giridhar

# how to create the Docker container
- Dockerfile Contains configraution using which we can create docker images
-vTo Create an Docker Iamge go to the dictory where this Dockerfile is present from their run
docker build -t server1:01 .
-- after -t "We can "provide the name of docker image and version of it" after that . signifies that To Build the Docker Image required file is in the pwd
after creating image you see from
-bdocker image ls
- After that we can create mulitiple containers from the created docker images using
docker run -d --rm --name "server1" -e SERVER_ID=12345 -p 5001:5000 server1:01
here -d means run in background ,  --rm means this container will remove when we stop it,
--name "name of container" , -p binding port number so that it is accessible from outside the container ,  after that name of image
"As said we can create multiple contianer from the same image"

docker run -d --rm --name "server2" -e SERVER_ID=54654 -p 5002:5000 server1:01
docker run -d --rm --name "server3" -e SERVER_ID=78564 -p 5002:5000 server1:01

- "All This Conatiner when we run them they runs the server.py file"
that contians the python code for server responses like 
if we type from termminal
http://127.0.0.1:5000/home
it returns {
  "message": "Hello from Server: Unknown", ---> serverId rather then unknown from envirnoment varible
  "status": "successful"
}
and when we run http://127.0.0.1:5000/heartbeat from browser
it will return the 
nohting only 200 ok 





