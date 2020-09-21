---
title: "Setting up CVMFS for use with the luminosity tools"
teaching: 0
exercises: 0
questions:
- "How do I access some CMS-specific software"
objectives:
- "Install the CVMFS on your local machine"
- "Learn to mount that volume in your container"
- "Use the CVMFS to access and run tools to calculate the luminosity for specific run periods"
keypoints:
- "Installing the CVMFS can make some parts of the analysis much easier"
- "Care must be given though to setting up your environment properly."
---

At some point you may want to calculate the luminosity or study trigger 
effects for the data you are analyzing. CMS uses a tool called `brilcalc` 
but it is not included in the Docker image.

To get around this, we mount drives at CERN in the Docker container when you fire it up
so that you can call this and perhaps other tools. 

To learn more about `brilcalc` you can read the 
[CERN Open Data Portal documentation](http://opendata.cern.ch/docs/cms-guide-luminosity-calculation).
This lesson however is just to help you test that you can access this tool. 

## Installing CVMFS locally

From the [CVMFS documentation](https://cvmfs.readthedocs.io/en/stable/index.html)

*The CernVM-File System (CernVM-FS) provides a scalable, reliable and low- maintenance software distribution service. It was developed to assist High Energy Physics (HEP) collaborations to deploy software on the worldwide- distributed computing infrastructure used to run data processing applications. CernVM-FS is implemented as a POSIX read-only file system in user space (a FUSE module). Files and directories are hosted on standard web servers and mounted in the universal namespace `/cvmfs`.*

In the following sections, we'll direct you to the appropriate pages to download
and install CVMFS locally. 
***This should be done on your local machine and not in the container.***

Let's walk through these steps.

### Get CVMFS

Follow the [installation instructions](https://cvmfs.readthedocs.io/en/stable/cpt-quickstart.html#getting-the-software) 
to download the software for your particular OS. 

### Setup CVMFS

Next, you'll want to set things up on your local machine. Follow
[these instructions](https://cvmfs.readthedocs.io/en/stable/cpt-quickstart.html#setting-up-the-software) carefully
for your system. 

One part of the setup which can be confusing is the content of the file `/etc/cvmfs/default.local`. 
The following lines should work, if they are the sole content of the file.

~~~
CVMFS_REPOSITORIES=cms.cern.ch,cms-opendata-conddb.cern.ch,cms-bril.cern.ch
CVMFS_HTTP_PROXY=DIRECT
CVMFS_CLIENT_PROFILE=single
~~~
{: .code}

> ## Check the installation
>
> Make sure you [verify the installation](https://cvmfs.readthedocs.io/en/stable/cpt-quickstart.html#verify-the-file-system).
> Check that link for the latest commands, but usually this involves running
> 
> ~~~
> cvmfs_config probe
> ~~~
> {: .bash}
> or
> ~~~
> sudo systemctl restart autofs
> ~~~
> {: .bash}
{: .callout}

> ## Possible issues
> 
> For some systems, you may run into some issues.
>
> On WSL2 Ubuntu, after the installation, on each session, one has to run the following
> ~~~
> sudo /usr/sbin/automount --pid-file /var/run/autofs.pid
> cvmfs_config probe
> ~~~
> {: .bash}
{: .discussion}

## Set up your Docker container

In the previous instructions on starting up your Docker container, we included the commands
to start your container with CVMFS mounted. 

~~~
... --volume "/cvmfs:/cvmfs:shared" ...
~~~
{: .bash}

This makes sure the container can see this CVMFS file system. 

If you ran all the correct commands in the previous exercise, you can now start the 
container by name

~~~
docker start -i myopendataproject
~~~
{: .bash}

Or, if you wanted to start a brand new, fresh container with the CVMFS file system mounted, 
you can run

~~~
docker run -it --name mycvmfs --volume "/cvmfs:/cvmfs:shared" cmsopendata/cmssw_5_3_32 /bin/bash
~~~
{: .bash}


Once you have started the container
and are in the CMSSW 5.3.32 environment, run the following commands to set some local environment
variables and then install `brilcalc` using the python `pip` command.

~~~
export PATH=$HOME/.local/bin:/cvmfs/cms-bril.cern.ch/brilconda/bin:$PATH

pip install --user brilws
~~~
{: .bash}

Each time you login, you will have to re-run that `export` command, even if you have
already installed `brilws` in the container. 

## Test it out and run brilcalc

If everything worked, you should be able to run `brilcalc` to check its version and 
to get the luminosity for a sample run. 

~~~
brilcalc --version

brilcalc lumi -c web -r 160431
~~~
{: .bash}



{% include links.md %}

