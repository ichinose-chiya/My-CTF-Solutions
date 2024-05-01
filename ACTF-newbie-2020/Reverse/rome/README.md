# ACTF - newbie - 2020 - RE - rome

## Reverse

As we use the IDA to do the reverse engineering work on the binary executable file provided by the author, we can easily find out that the core logic of the whole programe is in the `func()` function, which is just to have some very simple calculation and comparision work on the input:

```c
int func()
{
  int result; // eax
  int v1[4]; // [esp+14h] [ebp-44h]
  unsigned __int8 v2; // [esp+24h] [ebp-34h] BYREF
  unsigned __int8 v3; // [esp+25h] [ebp-33h]
  unsigned __int8 v4; // [esp+26h] [ebp-32h]
  unsigned __int8 v5; // [esp+27h] [ebp-31h]
  unsigned __int8 v6; // [esp+28h] [ebp-30h]
  int v7; // [esp+29h] [ebp-2Fh]
  int v8; // [esp+2Dh] [ebp-2Bh]
  int v9; // [esp+31h] [ebp-27h]
  int v10; // [esp+35h] [ebp-23h]
  unsigned __int8 v11; // [esp+39h] [ebp-1Fh]
  char v12[17]; // [esp+3Bh] [ebp-1Dh] BYREF
  int i; // [esp+4Ch] [ebp-Ch]

  strcpy(v12, "Qsw3sj_lz4_Ujw@l");
  printf("Please input:");
  scanf("%s", &v2);
  result = v2;
  if ( v2 == 'A' )
  {
    result = v3;
    if ( v3 == 'C' )
    {
      result = v4;
      if ( v4 == 'T' )
      {
        result = v5;
        if ( v5 == 'F' )
        {
          result = v6;
          if ( v6 == '{' )
          {
            result = v11;
            if ( v11 == '}' )
            {
              v1[0] = v7;
              v1[1] = v8;
              v1[2] = v9;
              v1[3] = v10;
              for ( i = 0; i <= 15; ++i )
              {
                if ( *((char *)v1 + i) > '@' && *((char *)v1 + i) <= 'Z' )
                  *((_BYTE *)v1 + i) = (*((char *)v1 + i) - 51) % 26 + 'A';
                if ( *((char *)v1 + i) > '`' && *((char *)v1 + i) <= 'z' )
                  *((_BYTE *)v1 + i) = (*((char *)v1 + i) - 79) % 26 + 'a';
              }
              for ( i = 0; i <= 15; ++i )
              {
                result = (unsigned __int8)v12[i];
                if ( *((_BYTE *)v1 + i) != (_BYTE)result )
                  return result;
              }
              result = printf("You are correct!");
            }
          }
        }
      }
    }
  }
  return result;
}
```

## Solution

As the core logic of the program is clear, we can just reverse the calculation and get the flag by a simple brute-force guessing, as the flag always consists of visible characters:

```python
def solver():
    s = [ord(i) for i in "Qsw3sj_lz4_Ujw@l"]
    flag = ''

    for i in range(16):
        found = False

        for c in range(128):
            ch = c

            if c > ord('@') and c <= ord('Z'):
                c = (c - 51) % 26 + ord('A')
            if c > ord('`') and c <= ord('z'):
                c = (c - 79) % 26 + ord('a')
            if c == s[i]:
                flag += chr(ch)
                found = True
                break

        if not found:
            raise Exception('flag could not be found by brute force')

    print(flag)

if __name__ == '__main__':
    solver()
else:
    raise Exception("What the hell are you doooooooooooooing???")
```

Here comes the flag:

![image.png](https://s2.loli.net/2024/05/01/W24MyOuY6lCK3ct.png)
