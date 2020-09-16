---
title: "Using Docker with the CMS open data"
teaching: Self-guided
exercises: 60 min
questions:
- "How do I use docker to effectively interface with the CMS open data?"
objectives:
- "Download (fetch) the correct docker image "
- "Fire up docker in the most useful way for CMS Open Data analysis"
- "Use docker in a persistent way"
- "Copy data out of the docker environment"
- "Access Github repositories from within a docker environment"
keypoints:
- "Docker is easy to use but there are number of options you have to be careful with in order to use it effectively with the CMS open data"

---

## Overview

This exercise will walk you through setting up and familiarizing yourself with Docker, so that
you can effectively use it to interface with the CMS open data. It is *not* meant to completely 
cover containers and everything you can do with Docker, but reach out to the organizers
if we are missing something. 


## Install Docker

There are many resources on the web to help you install Docker. You can start
with [the official Docker site](https://docs.docker.com/get-docker/) or whatever you find
that works for you. 

Once you have installed Docker, we again recommend you follow the 
[official Docker getting started/hello-world example](https://docs.docker.com/get-started/).
If you can run this, you should be good with everything that follows!


## Using the proper image for CMS software

The first time you go to run Docker, the following command will fetch the docker image and 
put you into a ```bash``` shell in which you have access to a complete CMS software release that
is appropriate for interfacing with the 2011 and 2012 7 and 8 TeV datasets. It may take some time to 
download the full image, even as long as 20-30 minutes, depending on the speed of your internet
connection.

This command and some extra guidance can also be found on the 
[Open Data Portal introduction to Docker](http://opendata.cern.ch/docs/cms-guide-docker), however
the following command differs in two ways:
* It allows for X11 forwarding That means that if you 
run a program from within Docker that pops up any windows or graphics, like ROOT, they will show up. 
* It allows you to access ssh keys from inside the docker container. This means that 
if you are [using ssh keys](https://docs.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh) to connect to Github and have stored those keys locally, you will have
an easier time cloning repositories.

~~~
docker run -it --name MYOPENDATAPROJECT -v ${HOME}/.ssh:/home/cmsusr/.ssh --net=host --env="DISPLAY" --volume="$HOME/.Xauthority:/root/.Xauthority:rw" cmsopendata/cmssw_5_3_32 /bin/bash

~~~
{: .language-bash}

It might be worth breaking down this command for the interested user. For a more complete
listing of options, see [the official Docker documentation](https://docs.docker.com/engine/reference/commandline/container_run/) on the ```run``` command. 

To start a CMSSW container instance and open it in a bash shell, one would need only type

~~~
docker run -it cmsopendata/cmssw_5_3_32 /bin/bash

~~~
{: .language-bash}

The ```-it``` option means to start the instance in *interactive* mode and using a *pseudo-TTY*
display. 

Adding the following assigns a ```name``` to the instance so that we can refer back
to this environment and still access any files we created in there. You can, of course,
choose a different name than ```MYOPENDATAPROJECT```! :)

~~~
... --name MYOPENDATAPROJECT ...

~~~
{: .language-bash}
Adding the following gives us X11-forwarding.

~~~
... --net=host --env="DISPLAY" --volume="$HOME/.Xauthority:/root/.Xauthority:rw" ...

~~~
{: .language-bash}

And the following mounts our local ```.ssh``` directory as a local *volume*. 

~~~
... -v ${HOME}/.ssh:/home/cmsusr/.ssh  ...

~~~
{: .language-bash}

In the lesson on access luminosity information, we explain how to mount the
*CERN-VM fileystem* which will add some additional flags. However, if 
you're not planning on accessing those helper functions, the above should be 
enough.

When you're done, you can just type ```exit``` to leave the Docker environment. 


## Using Docker repeatedly

The next time you want to run Docker, it will not need to download any significant data 
so it should open in seconds. You could choose to run the same command as before and while that would
work and quickly put you into a Docker environment, 
there are some issues with this. Most significantly, any files that you make or any code that you write in that
environment will not be there! Instead of the above command, we want to run Docker in a *persistent* way so that
we keep going into the same working area with all our files and code saved each time. 

There are two ways to do this: by giving your container instance a *name* or by making sure you
reference the *container id*. The former approach is probably easier and preferred, but we discuss 
both below. 

### Start docker by name

The easiest way to start a docker instance that you want to return to is using the ```--name```
option, as shown in the first example. If you've named your instance similarly, you can
```start``` the instance, just by providing the name. You will also use ```-i``` for interactive
rather than ```-it``` for the *pseudo-TTY*  display. It will still come up as normal. 

Note also that you do not need the full ```cmsopendata/cmssw_5_3_32 ``` argument anymore. 

So to re-```start``` your container, just do 

~~~
docker start -i MYOPENDATAPROJECT --volume "/cvmfs:/cvmfs:shared"  -v ${HOME}/.ssh:/home/cmsusr/.ssh --net=host --env="DISPLAY" --volume="$HOME/.Xauthority:/root/.Xauthority:rw" /bin/bash
~~~
{: .language-bash}

If you ever just wanted to open the image quickly and not worry about X11-forwarding or mounting 
specific disk volumes, you could just run

~~~
docker start -i MYOPENDATAPROJECT
~~~
{: .language-bash}


### Start/Attach to a particular process

If you did not name your container instance but still want to return to a very specifc
environment, you will need to ```start``` and then ```attach``` to the exact same Docker instance as before. 
First of all, you want to see what other Docker processes we have running. To do this, run the following
command
~~~
docker ps -a
~~~
{: .language-bash}

You'll see a list of docker processes that may look something like the following (the exact output
        will vary from user to user).

~~~
CONTAINER ID        IMAGE                      COMMAND                  CREATED             STATUS                      PORTS               NAMES
4f323c317b90        hello-world                "/hello"                 3 minutes ago       Exited (0) 3 minutes ago                        modest_jang
7719a7d74190        cmsopendata/cmssw_5_3_32   "/opt/cms/entrypoint…"   9 minutes ago       Exited (0) 2 minutes ago                        happy_greider
8939ade0bfac        cmsopendata/cmssw_5_3_32   "/opt/cms/entrypoint…"   16 hours ago        Exited (128) 16 hours ago                       hungry_bhaskara
e914cef3c45a        cmsopendata/cmssw_5_3_32   "/opt/cms/entrypoint…"   6 days ago          Exited (1) 9 minutes ago                        beautiful_tereshkova
b3a888c059f7        cmsopendata/cmssw_5_3_32   "/opt/cms/entrypoint…"   13 days ago         Exited (0) 13 days ago                          affectionate_ardinghelli
~~~
{: .output}

You'll want to attach using the ```CONTAINER ID```. In the above example, I know that I've been using the most 
recent container instance for cmsopendata, ```7719a7d74190```. So to reattach, I do

~~~
docker start 7719a7d74190
docker attach 7719a7d74190
~~~
{: .language-bash}

Voila! You should be back in the same container. 


> ## CHALLENGE! Test X11 forwarding
>
> Go into the Docker environment and open ROOT, simply by typing ```root``` on the command line. 
> Do you see the ROOT splash screen pop up? 
> If not, check that you followed all the instructions
> above correctly or contact the facilitators. 
>
> To exit the ROOT interpreter type ```.q```.
{: .challenge}

> ## CHALLENGE! Test persistence
>
> Go into the Docker environment and create a test file using some
> simple shell commands. Type the following exactly as you see it.
> It will dump some text into a file and then print the contents
> of the file to the screen
> ~~~
> echo "I am still here" > test.tmp
> cat test.tmp
> 
> ~~~
> {: .language-bash}
>
> After you've done this, exit out of the container and try to attach to the same
> instance. If you did it correctly, you should be able to list the contents
> of the directory with ```ls -l``` and see your file from before!
> If not, check that you followed all the instructions
> above correctly or contact the facilitators. 
{: .challenge}

## Copy file(s) into or out of a container

Sometimes you will want to copy a file directly into or out of a container. Let's start with copying
a file *out*. 

Suppose you have created your **MYOPENDATAPROJECT** container *and* you did the challenge
question above to *Test persistence*. In your docker image, there should be a file now 
called ```test.tmp``` Run the following on your *local* machine and *not* in a docker environment. 
It should copy the file out and onto your local machine where you can inspect it. 

~~~
docker cp MYOPENDATAPROJECT:/home/cmsusr/CMSSW_5_3_32/src/test.tmp .
~~~
{: .language-bash}

If you want to copy a file *into* a container instance, it works the way you might expect. 
Suppose you have a local file called ```localfile.tmp```. You can copy it into the same instance
as follows.

~~~
docker cp localfile.tmp MYOPENDATAPROJECT:/home/cmsusr/CMSSW_5_3_32/src/
~~~
{: .language-bash}



## Checkout a git repository 

We assume that you have configured your *local* machine to be able to access
Github and have setup your machine to use the [ssh keys](https://docs.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh). If you have, then the above instructions are mounting your local
drive such that your Docker containers can access those ssh keys. 

I've prepared a minimal github repository for you to clone for testing. To clone it, 
you will clone the directory slightly differently than the default procedure provided
by Github. The way you will want to clone a repository is as follows. 

~~~
git clone git://github.com/mattbellis/cern-opendata-sandbox
~~~
{: .language-bash}

Normally one would run the following command (and is what Github shows you usually from the 
webpage), but this does not work in the containers. 
**Running the following command will probaly fail and give you errors about
access rights.**
~~~
git clone git@github.com:mattbellis/cern-opendata-sandbox.git
~~~
{: .language-bash}

> ## Challenge!
> 
> Check out one of your own Github repositories to a container. Make some 
> minor changes to one of the files and push it back to Github, just to verify
> that you can do this. This will make it much easier for you to save your
> work when you are developing your analysis pipeline.
>
>
{: .challenge}

{% include links.md %}

