---
title: "Using Docker with the CMS open data"
teaching: Self-guided
exercises: 40 min
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
using the [dedicated Mattermost channel](https://mattermost.web.cern.ch/cmsopeyyndatatheo/channels/town-square)
if we are missing something. 



## Using the proper image for CMS software

The first time you go to run Docker, the following command will fetch the docker image and 
put you into a ```bash``` shell in which you have access to a complete CMS software release that
is appropriate for interfacing with the 2011 and 2012 7 and 8 TeV datasets. It may take some time to 
download the full image, even as long as 20-30 minutes, depending on the speed of your internet
connection.

This command and some extra guidance can also be found on the 
[Open Data Portal introduction to Docker](http://opendata.cern.ch/docs/cms-guide-docker), however
the following command differs in that 
it allows for X11 forwarding That means that if you 
run a program from within Docker that pops up any windows or graphics, like ROOT, they will show up. 

Keep in mind, on some systems, the file/directory paths might be different,
so reach out to the organizers through the 
[dedicated Mattermost channel](https://mattermost.web.cern.ch/cmsopeyyndatatheo/channels/town-square)
if you have issues.


~~~
docker run -it --name myopendataproject --net=host --env="DISPLAY" --volume="$HOME/.Xauthority:/home/cmsusr/.Xauthority:rw"  cmsopendata/cmssw_5_3_32 /bin/bash
~~~
{: .language-bash}
~~~
Setting up CMSSW_5_3_32
CMSSW should now be available.
[21:53:43] cmsusr@docker-desktop ~/CMSSW_5_3_32/src $
~~~
{: .output}

> ## Possible issues on Windows
> If the docker command exits without giving you this output on WSL2 (Windows), 
> see [this post](https://opendata-forum.cern.ch/t/running-cms-opendata-containers-in-wsl2/30)
> in the CERN Open Data forum
{: .discussion}

It might be worth breaking down this command for the interested user. For a more complete
listing of options, see [the official Docker documentation](https://docs.docker.com/engine/reference/commandline/container_run/) on the ```run``` command. 

To start a CMSSW container instance and open it in a bash shell, one would need only type

~~~
docker run -it cmsopendata/cmssw_5_3_32 /bin/bash

~~~
{: .language-bash}

The ```-it``` option means to start the instance in interactive mode

Adding the following assigns a ```name``` to the instance so that we can refer back
to this environment and still access any files we created in there. You can, of course,
choose a different name than ```myopendataproject```! :)

~~~
... --name myopendataproject ...

~~~
{: .language-bash}
Adding the following gives us X11-forwarding, though this will not work with
Windows10 WSL2 Linux.

~~~
... --net=host --env="DISPLAY" --volume="$HOME/.Xauthority:/home/cmsusr/.Xauthority:rw"  ...

~~~
{: .language-bash}

When you're done, you can just type ```exit``` to leave the Docker environment. 

### Additional flags

Later on in this lesson we will show you two additional arguments to this command, both related to 
mounting local directories on your laptop/desktop 
such that it will be visible in the Docker container. 

One example we will show you will walk you through creating a local working directory for your 
analysis code. This means that you can edit your scripts or files
*locally* and exectute them in Docker. It will give you much greater flexibility in using whatever
backup or version control you are comfortable with. 

In a separate module we will show you how to mount the CERN-VM file system (CVMFS), giving you more access to CMS software and
calibration information. CVMFS will be discussed in greater detail in that module

As these flags are discussed, we will modify this primary `docker` command in those sections.

### Stopping docker instances

As you are learning how to use Docker, you may find yourself with multiple instances running. Or maybe
you started an instance with your favourite name with some set of flags and now you want to re-start
that same instance but with new flags. In that case, you will want to stop and remove the running
containers. 

To **stop** all containers you would type the following on your local machine. 

~~~
docker stop $(docker ps -aq)
~~~
{: .bash}

To **remove** all containers, you would type the following on your local machine. 

~~~
docker rm $(docker ps -aq)
~~~
{: .bash}

> ## Don't worry!
> Note that these commands *will not* remove the actual Docker *files* that you downloaded and may have taken
> quite some time to download! Whew!
>
{: .callout}

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
```start``` the instance, just by providing the name. 
You will also use ```-i``` for interactive rather than ```-it```. It will still come up as normal. 

Note also that you do not need the full ```cmsopendata/cmssw_5_3_32 ``` argument anymore. 

So to re-```start``` your container, just do the following
and you will still have X11-forwarding (on Linux and Mac) and the mounted disk volumes, assuming you 
ran the full command earlier. 

~~~
docker start -i myopendataproject
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
> For Windows users,
> open a specific CMS open data container ```docker run -it -P -p 5901:5901 -p 6080:6080 cmsopendata/cmssw_5_3_32_vnc:latest /bin/bash```.
> In the container, type ```start_vnc``` and choose a password.
> Open a browser window with the given URL (enter the password), and start ROOT.
> If the web browser doesn't work for you, alternative:
>  - Go to https://bintray.com/tigervnc/stable/tigervnc/1.10.0 and download vncviewer64-1.10.0.exe
>  - Run vncviewer64-1.10.0.exe, enter vnc server name: 127.0.0.1:5901, click connect, enter password
>
> For Mac and Linux users,
> open the CMS open data container with ```docker start...``` or ```docker run...``` 
> as instructed above and open ROOT, simply by typing ```root``` on the command line. 
>
> Do you see the ROOT splash screen pop up? 
> If not, check that you followed all the instructions
> above correctly or contact the facilitators. 
>
> To exit the ROOT interpreter type ```.q```.
>
> If you find that X11 forwarding is _not_ working, try typing the following
> before going starting your Docker container.
>
> ~~~
> xhost local:root
> ~~~
> {: .bash}
>
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

Suppose you have created your **myopendataproject** container *and* you did the challenge
question above to *Test persistence*. In your docker image, there should be a file now 
called ```test.tmp``` Run the following on your *local* machine and *not* in a docker environment. 
It should copy the file out and onto your local machine where you can inspect it. 

~~~
docker cp myopendataproject:/home/cmsusr/CMSSW_5_3_32/src/test.tmp .
~~~
{: .language-bash}

If you want to copy a file *into* a container instance, it works the way you might expect. 
Suppose you have a local file called ```localfile.tmp```. You can copy it into the same instance
as follows.

~~~
docker cp localfile.tmp myopendataproject:/home/cmsusr/CMSSW_5_3_32/src/
~~~
{: .language-bash}

## Mounting a local volume

Sometimes you may want to mount a filesystem from your local machine or some other remote system
so that your docker image can see it. Let's first see how this is done in a general way. 

The basic usage is 

~~~
docker run -v <path on host>:<path in container> <image>
~~~
{: .language-bash}

Where the `path on host` is the full path to the local file system/directory you want to 
make visible to docker. The `path in container` is where it will be mounted in your
Docker container. 

There are more options and if you want to read more, please visit the 
[official Docker documentation](https://docs.docker.com/storage/volumes/).

When working with the CMS open data, you will find yourself using this approach in at
least two ways:
* Having a local working directory for all your editing/version control, etc.
* Mounting the CVMFS file system (next module). 

Note that all your compiling and executing still has to be done *in the Docker container*! 
But having your source code also visible on your local laptop/desktop will make things easier for you. 

Let's try this. First, before you start up your Docker image, create a local directory
where you will be doing your code development. In the example below, I'm calling it
`cms_open_data_work` and it will live in my `$HOME` directory. You may choose a shorter directory name if you like. :)

> ## Local machine
> ~~~
> cd # This is to make sure I'm in my home directory
> mkdir cms_open_data_work
> ~~~
> {: .bash}
{: .challenge}

Then fire up your Docker container, adding the following
~~~
-v ${HOME}/cms_open_data_work:/home/cmsusr:shared
~~~
{: .bash}

Your full `docker` command would then look like this

> ## Local machine
> ~~~
> docker run -it --name myopendataproject --net=host --env="DISPLAY" --volume="$HOME/.Xauthority:/home/cmsusr/.Xauthority:rw" -v ${HOME}/cms_open_data_work:/home/cmsusr/cms_open_data_work:shared cmsopendata/cmssw_5_3_32 /bin/bash
> ~~~
> {: .language-bash}
{: .challenge}

~~~
Setting up CMSSW_5_3_32
CMSSW should now be available.
[21:53:43] cmsusr@docker-desktop ~/CMSSW_5_3_32/src $
~~~
{: .output}

When your Docker container starts up, it puts you in `/home/cmsusr/CMSSW_5_3_32/src`, but your new mounted directory is `/home/cmsusr/cms_open_data_work`. 
The easiest thing to do is to create a soft link to that directory from inside `/home/cmsusr/CMSSW_5_3_32/src` using `ln -s ...` as shown below,
and then do your work in that directory. 

> ## Warning!
> Sometimes the local volume is mounted in the Docker container as the wrong user/group. It should be
> `cmsusr` but sometimes is mounted as `cmsinst`. Note that in the following set of commands, we add a line
> to change the user/group with the `chown` command. 
>
> If this is an issue, you'll also need to do this in Docker for any new directories you check out
> on your local machine.
{: .callout}


> ## Docker container
> ~~~
> cd /home/cmsusr/CMSSW_5_3_32/src
> sudo chown -R cmsusr.cmsusr ~/cms_open_data_work/
> ln -s ~/cms_open_data_work/
> cd /home/cmsusr/CMSSW_5_3_32/src/cms_open_data_work/
> ~~~
> {: .language-bash}
{: .prereq}

Now, open a new terminal on your local machine (or simply exit out of your container) and check out one of the repositories
you'll be working with. If you are not familiar with git/Github, check out the [Git pre-exercises](https://swcarpentry.github.io/git-novice/). 

> ## Local machine
> ~~~
> cd ~/cms_open_data_work
> git clone https://github.com/katilp/AOD2NanoAODOutreachTool.git AOD2NanoAOD
> ~~~
> {: .language-bash}
{: .challenge}
~~~
Cloning into 'AOD2NanoAOD'...
remote: Enumerating objects: 60, done.
remote: Counting objects: 100% (60/60), done.
remote: Compressing objects: 100% (54/54), done.
remote: Total 343 (delta 29), reused 13 (delta 5), pack-reused 283
Receiving objects: 100% (343/343), 743.11 KiB | 461.00 KiB/s, done.
Resolving deltas: 100% (162/162), done.
~~~
{: .output}

Next, go back into your Docker container (either in your other window or by restarting *that same* container, and see if you can 
see this new directory that you checked out on your local machine. 

> ## Docker container
> ~~~
> cd /home/cmsusr/CMSSW_5_3_32/src/cms_open_data_work
> ls -l
> ~~~
> {: .language-bash}
{: .prereq}
~~~
total 4
drwxr-xr-x 8 cmsinst cmsinst 4096 Sep 26 20:48 AOD2NanoAOD
~~~
{: .output}

Voila! You now have a workflow where you can edit files *locally*, using whatever
tools are on your local machine, and then *exectute* them in the Docker 
environment. 

Let's try compiling and running this new code!
Note that to actually *compile* the code, we want to be in the
`/home/cmsusr/CMSSW_5_3_32/src` directory.

> ## Docker container
> ~~~
> cd /home/cmsusr/CMSSW_5_3_32/src
> sudo chown -R cmsusr.cmsusr cms_open_data_work/AOD2NanoAOD/
> scram b
> ~~~
> {: .language-bash}
{: .prereq}
~~~
Reading cached build data
>> Local Products Rules ..... started
>> Local Products Rules ..... done
>> Building CMSSW version CMSSW_5_3_32 ----
>> Entering Package cms_open_data_work/AOD2NanoAOD
>> Creating project symlinks
Entering library rule at cms_open_data_work/AOD2NanoAOD
>> Compiling edm plugin /home/cmsusr/CMSSW_5_3_32/src/cms_open_data_work/AOD2NanoAOD/src/AOD2NanoAOD.cc 
>> Building edm plugin tmp/slc6_amd64_gcc472/src/cms_open_data_work/AOD2NanoAOD/src/cms_open_data_workAOD2NanoAOD/libcms_open_data_workAOD2NanoAOD.so
Leaving library rule at cms_open_data_work/AOD2NanoAOD
@@@@ Running edmWriteConfigs for cms_open_data_workAOD2NanoAOD
--- Registered EDM Plugin: cms_open_data_workAOD2NanoAOD
>> Leaving Package cms_open_data_work/AOD2NanoAOD
>> Package cms_open_data_work/AOD2NanoAOD built
>> Subsystem cms_open_data_work built
>> Local Products Rules ..... started
>> Local Products Rules ..... done
gmake[1]: Entering directory `/home/cmsusr/CMSSW_5_3_32'
>> Creating project symlinks
>> Done python_symlink
>> Compiling python modules cfipython/slc6_amd64_gcc472
>> Compiling python modules python
>> Compiling python modules src/cms_open_data_work/AOD2NanoAOD/python
>> All python modules compiled
@@@@ Refreshing Plugins:edmPluginRefresh
>> Pluging of all type refreshed.
>> Done generating edm plugin poisoned information
gmake[1]: Leaving directory `/home/cmsusr/CMSSW_5_3_32'
~~~
{: .output}

And now we can run it! The following command may take anywhere from 10-20 minutes to run.

> ## Docker container
> ~~~
> cd /home/cmsusr/CMSSW_5_3_32/src/cms_open_data_work/AOD2NanoAOD/
> cmsRun configs/data_cfg.py
> ~~~
> {: .bash}
{: .prereq}
~~~
200926 22:12:20 802 secgsi_InitProxy: cannot access private key file: /home/cmsusr/.globus/userkey.pem
26-Sep-2020 22:46:14 CEST  Initiating request to open file root://eospublic.cern.ch//eos/opendata/cms/Run2012B/TauPlusX/AOD/22Jan2013-v1/20000/0040CF04-8E74-E211-AD0C-00266CFFA344.root
26-Sep-2020 22:46:17 CEST  Successfully opened file root://eospublic.cern.ch//eos/opendata/cms/Run2012B/TauPlusX/AOD/22Jan2013-v1/20000/0040CF04-8E74-E211-AD0C-00266CFFA344.root
26-Sep-2020 22:51:14 CEST  Closed file root://eospublic.cern.ch//eos/opendata/cms/Run2012B/TauPlusX/AOD/22Jan2013-v1/20000/0040CF04-8E74-E211-AD0C-00266CFFA344.root

=============================================

MessageLogger Summary

 type     category        sev    module        subroutine        count    total
 ---- -------------------- -- ---------------- ----------------  -----    -----
    1 fileAction           -s file_close                             1        1
    2 fileAction           -s file_open                              2        2

 type    category    Examples: run/evt        run/evt          run/evt
 ---- -------------------- ---------------- ---------------- ----------------
    1 fileAction           PostEndRun
    2 fileAction           pre-events       pre-events

Severity    # Occurrences   Total Occurrences
--------    -------------   -----------------
System                  3                   3
~~~
{: .output}




{% include links.md %}

