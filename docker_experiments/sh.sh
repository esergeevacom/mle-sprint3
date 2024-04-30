docker pull docker/whalesay
docker image ls
docker container run docker/whalesay
docker container run docker/whalesay cowsay ‘Hello Yandex’




docker build . --tag cow_image:0
docker run cow_image:0