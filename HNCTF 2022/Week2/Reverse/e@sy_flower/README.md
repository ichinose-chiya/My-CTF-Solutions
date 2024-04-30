# HNCTF 2022 - WEEK2 - e@sy_flower

## Reverse

Drag the binary file into `IDA` directly, we can simply find a significant sign of `junk code` at `0x004010D0`:

```c
.text:00401090 ; int __cdecl main(int argc, const char **argv, const char **envp)
.text:00401090 _main:                                  ; CODE XREF: __scrt_common_main_seh(void)+F5↓p
.text:00401090                 push    ebp
.text:00401091                 mov     ebp, esp
.text:00401093                 sub     esp, 38h
.text:00401096                 mov     eax, ___security_cookie
.text:0040109B                 xor     eax, ebp
.text:0040109D                 mov     [ebp-4], eax
.text:004010A0                 push    ebx
.text:004010A1                 push    esi
.text:004010A2                 push    edi
.text:004010A3                 push    offset aPleaseInputFla ; "please input flag\n"
.text:004010A8                 call    sub_401020
.text:004010AD                 lea     eax, [ebp-34h]
.text:004010B0                 push    eax
.text:004010B1                 push    offset aS       ; "%s"
.text:004010B6                 call    sub_401050
.text:004010BB                 lea     eax, [ebp-34h]
.text:004010BE                 add     esp, 0Ch
.text:004010C1                 lea     edx, [eax+1]
.text:004010C4
.text:004010C4 loc_4010C4:                             ; CODE XREF: .text:004010C9↓j
.text:004010C4                 mov     cl, [eax]
.text:004010C6                 inc     eax
.text:004010C7                 test    cl, cl
.text:004010C9                 jnz     short loc_4010C4
.text:004010CB                 sub     eax, edx
.text:004010CD                 mov     [ebp-38h], eax
.text:004010D0                 jz      short near ptr loc_4010D4+1
.text:004010D2                 jnz     short near ptr loc_4010D4+1
.text:004010D4
.text:004010D4 loc_4010D4:                             ; CODE XREF: .text:004010D0↑j
.text:004010D4                                         ; .text:004010D2↑j
.text:004010D4                 jmp     near ptr 9A085664h
```

Just patch the `0x004010D4` to `nop` and press `p` and `F5` at the `main`, then we can get the discompiled code for the challenge easily. The main logic is just he `shifting` and `xor`:

```c
int __cdecl __noreturn main(int argc, const char **argv, const char **envp)
{
  signed int v3; // kr00_4
  int i; // edx
  char v5; // cl
  unsigned int j; // edx
  int v7; // eax
  char v8; // [esp+0h] [ebp-44h]
  char v9; // [esp+0h] [ebp-44h]
  char Arglist[48]; // [esp+10h] [ebp-34h] BYREF

  sub_401020("please input flag\n", v8);
  sub_401050("%s", (char)Arglist);
  v3 = strlen(Arglist);
  for ( i = 0; i < v3 / 2; ++i )
  {
    v5 = Arglist[2 * i];
    Arglist[2 * i] = Arglist[2 * i + 1];
    Arglist[2 * i + 1] = v5;
  }
  for ( j = 0; j < strlen(Arglist); ++j )
    Arglist[j] ^= 0x30u;
  v7 = strcmp(Arglist, "c~scvdzKCEoDEZ[^roDICUMC");
  if ( v7 )
    v7 = v7 < 0 ? -1 : 1;
  if ( !v7 )
  {
    sub_401020("yes", v9);
    exit(0);
  }
  sub_401020("error", v9);
  exit(0);
}
```

## Solution

As the core logic is simple, we can write the solution script easily:

```python
s = 'c~scvdzKCEoDEZ[^roDICUMC'
ans = []

for i in s:
    ans.append(chr(ord(i) ^ 0x30))

for i in range(len(ans) // 2):
    tmp = ans[2 * i + 1]
    ans[2 * i + 1] = ans[2 * i]
    ans[2 * i] = tmp

print(''.join(ans))
```

![image.png](https://s2.loli.net/2023/07/13/UbNFs2z76XK1dSq.png)