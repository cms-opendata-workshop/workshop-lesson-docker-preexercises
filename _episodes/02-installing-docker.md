---
title: "Installing Docker"
teaching: 5
exercises: 15
questions:
- "What equipment do I need?"
- "How do I install Docker?"
objectives:
- "Install Docker on your machine"
keypoints:
- "For up-to-date details for installing Docker, the official documentation is the best bet."
- "Make sure you were able to download and run Docker's `hello-world` example."
---

Installing Docker is relatively straightforward, particularly because of the excellent
documentation they provide. Still you want to set aside some time to do it properly and
test it out. 

## Installing

Go to the offical [Docker site and their installation instructions](https://docs.docker.com/get-docker/)
to install Docker for your operating system.

We see no need to go beyond the documentation they provide so we leave it up to you to follow
their installation procedure. 

## Testing

As you walk through their documentation, you will eventually come to a point where you will 
run a very simple test, usually involving their `hello-world` container. 

You can find their documentation for this step [here](https://docs.docker.com/get-started/). 

Testing their code can be summed up by the ability to run (without generating any errors) the following
commands.

~~~
docker --version
~~~
{: .bash}

~~~
docker run hello-world
~~~
{: .bash}


{% include links.md %}

