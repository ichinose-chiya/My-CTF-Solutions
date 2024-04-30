# AngrCTF - 00\_angr\_find

## _Introduction_ 

[angr](https://github.com/angr/angr) is a strong concolic execution framework written in Python, which provides us with tons of useful tools to do the concolic execution on executable binary files.

[angr_ctf](https://github.com/jakespringer/angr_ctf) is a project for people to get familiar with the usage of angr, which has provided us with about 18 challenges that can be solved by the angr.

Before we start, we need to install some dependencies:

```shell
$ sudo apt-get install gcc-multilib
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

Though the source code is provided, the recommended way to solve the challenge is to treat them the same as general `CTF REVERSE` challenge.

In the following posts I'll write the write-up for each challenges in the project.

## Analysis

We firstly drag the binary file into IDA and find that it's just like a general CTF-RE challenge: read the input and determine whether it's correct or not.

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  int i; // [esp+1Ch] [ebp-1Ch]
  char s1[9]; // [esp+23h] [ebp-15h] BYREF
  unsigned int v6; // [esp+2Ch] [ebp-Ch]

  v6 = __readgsdword(0x14u);
  printf("Enter the password: ");
  __isoc99_scanf("%8s", s1);
  for ( i = 0; i <= 7; ++i )
    s1[i] = complex_function(s1[i], i);
  if ( !strcmp(s1, "NSGJRTMP") )
    puts("Good Job.");
  else
    puts("Try again.");
  return 0;
}
```

The `complex_function()` will encode our input simply like this:

```c
int __cdecl complex_function(int a1, int a2)
{
  if ( a1 <= 64 || a1 > 90 )
  {
    puts("Try again.");
    exit(1);
  }
  return (3 * a2 + a1 - 65) % 26 + 65;
}
```

## Solution

As the logic of encoding input is simple, we can just simply write out a script to get the answer like this:

```python
s = "NSGJRTMP"
ans = ''
for i in range(len(s)):
    c = ord(s[i])
    c -= 65
    c -= i * 3
    while c < 0:
        c += 26
    c += 65
    ans += chr(c)
print(ans)
```

Then we'll get the correct answer:

![](https://s2.loli.net/2023/07/12/KZAv4SwdGo3I2cL.png)

But for those challenge with complex logic, reversing the program and writing the script directly is definitely not a wise approach. Thus we need to find a more general solution for those extremly complex ones.

As the `angr` has provided us with a powerful `concolic execution engine`, we can just let the `angr` explore until the destination we want in the program, e.g., **the path that represents the input is correct**:

```python
import angr

proj = angr.Project('./00_angr_find')
simgr = proj.factory.simgr(proj.factory.entry_state())
simgr.explore(find = 0x80492F0)
```

If the constraints is solvable, the result will be stored in `simgr.found`, which is an array of the `state` (representing a execution context of the program). Then we can **extract the input that satisfies the constraints in any of these states** like this:

```python
if simgr.found:
    print(simgr.found[0].posix.dumps(0))
```

So here comes the final solution script:

```python
import angr

proj = angr.Project('./00_angr_find')
simgr = proj.factory.simgr(proj.factory.entry_state())
simgr.explore(find = 0x80492F0)

if simgr.found:
    print(simgr.found[0].posix.dumps(0))
else:
    print("Solution not found!")
```

It's so easy, right?

![](https://s2.loli.net/2023/07/12/87FWog5G4PHzUJc.png)
