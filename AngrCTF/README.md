[angr](https://github.com/angr/angr) is a strong concolic execution framework written in Python, which provides us with tons of useful tools to do the concolic execution on executable binary files.

[angr_ctf](https://github.com/jakespringer/angr_ctf) is a project for people to get familiar with the usage of angr, which has provided us with about 18 challenges that can be solved by the angr.

Before we start, we need to install some dependencies:

```shell
$ sudo zypper in glibc-devel-32bit gcc-32bit libgcc_s1-32bit
$ pip3 install jinja2
```

The project has given us the source code of each challenge, which means that we can simply compile each of then on our own. Here comes an example:

```shell
$ git clone https://github.com/jakespringer/angr_ctf.git
$ cd 00_angr_find/
$ python3 generate.py 
Usage: ./generate.py [seed] [output_file]
$ python3 generate.py 114514 00_angr_find
```

Though the source code is provided, the recommended way to solve the challenge is to treat them the same as general CTF REVERSE challenge.

In the following posts I’ll write the write-up for each challenges in the project.
