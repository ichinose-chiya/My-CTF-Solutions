# GXYCTF2019 - Reverse - luck_guy

## Reverse

As we drag the binary file provided from the author into the IDA, we can easily find out that the core logic of verifying the flag is in the function `get_flag()`, which mainly consists of a loop that has a `switch` statement as its core componet. In the `switch` statement the flag consists of two string `f1` and `f2`, while the value of `f2` will be randomly changed in different branches in the `switch`:

```c
unsigned __int64 get_flag()
{
  unsigned int v0; // eax
  int i; // [rsp+4h] [rbp-3Ch]
  int j; // [rsp+8h] [rbp-38h]
  __int64 s; // [rsp+10h] [rbp-30h] BYREF
  char v5; // [rsp+18h] [rbp-28h]
  unsigned __int64 v6; // [rsp+38h] [rbp-8h]

  v6 = __readfsqword(0x28u);
  v0 = time(0LL);
  srand(v0);
  for ( i = 0; i <= 4; ++i )
  {
    switch ( rand() % 200 )
    {
      case 1:
        puts("OK, it's flag:");
        memset(&s, 0, 0x28uLL);
        strcat((char *)&s, f1);
        strcat((char *)&s, &f2);
        printf("%s", (const char *)&s);
        break;
      case 2:
        printf("Solar not like you");
        break;
      case 3:
        printf("Solar want a girlfriend");
        break;
      case 4:
        s = 0x7F666F6067756369LL;
        v5 = 0;
        strcat(&f2, (const char *)&s);
        break;
      case 5:
        for ( j = 0; j <= 7; ++j )
        {
          if ( j % 2 == 1 )
            *(&f2 + j) -= 2;
          else
            --*(&f2 + j);
        }
        break;
      default:
        puts("emmm,you can't find flag 23333");
        break;
    }
  }
  return __readfsqword(0x28u) ^ v6;
}
```

At the same time, we can find out that the value of `f1` is `GXY{do_not_`, which is initialized on the `.data` segment as below:

```
.data:0000000000601078 ; char f1[]
.data:0000000000601078 f1              db 'GXY{do_not_',0      ; DATA XREF: get_flag+9E↑o
```

As all the characters in the flag should be visible ones, we can use a brute-force method to resolve it:

```python
import binascii

f1 = 'GXY{do_not_'
f2 = [i for i in (binascii.unhexlify('7F666F6067756369')[::-1])]

while True:
    again = False
    for i in f2:
        if i < 32 or i >126:
            again = True
            break

    if not again:
        break

    for i in range(8):
        if i %2 == 1:
            f2[i] -= 2
        else:
            f2[i] -= 1

print(f1 + ''.join([chr(i) for i in f2]))
```

Here comes the flag:

![image.png](https://s2.loli.net/2024/05/01/goIsFJTwWS8Arfp.png)
