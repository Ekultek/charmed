# Pycharm Vulnerabilities

Hello everyone, today I will be releasing some pycharm vulnerabilities. These vulnerabilities are;

 - Arbitrary code execution and sandbox escaping in a component of pycharm for Linux called `restart.py`
 - File traversal in the `charm` command on a Linux system
 
I am doing this because I first reported the vulnerabilities to pycharm responsibly disclosing the issues. I like pycharm and I use it, so I figured it would of been the right thing to do. They first closed the file traversal saying that the same concept can be applied to `vi` which I understand, but if you look at the charm command code it locks the user to the current users working directory, so the traversal is still legit. After that was closed about 12 hours later they closed the arbitrary code execution stating the following: 

```
If one has the ability to execute stuff on user's system, one as well can do this directly without restart.py
```

Which, yes I understand. But the importance of this issue is that for one, it escapes whatever sandbox you have been placed in. Also for two, you're saying you're going to allow code execution in your software because if someone has access you're basically already fucked. Yeah ..

# The Exploits

Alright let's get into it right here:

## Charm Command

For the traversal of the charm command all you have to do is the following:

`charm ../../../../../../etc/passwd` 

this will open whatever you want that you have the ability to read. You can also add `;/bin/sh` to the end of the command and get a shell (didn't report this since it's not that big of a deal)

## Code execution

When you download pycharm on a Linux system there is a file that comes with it called `restart.py`. This file is used in conjunction with the program to obviously restart it. The program requires two arguments, a PID and a path, there is also room for a third argument called `[optional argument]` this argument can be anything, and is run using `os.execv`. This function allows you to create new procs and allows you to call whatever command is needed. It also will allow you to escape from the sandbox you have been put into. You can use this to get reverse shell, escape from a sandbox, in conjunction with an LPE, or in anyway your little heart can imagine. The coolest part about it, is that when it logs the failures for the PID and path, it doesn't log the "option command" so you're basically invisible. Here is an example of the logging:

```
Dec  7 23:22:35 celestial xxxxxxx.xx: (<type 'exceptions.OSError'>, OSError(13, 'Permission denied'), <traceback object at 0x7fd7fb297fc8>)
```

So if you did `python restart.py -1 / /bin/sh` you now have a shell that is only detectable by being looked for. Otherwise it just looks like a LPE.

The exploit name is `dot_idea.py`.

# Images of Reports and of PoC

Code execution report:

![arb_code_exec_restart](https://user-images.githubusercontent.com/14183473/70473550-e5244f00-1a96-11ea-86be-96ee30c2bca2.png)

File traversale report:

![file_Traversal_stuff](https://user-images.githubusercontent.com/14183473/70473551-e5bce580-1a96-11ea-8541-99e83f472c49.png)

Code execution PoC:

![pycharm_exploit_arb_1](https://user-images.githubusercontent.com/14183473/70473926-62e85a80-1a97-11ea-99dd-d36bba309df7.png)

File traversal with /etc/passwd and /bin/bash

![traversal_etc_bash](https://user-images.githubusercontent.com/14183473/70474163-b9559900-1a97-11ea-9388-9371c33fd8cd.png)


# Bonus Points

If you read this far I have a surprise for you, there is also XXS in pycharm, check the way the folders and files are named and thank me later.


