# GFCTF2021 - RE - wordy

## Reverse

As the IDA failed to disassemble the code from `0x1144` after we dragged the file into it, we can simply find out that it use the `junk code` to confuse the disassembler:

```c
.text:0000000000001135 ; int __fastcall main(int, char **, char **)
.text:0000000000001135 main:                                   ; DATA XREF: start+1D↑o
.text:0000000000001135 ; __unwind {
.text:0000000000001135                 push    rbp
.text:0000000000001136                 mov     rbp, rsp
.text:0000000000001139                 sub     rsp, 10h
.text:000000000000113D                 mov     dword ptr [rbp-4], 0
.text:0000000000001144
.text:0000000000001144 loc_1144:                               ; CODE XREF: .text:loc_1144↑j
.text:0000000000001144                 jmp     short near ptr loc_1144+1
.text:0000000000001144 ; ---------------------------------------------------------------------------
.text:0000000000001146                 dw 0BFC0h
.text:0000000000001148                 dq 0FFFEDFE800000068h, 65BFC0FFEBFFh, 0FFEBFFFFFED2E800h
.text:0000000000001148                 dq 0C5E80000006CBFC0h, 6CBFC0FFEBFFFFFEh, 0FFFFFEB8E8000000h
.text:0000000000001148                 dq 6FBFC0FFEBh, 0C0FFEBFFFFFEABE8h, 0FE9EE800000020BFh
.text:0000000000001148                 dq 77BFC0FFEBFFFFh, 0EBFFFFFE91E80000h, 0E80000006FBFC0FFh
.text:0000000000001148                 dq 0BFC0FFEBFFFFFE84h, 0FFFE77E800000072h, 6CBFC0FFEBFFh
.text:0000000000001148                 dq 0FFEBFFFFFE6AE800h, 5DE800000064BFC0h, 21BFC0FFEBFFFFFEh
```

There's no doubt that it's not a wise choice to remove all the junk codes manually because the program is very BIG:

```c
.text:0000000000001135 ; int __fastcall main(int, char **, char **)
.text:0000000000001135 main:                                   ; DATA XREF: start+1D↑o
.text:0000000000001135 ; __unwind {
.text:0000000000001135                 push    rbp
.text:0000000000001136                 mov     rbp, rsp
.text:0000000000001139                 sub     rsp, 10h
.text:000000000000113D                 mov     dword ptr [rbp-4], 0
.text:0000000000001144
.text:0000000000001144 loc_1144:                               ; CODE XREF: .text:loc_1144↑j
.text:0000000000001144                 jmp     short near ptr loc_1144+1
.text:0000000000001144 ; ---------------------------------------------------------------------------
.text:0000000000001146                 db 0C0h
.text:0000000000001147 ; ---------------------------------------------------------------------------
.text:0000000000001147                 mov     edi, 68h ; 'h'
.text:000000000000114C                 call    _putchar
.text:0000000000001151
.text:0000000000001151 loc_1151:                               ; CODE XREF: .text:loc_1151↑j
.text:0000000000001151                 jmp     short near ptr loc_1151+1
.text:0000000000001151 ; ---------------------------------------------------------------------------
.text:0000000000001153                 db 0C0h
.text:0000000000001154 ; ---------------------------------------------------------------------------
.text:0000000000001154                 mov     edi, 65h ; 'e'
.text:0000000000001159                 call    _putchar
.text:000000000000115E
.text:000000000000115E loc_115E:                               ; CODE XREF: .text:loc_115E↑j
.text:000000000000115E                 jmp     short near ptr loc_115E+1
.text:000000000000115E ; ---------------------------------------------------------------------------
.text:0000000000001160                 db 0C0h
.text:0000000000001161 ; ---------------------------------------------------------------------------
.text:0000000000001161                 mov     edi, 6Ch ; 'l'
.text:0000000000001166                 call    _putchar
.text:000000000000116B
.text:000000000000116B loc_116B:                               ; CODE XREF: .text:loc_116B↑j
.text:000000000000116B                 jmp     short near ptr loc_116B+1
.text:000000000000116B ; ---------------------------------------------------------------------------
.text:000000000000116D                 db 0C0h
.text:000000000000116E ; ---------------------------------------------------------------------------
.text:000000000000116E                 mov     edi, 6Ch ; 'l'
.text:0000000000001173                 call    _putchar
.text:0000000000001178
.text:0000000000001178 loc_1178:                               ; CODE XREF: .text:loc_1178↑j
.text:0000000000001178                 jmp     short near ptr loc_1178+1
.text:0000000000001178 ; ---------------------------------------------------------------------------
.text:000000000000117A                 db 0C0h
.text:000000000000117B ; ---------------------------------------------------------------------------
.text:000000000000117B                 mov     edi, 6Fh ; 'o'
.text:0000000000001180                 call    _putchar
.text:0000000000001185
.text:0000000000001185 loc_1185:                               ; CODE XREF: .text:loc_1185↑j
.text:0000000000001185                 jmp     short near ptr loc_1185+1
.text:0000000000001185 ; ---------------------------------------------------------------------------
.text:0000000000001187                 db 0C0h
.text:0000000000001188 ; ---------------------------------------------------------------------------
.text:0000000000001188                 mov     edi, 20h ; ' '
.text:000000000000118D                 call    _putchar
.text:0000000000001192
.text:0000000000001192 loc_1192:                               ; CODE XREF: .text:loc_1192↑j
.text:0000000000001192                 jmp     short near ptr loc_1192+1
.text:0000000000001192 ; ---------------------------------------------------------------------------
.text:0000000000001194                 db 0C0h
```

We can use `IDA python` here to change all the `0xC0` into `0x90` (nop):

```python
import idc

for i in range(0x1135, 0x3100):
    if idc.get_db_byte(i) == 0xc0:
        idc.patch_byte(i, 0x90)
```

But there's a problem here: even though I fix all the junk codes, the IDA still won't continue to disassemble automatically (it'll disassemble a basic block only and stop working then), which means that it still requres my manual work:

```c
.text:0000000000001135 ; int __fastcall main(int, char **, char **)
.text:0000000000001135 main:                                   ; DATA XREF: start+1D↑o
.text:0000000000001135 ; __unwind {
.text:0000000000001135                 push    rbp
.text:0000000000001136                 mov     rbp, rsp
.text:0000000000001139                 sub     rsp, 10h
.text:000000000000113D                 mov     dword ptr [rbp-4], 0
.text:0000000000001144
.text:0000000000001144 loc_1144:                               ; CODE XREF: .text:loc_1144↑j
.text:0000000000001144                 jmp     short near ptr loc_1144+1
.text:0000000000001146 ; ---------------------------------------------------------------------------
.text:0000000000001146                 nop
.text:0000000000001147                 mov     edi, 68h ; 'h'
.text:000000000000114C                 call    _putchar
.text:0000000000001151
.text:0000000000001151 loc_1151:                               ; CODE XREF: .text:loc_1151↑j
.text:0000000000001151                 jmp     short near ptr loc_1151+1
.text:0000000000001151 ; ---------------------------------------------------------------------------
.text:0000000000001153                 db  90h
```

So we need to find another solution here. Notice that all the char printed by `putchar()` is stored directly in `.text`, which means that we can use `IDA python` to read every char directly.

```python
.text:0000000000001153                 nop
.text:0000000000001154                 mov     edi, 65h ; 'e'
.text:0000000000001159                 call    _putchar
.text:000000000000115E
.text:000000000000115E loc_115E:                               ; CODE XREF: .text:loc_115E↑j
.text:000000000000115E                 jmp     short near ptr loc_115E+1
```

As there's a `0xC0` locates on the beginning of every basic block as an indicator, here comes my final solution:

```python
import idc

for i in range(0x1135, 0x3100):
    if idc.get_db_byte(i) == 0xc0:
        print(chr(idc.get_db_byte(i + 2)), end = '')
```

Then we'll get the flag:

![image.png](https://s2.loli.net/2023/07/12/OhP1YSvunmBFk4A.png)

> I think it's a little crazy...
