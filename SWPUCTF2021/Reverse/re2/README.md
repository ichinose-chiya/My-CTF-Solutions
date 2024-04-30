# SWPUCTF2021 - re2

## Reverse

Firstly check the binary file with the `Exeinfo`:

![image.png](https://s2.loli.net/2023/07/12/INcQjudfR81T6bq.png)

As there's no any protection for it, we can just drag it directly into the IDA:

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  char Str2[64]; // [rsp+20h] [rbp-90h] BYREF
  char Str[68]; // [rsp+60h] [rbp-50h] BYREF
  int v7; // [rsp+A8h] [rbp-8h]
  int i; // [rsp+ACh] [rbp-4h]

  _main();
  strcpy(Str2, "ylqq]aycqyp{");
  printf(&Format);
  gets(Str);
  v7 = strlen(Str);
  for ( i = 0; i < v7; ++i )
  {
    if ( (Str[i] <= 96 || Str[i] > 98) && (Str[i] <= 64 || Str[i] > 66) )
      Str[i] -= 2;
    else
      Str[i] += 24;
  }
  if ( strcmp(Str, Str2) )
    printf(&byte_404024);
  else
    printf(aBingo);
  system("pause");
  return 0;
}
```

The whole logic of the program is very simple: read the input and encode it simply, then compare it with the string `ylqq]aycqyp{`.

## Solution

As the logic of encoding is very simple, we can easily write the script to solve it:

```python
s = 'ylqq]aycqyp{'
ans = ''
for i in s:
    c = ord(i)
    c += 2
    if (c <= 96 or c >= 98) and (c <= 64 or c > 66):
        ans += chr(c)
    else:
        ans += chr(c -2 - 24)
print(ans)
```

![image.png](https://s2.loli.net/2023/07/12/GcuV9IOmvD17aJX.png)

> It seems that the challenge has multiple solutions for that in fact?
