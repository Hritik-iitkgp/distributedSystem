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

