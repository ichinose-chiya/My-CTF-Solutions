# ACTF - newbie - 2020 - Re - easyre

## Reverse

As we get the binary file of this challenge, we can find that the programme is encrypted with the `UPX` shell, so firstly we need to decrypt it:

```powershell
upx -d easyre.exe
```

After the shell had been broken, we can now use the IDA to analyze it. Note that the core logic of this programme is to read the input from user and compare some of it with `_sata_start__` on the `.data` segment:

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  _BYTE v4[12]; // [esp+12h] [ebp-2Eh] BYREF
  _DWORD v5[3]; // [esp+1Eh] [ebp-22h]
  _BYTE v6[5]; // [esp+2Ah] [ebp-16h] BYREF
  int v7; // [esp+2Fh] [ebp-11h]
  int v8; // [esp+33h] [ebp-Dh]
  int v9; // [esp+37h] [ebp-9h]
  char v10; // [esp+3Bh] [ebp-5h]
  int i; // [esp+3Ch] [ebp-4h]

  __main();
  qmemcpy(v4, "*F'\"N,\"(I?+@", sizeof(v4));
  printf("Please input:");
  scanf("%s", v6);
  if ( v6[0] != 'A' || v6[1] != 'C' || v6[2] != 'T' || v6[3] != 'F' || v6[4] != '{' || v10 != '}' )
    return 0;
  v5[0] = v7;
  v5[1] = v8;
  v5[2] = v9;
  for ( i = 0; i <= 11; ++i )
  {
    if ( v4[i] != _data_start__[*((char *)v5 + i) - 1] )
      return 0;
  }
  printf("You are correct!");
  return 0;
}
```

The value of the `_sata_start__` is as below:

```
.data:00402000 __data_start__  db 7Eh                  ; DATA XREF: _main+EC↑r
.data:00402001 aZyxwvutsrqponm db '}|{zyxwvutsrqponmlkjihgfedcba`_^]\[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>='
.data:00402001                 db '<;:9876543210/.-,+*)(',27h,'&%$# !"',0
```

## Solution

As the core logic of the challenge is simple, we can now simply get the script to solve that by reversing its algorithm:

```python
s = [0x7E]
s += [ord(i) for i in '}|{zyxwvutsrqponmlkjihgfedcba`_^]\[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=']
s += [ord(i) for i in '<;:9876543210/.-,+*)(']
s.append(0x27)
s += [ord(i) for i in '&%$# !"']
s.append(0)

b = [ord(i) for i in '''*F'"N,"(I?+@''']

flag = ''
for i in range(12):
    for j in range(len(s)):
        if s[j] == b[i]:
            flag += chr(j + 1)
            break

print(flag)
```

Here comes the flag:

![image.png](https://s2.loli.net/2024/05/01/rPnwpCuK1v8Rfj5.png)
