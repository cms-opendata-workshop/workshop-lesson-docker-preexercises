---
title: "Test and validate"
teaching: 10
exercises: 30
questions:
- "What is in the CMS Docker image?"
- "How do I test and validate my Docker container?"
objectives:
- "Learn about the details of the CMS Docker container"
- "Test and validate the CMS Docker image by running a CMSSW job."
keypoints:
- "The CMS Docker image contains all the required ingredients to start analyzing CMS open data."
- "In order to test and validate the Docker container you can run a simple CMSSW job."  
---
> ## Helpline
>
> Remember that we are always available to help.  Our [Mattermost](https://mattermost.web.cern.ch/cmsopendatatheo/channels/docker-pre-exercises) channel is open.
{: .callout}

## Know your Docker image

The Docker container we just installed provides CMS computing environment to be used with the 2011 and 2012 CMS open data. The Docker container uses Scientific Linux CERN.  As it was mentioned before, it comes equipped with the [ROOT](http://root.cern.ch/) framework and [CMSSW](http://cms-sw.github.io/).

An important feature of the image is the availability of the [CernVM File System](https://cernvm.cern.ch/fs/).  
Thanks to the cvmfs client installed, the Docker instance gets the CMS software (CMSSW) 
from the shared `/cvmfs/cms.cern.ch` area (physically at CERN but mounted locally) 
and the jobs, running on the CMS open data Docker image, read the conditions data 
from `/cvmfs/cms-opendata-conddb.cern.ch`. Access to the data is through [XRootD](https://xrootd.slac.stanford.edu/).


## Run a simple *demo* for testing and validating

The validation procedure tests that the CMS environment is installed and operational on your Docker container, and that you have access to the CMS Open Data files.  It also access the conditions data from the shared cvmfs area and caches them.  This last action will save us time during the workshop.  These steps also give you a quick introduction to the CMS environment.

Run the following command to create the CMS runtime variables:

~~~
cmsenv
~~~
{: .language-bash}

Create a working directory for the demo analyzer, change to that directory and create a *skeleton* for the analyzer:

~~~
mkdir Demo
cd Demo
mkedanlzr DemoAnalyzer
~~~
{: .language-bash}

Come back to the main `src` area:

~~~
cd ../
~~~
{: .language-bash}

Compile the code:

~~~
scram b
~~~
{: .language-bash}

You can safely ignore the warning.

> **IMPORTANT NOTE**: Depending on your system, there could be some issues with the shared clipboard between the host machine and the Docker container.  
> This means that it is possible that you cannot copy the instrucitons 
> in this episode directly into your Docker session.  
>
> One thing you can try is `Shift+Ctrl+V` when pasting into your Docker terminal,
> rather than `Ctrl-V`. That sometimes will work.
>
> The quickest workaround might be using `ssh` and/or `scp` commands to copy the required files to some other machine that you have access to, from the Docker container as well as from the host machine.  For instance, if you had access to an `lxplus` computer at cern, you could copy a certain file from the Docker container to the lxplus computer.  On the Docker container you could do:
>
> ~~~
> scp myfile.txt myusername@lxplus.cern.ch:.
> ~~~
> {: .language-bash}
>
> to copy a hypothetical file `myfile.txt` to lxplus, and then on the host
>
> ~~~
> scp myusername@lxplus.cern.ch:myfile.txt .
> ~~~
> {: .language-bash}
>
> to copy the same file back to your host machine.  Then you can edit the file locally and reverse the process to get it back to your Docker container.
>
> It could also be possible to have direct access from the host to the Docker container.  This [youtube tutorial](https://www.youtube.com/watch?v=ErzhbUusgdI) might be of help for that option.
{: .testimonial}

Before launching the job, let's modify the configuration file (do not worry, you will learn about all this stuff in a different [lesson](https://cms-opendata-workshop.github.io/workshop-lesson-cmssw/)) so it is able access a CMS open data file and cache the conditions data.  As it was mentioned, this will save us time later.

Open the `demoanalyzer_cfg.py` file using the `vi` editor ([here](https://www.thegeekdiary.com/basic-vi-commands-cheat-sheet/) you can find a good cheatsheet for that editor). 

~~~
vi Demo/DemoAnalyzer/demoanalyzer_cfg.py
~~~
{: .language-bash}

Replace `file:myfile.root` with `root://eospublic.cern.ch//eos/opendata/cms/Run2011A/ElectronHad/AOD/12Oct2013-v1/20001/001F9231-F141-E311-8F76-003048F00942.root` to point to an example file.

Chage also the maximum number of events to 10.  I.e., change `-1`to `10` in `process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1))`.

In addition, insert, below the *PoolSource* module, the following lines:

```
#needed to cache the conditions data
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.GlobalTag.connect = cms.string('sqlite_file:/cvmfs/cms-opendata-conddb.cern.ch/FT_53_LV5_AN1_RUNA.db')
process.GlobalTag.globaltag = 'FT_53_LV5_AN1::All'
```

> ## Take a look at the final validation config file
>
> At the end, the config file should look like
>
> ~~~
> import FWCore.ParameterSet.Config as cms
> process = cms.Process("Demo")
> process.load("FWCore.MessageService.MessageLogger_cfi")
> process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )
> process.source = cms.Source("PoolSource",
> # replace 'myfile.root' with the source file you want to use
>    fileNames = cms.untracked.vstring(
>        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/ElectronHad/AOD/12Oct2013-v1/20001/001F9231-F141-E311-8F76-003048F00942.root'
>    )
> )
> #needed to cache the conditions data
> process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
> process.GlobalTag.connect = cms.string('sqlite_file:/cvmfs/cms-opendata-conddb.cern.ch/FT_53_LV5_AN1_RUNA.db')
> process.GlobalTag.globaltag = 'FT_53_LV5_AN1::All'
>
> process.demo = cms.EDAnalyzer('DemoAnalyzer'
> )
>
> process.p = cms.Path(process.demo)
> ~~~
> {: .language-python}
{: .solution}

Make symbolic links to the conditions database files from cvmfs:

~~~
ln -sf /cvmfs/cms-opendata-conddb.cern.ch/FT_53_LV5_AN1_RUNA FT_53_LV5_AN1
ln -sf /cvmfs/cms-opendata-conddb.cern.ch/FT_53_LV5_AN1_RUNA.db FT_53_LV5_AN1_RUNA.db
~~~
{: .language-bash}

and make sure the cms-opendata-conddb.cern.ch directory has actually expanded in your Docker instance. One way of doing this is executing:

~~~
ls -l /cvmfs/
~~~
{: .language-bash}

~~~
total 18
drwxr-xr-x  8 root root 4096 Jan 13  2014 cernvm-prod.cern.ch
drwxr-xr-x 69  989  984 4096 Aug 29  2014 cms.cern.ch
drwxr-xr-x 14  989  984 4096 Dec 16  2015 cms-opendata-conddb.cern.ch
drwxr-xr-x  4  989  984 4096 May 28  2014 cvmfs-config.cern.ch
~~~
{: .output}

Finally, run the cms executable with our configuration (it may really **take a while**, but the next time you want to run it will be faster):
~~~
cmsRun Demo/DemoAnalyzer/demoanalyzer_cfg.py
~~~
{: .language-bash}

~~~
14-Sep-2020 02:28:06 GMT  Initiating request to open file root://eospublic.cern.ch//eos/opendata/cms/Run2011A/ElectronHad/AOD/12Oct2013-v1/20001/001F9231-F141-E311-8F76-003048F00942.root
14-Sep-2020 02:28:13 GMT  Successfully opened file root://eospublic.cern.ch//eos/opendata/cms/Run2011A/ElectronHad/AOD/12Oct2013-v1/20001/001F9231-F141-E311-8F76-003048F00942.root
Begin processing the 1st record. Run 166782, Event 340184599, LumiSection 309 at 14-Sep-2020 02:28:26.283 GMT
Begin processing the 2nd record. Run 166782, Event 340185007, LumiSection 309 at 14-Sep-2020 02:28:26.284 GMT
Begin processing the 3rd record. Run 166782, Event 340187903, LumiSection 309 at 14-Sep-2020 02:28:26.285 GMT
Begin processing the 4th record. Run 166782, Event 340227487, LumiSection 309 at 14-Sep-2020 02:28:26.285 GMT
Begin processing the 5th record. Run 166782, Event 340210607, LumiSection 309 at 14-Sep-2020 02:28:26.285 GMT
Begin processing the 6th record. Run 166782, Event 340256207, LumiSection 309 at 14-Sep-2020 02:28:26.286 GMT
Begin processing the 7th record. Run 166782, Event 340165759, LumiSection 309 at 14-Sep-2020 02:28:26.286 GMT
Begin processing the 8th record. Run 166782, Event 340396487, LumiSection 309 at 14-Sep-2020 02:28:26.287 GMT
Begin processing the 9th record. Run 166782, Event 340390767, LumiSection 309 at 14-Sep-2020 02:28:26.287 GMT
Begin processing the 10th record. Run 166782, Event 340435263, LumiSection 309 at 14-Sep-2020 02:28:26.288 GMT
14-Sep-2020 02:28:26 GMT  Closed file root://eospublic.cern.ch//eos/opendata/cms/Run2011A/ElectronHad/AOD/12Oct2013-v1/20001/001F9231-F141-E311-8F76-003048F00942.root

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
