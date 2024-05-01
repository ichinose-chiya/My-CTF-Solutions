# GWCTF2019 - Re - pyre

## Reverse

This is a reverse challenge that need us to analyse a `pyc` file. Generally we can use the `uncompyle6` to do the work:

```shell
$ pip3 install  uncompyle6
$ uncompyle6 ./attachment.pyc
```

Or we can use some online tools to do the work, e.g. , [https://tool.lu/pyc/](https://tool.lu/pyc/).  After the reversing work, we can get the original logic of this `.pyc` file as below:

```python
#!/usr/bin/env python
# visit https://tool.lu/pyc/ for more information
# Version: Python 2.7

print 'Welcome to Re World!'
print 'Your input1 is your flag~'
l = len(input1)
for i in range(l):
    num = ((input1[i] + i) % 128 + 128) % 128
    code += num

for i in range(l - 1):
    code[i] = code[i] ^ code[i + 1]

print code
code = [
    '%1f',
    '%12',
    '%1d',
    '(',
    '0',
    '4',
    '%01',
    '%06',
    '%14',
    '4',
    ',',
    '%1b',
    'U',
    '?',
    'o',
    '6',
    '*',
    ':',
    '%01',
    'D',
    ';',
    '%',
    '%13']
```

> Unfortunately, my `uncompyle6` didn't get the right value of the variable `code` in the `.pyc` file from the challenge, maybe some designs in it are wrong?

Now the core logic of this challenge is very clear to use now, which is just a simple `xor` encryption only.

## Solution

As the `xor` operation has the feature that the original value can be obtained by doing the same operation twice, we can simply get the flag by using the same logic again on the ciphertext:

```python
code = [
    '\x1f',
    '\x12',
    '\x1d',
    '(',
    '0',
    '4',
    '\x01',
    '\x06',
    '\x14',
    '4',
    ',',
    '\x1b',
    'U',
    '?',
    'o',
    '6',
    '*',
    ':',
    '\x01',
    'D',
    ';',
    '%',
    '\x13']
code = [ord(i) for i in code]

for i in range(len(code) - 1):
    code[len(code) - 2 - i] ^= code[len(code) - 1 - i]

for i in range(len(code)):
    code[i] = (code[i] - i + 128) % 128

print(''.join([chr(i) for i in code]))
```

Here comes the flag:

![image.png](https://s2.loli.net/2024/05/01/gYx8uawdBsFnMfS.png)
