---
title: "Using github in the docker environment"
teaching: Self-guided
exercises: 10 min
questions:
- "Can I effectively clone from and push to a Github repository?"
objectives:
- "Clone a public github repository"
- "Clone my own github repository and push my changes to it"
keypoints:
- "First key point. Brief Answer to questions. (FIXME)"

---

## Overview

In this exercise you will clone a Github public repository and
run some of the code there. You will also clone your own
repository and push some changes to it. 

## Git and Github

https://swcarpentry.github.io/git-novice/

## Clone a repo

[09:31:32] cmsusr@cyberspace7 ~/CMSSW_5_3_32/src $ git clone https://github.com/mattbellis/cern-opendata-sandbox.git
Cloning into 'cern-opendata-sandbox'...
fatal: unable to access 'https://github.com/mattbellis/cern-opendata-sandbox.git/': error:1407742E:SSL routines:SSL23_GET_SERVER_HELLO:tlsv1 alert protocol version
[09:31:36] cmsusr@cyberspace7 ~/CMSSW_5_3_32/src $ git clone git://github.com/mattbellis/cern-opendata-sandbox.git
Cloning into 'cern-opendata-sandbox'...



> ## CHALLENGE! Test X11 forwarding
>
> Fire up a docker container following the instructions in 
> the [docker lesson]({ post_url 08-docker %}). Use
> your editor-of-choice to 
> * Open a file named ```editortest.tmp```
> * Add some text to the file.
> * Exit and save the file.
> * Verify that the file exists. 
> 
{: .challenge}


TO DO!

> ## Further reading
>
> * text
> * text
> * text
>
{: .checklist}

{% include links.md %}

