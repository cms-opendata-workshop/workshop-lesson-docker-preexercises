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

At some point you may want to calculate the luminosity for the data you are analyzing. 
CMS uses a tool called `brilcalc` but it is not included in the Docker image. Similarly, there
are some tools needed to calculate trigger effects/efficiencies that are also not included
in the Docker image. 

To get around this, we mount drives at CERN in the Docker container when you fire it up
so that you can call this and perhaps other tools. 

To learn more about `brilcalc` you can read the 
[CERN Open Data Portal documentation](http://opendata.cern.ch/docs/cms-guide-luminosity-calculation).
This lesson however is just to help you test that you can access this tool. 

## Installing CVMFS locally

From the [CVMFS documentation](https://cvmfs.readthedocs.io/en/stable/index.html)

*The CernVM-File System (CernVM-FS) provides a scalable, reliable and low- maintenance software distribution service. It was developed to assist High Energy Physics (HEP) collaborations to deploy software on the worldwide- distributed computing infrastructure used to run data processing applications. CernVM-FS is implemented as a POSIX read-only file system in user space (a FUSE module). Files and directories are hosted on standard web servers and mounted in the universal namespace `/cvmfs`.*

You will want to go to the [installation instructions](https://cvmfs.readthedocs.io/en/stable/cpt-quickstart.html#) and
install this locally for your operating system. 

***This should be done on your local machine and not in the container.***

Pay particular attention to the setup procedure. You may have to create/edit [some important config files](https://cvmfs.readthedocs.io/en/stable/cpt-quickstart.html#create-default-local). 

> ## Check the installation
>
> Make sure you [verify the installation](https://cvmfs.readthedocs.io/en/stable/cpt-quickstart.html#verify-the-file-system).
>
{: .callout}

## Set up your Docker container

In the previous instructions on starting up your Docker container, the following arguments were used

~~~
... --volume "/cvmfs:/cvmfs:shared" ...
~~~
{: .bash}

This makes sure the container can see this CVMFS file system. Once you have started the container
and are in the CMSSW 5.3.32 environment, run the following commands to set some local environment
variables and then install `brilcalc` using the python `pip` command.

~~~
export PATH=$HOME/.local/bin:/cvmfs/cms-bril.cern.ch/brilconda/bin:$PATH

pip install --user brilws
~~~
{: .bash}

## Test it out and run brilcalc

If everything worked, you should be able to run `brilcalc` to check its version and 
to get the luminosity for a sample run. 

~~~
brilcalc --version

brilcalc lumi -c web -r 160431
~~~
{: .bash}



{% include links.md %}

