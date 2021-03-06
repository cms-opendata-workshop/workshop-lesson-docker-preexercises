---
title: "Setting up CVMFS"
teaching: 15
exercises: 30
questions:
- "How do I access some CMS-specific software"
objectives:
- "Install the CVMFS on *either* your local machine *or* inside the Docker container"
- "Use CVMFS to access and run tools used to calculate the luminosity for specific run periods"
keypoints:
- "Installing CVMFS can make some parts of the analysis much easier"
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

# Installing CVMSFS

There are two ways to install CVMFS: 
* Install CVMFS locally and then mount in the Docker container
* Install CMVFS directly in the Docker container

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
> ~~~
> sudo cvmfs_config setup
> ~~~
> {: .bash}
> and then
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
>
> You may even find that even *during* a session, you need to re-run
> ~~~
> cvmfs_config probe
> ~~~
> {: .bash}
> on your host machine, even on Linux or Mac.
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

If you want to simply build upon everything you have done already, your full Docker command
would now look like

~~~
docker run -it --name myopendataproject --net=host --env="DISPLAY" --volume="$HOME/.Xauthority:/home/cmsusr/.Xauthority:rw" -v ${HOME}/cms_open_data_work:/home/cmsusr/cms_open_data_work:shared --volume "/cvmfs:/cvmfs:shared" cmsopendata/cmssw_5_3_32 /bin/bash
~~~
{: .bash}


## Install CVMFS directly in the Docker container 

We'll be following the offical CVMFS documentation [here](https://cvmfs.readthedocs.io/en/stable/cpt-quickstart.html) 
and [here](https://cvmfs.readthedocs.io/en/stable/cpt-configure.html) but with specific instructions
for the CMSSW Docker image. 

You'll want to launch Docker with a new `--privileged` flag that will make it easier to install
new packages. If we are using the full command from the previous module, it would now look like
this

~~~
docker run --privileged -it --name myopendataproject --net=host --env="DISPLAY" --volume="$HOME/.Xauthority:/home/cmsusr/.Xauthority:rw" -v ${HOME}/cms_open_data_work:/home/cmsusr/cms_open_data_work:shared cmsopendata/cmssw_5_3_32 /bin/bash
~~~
{: .bash}

The following command are all done *in the Docker container*. 

Install the necessary packages using `yum`. This could take up to 30 minutes to install these packages. 

At some point, the installation process will prompt you for your approval,
`Is this ok [y/N]:`. You can enter `y`.

~~~
sudo yum install https://ecsft.cern.ch/dist/cvmfs/cvmfs-release/cvmfs-release-latest.noarch.rpm
sudo yum install -y cvmfs
~~~
{:.bash}
~~~
Loaded plugins: changelog, kernel-module, ovl, protectbase, tsflags, versionlock
Setting up Install Process
cvmfs-release-latest.noarch.rpm                                                                                                          | 5.5 kB     00:00
Examining /var/tmp/yum-root-NokpI5/cvmfs-release-latest.noarch.rpm: cvmfs-release-2-6.noarch
Marking /var/tmp/yum-root-NokpI5/cvmfs-release-latest.noarch.rpm to be installed
EGI-trustanchors                                                                                                                         | 2.5 kB     00:00
EGI-trustanchors/primary_db                                                                                                              |  56 kB     00:00
.
<more output follows>
.
~~~
{: .output}

Next you'll need to configure `autofs`, which [handles mounting of filesystems](https://www.kernel.org/doc/html/latest/filesystems/autofs.html).

~~~
sudo cvmfs_config setup
~~~
{: .bash}

Edit the `/etc/cvmfs/default.local` file

~~~
sudo vi /etc/cvmfs/default.local
~~~
{: .bash}

and add these lines:

```
CVMFS_REPOSITORIES=cms.cern.ch,cms-opendata-conddb.cern.ch,cms-bril.cern.ch
CVMFS_HTTP_PROXY=DIRECT
CVMFS_CLIENT_PROFILE=single
```

Restart `autofs`

~~~
sudo service autofs restart
~~~
{: .bash}

Verify the file system

~~~
cvmfs_config probe
~~~
{: .bash}

> ## Heads-up!
> You will need to repeat the last two commands every time you restart the container.
>
{: .callout}


# Test it out and run brilcalc

Once you are in the container
and are in the CMSSW 5.3.32 environment, and have CVMFS working through either of
the above methods, you can then run the following commands to set some local environment
variables and then install `brilcalc` using the python `pip` command.

~~~
export PATH=$HOME/.local/bin:/cvmfs/cms-bril.cern.ch/brilconda/bin:$PATH

pip install --user brilws
~~~
{: .bash}

Each time you login, you will have to re-run that `export` command, even if you have
already installed `brilws` in the container. 


If everything worked, you should be able to run `brilcalc` to check its version and 
to get the luminosity for a sample run. 

_Note that the first time you run the `brilcalc` commands, it can take up to 7 minutes to run!_

~~~
brilcalc --version

brilcalc lumi -c web -r 160431
~~~
{: .bash}

It should be noted that during the workshop, we will have an entire exercise dedicated to using this tool
to calculate the luminosity for your datasets. 


{% include links.md %}

