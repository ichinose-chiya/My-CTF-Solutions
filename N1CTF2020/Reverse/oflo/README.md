# N1CTF 2020 - oflo

## Reverse

When using IDA to analyze the binary file, we can simply found the `jmp` instruction at `0x400BB1` has made the disassembler confused.

```c
.text:0000000000400B54 ; int __fastcall main(int, char **, char **)
.text:0000000000400B54 main:                                   ; DATA XREF: start+1D↑o
.text:0000000000400B54                                         ; .text:0000000000400C21↓o
.text:0000000000400B54 ; __unwind {
.text:0000000000400B54                 push    rbp
.text:0000000000400B55                 mov     rbp, rsp
.text:0000000000400B58                 sub     rsp, 240h
.text:0000000000400B5F                 mov     rax, fs:28h
.text:0000000000400B68                 mov     [rbp-8], rax
.text:0000000000400B6C                 xor     eax, eax
.text:0000000000400B6E                 lea     rdx, [rbp-210h]
.text:0000000000400B75                 mov     eax, 0
.text:0000000000400B7A                 mov     ecx, 40h ; '@'
.text:0000000000400B7F                 mov     rdi, rdx
.text:0000000000400B82                 rep stosq
.text:0000000000400B85                 mov     qword ptr [rbp-230h], 0
.text:0000000000400B90                 mov     qword ptr [rbp-228h], 0
.text:0000000000400B9B                 mov     qword ptr [rbp-220h], 0
.text:0000000000400BA6                 mov     qword ptr [rbp-218h], 0
.text:0000000000400BB1
.text:0000000000400BB1 loc_400BB1:                             ; CODE XREF: .text:loc_400BB1↑j
.text:0000000000400BB1                 jmp     short near ptr loc_400BB1+1
.text:0000000000400BB3 ; ---------------------------------------------------------------------------
.text:0000000000400BB3                 ror     byte ptr [rax-70h], 90h
.text:0000000000400BB7                 call    loc_400BBF
.text:0000000000400BB7 ; ---------------------------------------------------------------------------
.text:0000000000400BBC                 db 0E8h, 0EBh, 12h
.text:0000000000400BBF ; ---------------------------------------------------------------------------
```

As the destination of the `jmp` is `0x400BB1+1`, we can just simply patch the byte at `0x400BB1` to `0x90` (`nop`) and restart disassembling.

```c
.text:0000000000400BB1                 nop
.text:0000000000400BB2                 inc     eax
.text:0000000000400BB4                 xchg    rax, rax
.text:0000000000400BB6                 nop
```

Then it comes to the call to `0x400BBF`, which is a piece of code gadget that redirecting the control flow by changing the return address on the stack:

```
.text:0000000000400BB7                 call    loc_400BBF
.text:0000000000400BB7 ; ---------------------------------------------------------------------------
.text:0000000000400BBC                 db 0E8h, 0EBh, 12h
.text:0000000000400BBF ; ---------------------------------------------------------------------------
.text:0000000000400BBF
.text:0000000000400BBF loc_400BBF:                             ; CODE XREF: .text:0000000000400BB7↑j
.text:0000000000400BBF                 pop     rax             ; ret addr(0x400BBC)
.text:0000000000400BC0                 add     rax, 1          ; rax=0x400BBD
.text:0000000000400BC4                 push    rax             ; push back onto the stack
.text:0000000000400BC5                 mov     rax, rsp        ; following codes are equal to doing nothing
.text:0000000000400BC8                 xchg    rax, [rax]
.text:0000000000400BCB                 pop     rsp
.text:0000000000400BCC                 mov     [rsp], rax
.text:0000000000400BD0                 retn
```

So we can just patch the `call` at `0x400BB7` and the gadget at `0x400BBF` to `nop`, then restart disassembling at `0x400BBD`:

```c
.text:0000000000400BBD                 jmp     short loc_400BD1
.text:0000000000400BBF ; ---------------------------------------------------------------------------
.text:0000000000400BBF                 nop
.text:0000000000400BC0                 nop
.text:0000000000400BC1                 nop
.text:0000000000400BC2                 nop
.text:0000000000400BC3                 nop
.text:0000000000400BC4                 nop
.text:0000000000400BC5                 nop
.text:0000000000400BC6                 nop
.text:0000000000400BC7                 nop
.text:0000000000400BC8                 nop
.text:0000000000400BC9                 nop
.text:0000000000400BCA                 nop
.text:0000000000400BCB                 nop
.text:0000000000400BCC                 nop
.text:0000000000400BCD                 nop
.text:0000000000400BCE                 nop
.text:0000000000400BCF                 nop
.text:0000000000400BD0                 nop
```

As the `main()` is still undecompilable, let's just left the `sub_4008B9()` behind and check for the following code firstly(because reading the raw assembly code really sucks). After some general codes, we get to meet another obfuscated code gadget at `0x400CBD`, which is almost the same logic as before:

```c
.text:0000000000400CAC loc_400CAC:                             ; CODE XREF: .text:0000000000400C47↑j
.text:0000000000400CAC                 cmp     dword ptr [rbp-23Ch], 9
.text:0000000000400CB3                 jle     short loc_400C49
.text:0000000000400CB5                 call    loc_400CBD
.text:0000000000400CB5 ; ---------------------------------------------------------------------------
.text:0000000000400CBA                 dw 0EBE8h
.text:0000000000400CBC                 db 12h
.text:0000000000400CBD ; ---------------------------------------------------------------------------
.text:0000000000400CBD
.text:0000000000400CBD loc_400CBD:                             ; CODE XREF: .text:0000000000400CB5↑j
.text:0000000000400CBD                 pop     rax
.text:0000000000400CBE                 add     rax, 1
.text:0000000000400CC2                 push    rax
.text:0000000000400CC3                 mov     rax, rsp
.text:0000000000400CC6                 xchg    rax, [rax]
.text:0000000000400CC9                 pop     rsp
.text:0000000000400CCA                 mov     [rsp], rax
.text:0000000000400CCE                 retn
.text:0000000000400CCE ; ---------------------------------------------------------------------------
.text:0000000000400CCF                 db 48h
.text:0000000000400CD0                 dq 8348FFFFFDD0858Dh, 0FFFDF0958D4805C0h, 0E8D78948C68948FFh
```

So we patch them to `nop` again and get the correct ones:

```c
.text:0000000000400CB5                 nop
.text:0000000000400CB6                 nop
.text:0000000000400CB7                 nop
.text:0000000000400CB8                 nop
.text:0000000000400CB9                 nop
.text:0000000000400CBA                 nop
.text:0000000000400CBB                 jmp     short loc_400CCF
.text:0000000000400CBD ; ---------------------------------------------------------------------------
.text:0000000000400CBD                 nop
.text:0000000000400CBE                 nop
.text:0000000000400CBF                 nop
.text:0000000000400CC0                 nop
.text:0000000000400CC1                 nop
.text:0000000000400CC2                 nop
.text:0000000000400CC3                 nop
.text:0000000000400CC4                 nop
.text:0000000000400CC5                 nop
.text:0000000000400CC6                 nop
.text:0000000000400CC7                 nop
.text:0000000000400CC8                 nop
.text:0000000000400CC9                 nop
.text:0000000000400CCA                 nop
.text:0000000000400CCB                 nop
.text:0000000000400CCC                 nop
.text:0000000000400CCD                 nop
.text:0000000000400CCE                 nop
```

At the `loc_400D04` there's another junk code here:

```c
.text:0000000000400D04 loc_400D04:                             ; CODE XREF: .text:0000000000400CEE↑j
.text:0000000000400D04                                         ; .text:loc_400D04↑j
.text:0000000000400D04                 jmp     short near ptr loc_400D04+1
.text:0000000000400D04 ; ---------------------------------------------------------------------------
```

Just patch the first byte of `jmp` to `nop` is okay:

```c
.text:0000000000400D04 loc_400D04:                             ; CODE XREF: .text:0000000000400CEE↑j
.text:0000000000400D04                 nop
.text:0000000000400D05                 inc     eax
.text:0000000000400D07                 xchg    rax, rax
.text:0000000000400D09                 nop
.text:0000000000400D0A                 mov     edi, 0
.text:0000000000400D0F                 call    exit
.text:0000000000400D14 ; ---------------------------------------------------------------------------
.text:0000000000400D14                 nop
.text:0000000000400D15                 mov     rax, [rbp-8]
.text:0000000000400D19                 xor     rax, fs:28h
.text:0000000000400D22                 jz      short locret_400D29
.text:0000000000400D24                 call    ___stack_chk_fail
.text:0000000000400D29 ; ---------------------------------------------------------------------------
.text:0000000000400D29
.text:0000000000400D29 locret_400D29:                          ; CODE XREF: .text:0000000000400D22↑j
.text:0000000000400D29                 leave
.text:0000000000400D2A                 retn
.text:0000000000400D2A ; } // starts at 400B54
```

Now press `P` at the start of `main()` to left the IDA rethink again, then press `F5`, here finally comes the discompiled codes for `main()`:

- call the `sub_4008B9()` to do some works
- read 19 bytes from input
- call `mprotect()` to mark the first 16 bytes at `(unsigned int)main & 0xFFFFC000` (which is `0x400000`) as ` r | w | x`
- change the first 10 bytes of the `sub_400A69()`
- call the `sub_400A69()`

```c
void __fastcall __noreturn main(int a1, char **a2, char **a3)
{
  int v3; // ecx
  int v4; // er8
  int v5; // er9
  int i; // [rsp+4h] [rbp-23Ch]
  __int64 v7[4]; // [rsp+10h] [rbp-230h] BYREF
  char v8[520]; // [rsp+30h] [rbp-210h] BYREF
  unsigned __int64 v9; // [rsp+238h] [rbp-8h]

  v9 = __readfsqword(0x28u);
  memset(v8, 0, 0x200uLL);
  v7[0] = 0LL;
  v7[1] = 0LL;
  v7[2] = 0LL;
  v7[3] = 0LL;
  if ( (unsigned int)sub_4008B9((__int64)v8) == -1 )
    exit(0LL);
  read(0LL, v7, 19LL);
  qword_602048 = (__int64)sub_400A69;
  mprotect((unsigned int)main & 0xFFFFC000, 16LL, 7LL);
  for ( i = 0; i <= 9; ++i )
  {
    v3 = i % 5;
    *(_BYTE *)(qword_602048 + i) ^= *((_BYTE *)v7 + i % 5);
  }
  if ( (unsigned int)sub_400A69((unsigned int)v8, (unsigned int)v7 + 5, (unsigned int)v8, v3, v4, v5) )
    write(1LL, "Cong!\n", 6LL);
  exit(0LL);
}
```

Now let's have a look at `sub_4008B9()`, it uses the sysall `fork()` to do the whole work. Firstly the children process will wait for the ptracer to attach, then it'll execute `cat /proc/version` and exit:

```c
__int64 __fastcall sub_4008B9(__int64 a1)
{
  unsigned int v2; // [rsp+14h] [rbp-5Ch] BYREF
  int v3; // [rsp+18h] [rbp-58h]
  unsigned int v4; // [rsp+1Ch] [rbp-54h]
  __int64 v5; // [rsp+20h] [rbp-50h]
  __int64 v6; // [rsp+28h] [rbp-48h]
  __int64 v7; // [rsp+30h] [rbp-40h]
  __int64 v8; // [rsp+38h] [rbp-38h]
  __int64 v9; // [rsp+40h] [rbp-30h] BYREF
  __int64 v10[4]; // [rsp+50h] [rbp-20h] BYREF

  v10[3] = __readfsqword(0x28u);
  v4 = fork();
  if ( (v4 & 0x80000000) != 0 )
    v2 = -1;
  if ( !v4 )
  {
    v10[0] = (__int64)&unk_400DB8;
    v10[1] = (__int64)"/proc/version";
    v10[2] = 0LL;
    v9 = 0LL;
    ptrace(PTRACE_TRACEME, 0LL, 0LL, 0LL);
    execve("/bin/cat", v10, &v9);
    exit(127LL);
  }
```

Then let's take a look at the parent process, it's mainly a loop that keeps continuously calling the `ptrace(PTRACE_PEEKUSER)` and `ptrace(PTRACE_SYSCALL)`:

```c
  v3 = 0;
  v5 = a1;
  while ( 1 )
  {
    wait4(v4, &v2, 0LL, 0LL);
    if ( (v2 & 0x7F) == 0 )
      break;
    v6 = ptrace(PTRACE_PEEKUSER, v4, 120LL, 0LL);
    if ( v6 == 1 )
    {
      if ( v3 )
      {
        v3 = 0;
      }
      else
      {
        v3 = 1;
        v7 = ptrace(PTRACE_PEEKUSER, v4, 104LL, 0LL);   // rsi
        v8 = ptrace(PTRACE_PEEKUSER, v4, 96LL, 0LL);    // rdx
        sub_4007D1(v4, v7, v5, v8);
        v5 += v8;
      }
    }
    ptrace(PTRACE_SYSCALL, v4, 0LL, 0LL);
  }
  return v2;
}
```

The offset for different registers is defined in `/arch/x86/include/asm/user_64.h` as below:

```c
/*
 * Segment register layout in coredumps.
 */
struct user_regs_struct {
	unsigned long	r15;    // 0
	unsigned long	r14;    // 8
	unsigned long	r13;    // 16
	unsigned long	r12;    // 24
	unsigned long	bp;     // 32
	unsigned long	bx;     // 40
	unsigned long	r11;    // 48
	unsigned long	r10;    // 56
	unsigned long	r9;     // 64
	unsigned long	r8;     // 72
	unsigned long	ax;     // 80
	unsigned long	cx;     // 88
	unsigned long	dx;     // 96
	unsigned long	si;     // 104
	unsigned long	di;     // 112
	unsigned long	orig_ax;// 120
	unsigned long	ip;
	unsigned long	cs;
	unsigned long	flags;
	unsigned long	sp;
	unsigned long	ss;
	unsigned long	fs_base;
	unsigned long	gs_base;
	unsigned long	ds;
	unsigned long	es;
	unsigned long	fs;
	unsigned long	gs;
};
```

Thus we can get to know what the loop in parent process does: it firstly check whether the value of `rax` in children process is equal to `1`, if it does, it'll read the `rsi` and `rdx` in children process and pass them together with a value `v5` into `sub_4007D1()`.

The `v5` is initialized by the first param of `sub_4008B9()`, which is assigned an offset on the stack:

```c
.text:0000000000400BD1 loc_400BD1:                             ; CODE XREF: .text:0000000000400BBD↑j
.text:0000000000400BD1                 lea     rax, [rbp-210h]
.text:0000000000400BD8                 mov     rdi, rax
.text:0000000000400BDB                 call    sub_4008B9
```

Now let's take a look into `sub_4007D1()`. What comes first is a loop that keeps reading data from the children process and copy that to the location on the stack that passed as the first param of `sub_4008B9()`. The source is the space indicated by `rsi` in children process.

```c
__int64 __fastcall sub_4007D1(unsigned int a1, __int64 a2, __int64 a3, __int64 a4)
{
  __int64 result; // rax
  int v6; // [rsp+20h] [rbp-20h]
  int v7; // [rsp+24h] [rbp-1Ch]

  v6 = 0;
  v7 = a4 / 8;
  while ( v6 < v7 )
  {
    *(_QWORD *)(4 * v6 + a3) = ptrace(PTRACE_PEEKDATA, a1, a2 + 4 * v6, 0LL);
    ++v6;
  }
  result = a4 % 8;
  if ( (unsigned int)(a4 % 8) )
  {
    result = ptrace(PTRACE_PEEKDATA, a1, a2 + 4 * v6, 0LL);
    *(_QWORD *)(4 * v6 + a3) = result;
  }
  return result;
}
```

What data it is? As the loop will use `prace(PTRACE_SYSCALL)` to execute the children process `syscall by syscall`, and step into the `sub_4007D1()` only when the `orig_rax == 1`, we can easily guess out that the parent process is waiting for the syscall who satisfies the `nr == 1` (as the `orig_rax` is the syscall number), that is the `write()`.

Thus we can know that the parent process will copy the data from children process only when it calls the `write()`, that is, for `/bin/cat`, the content of `/proc/version` will be read back to the parent process.

Look back to the `main()`, as the code at the beginning of `sub_400A69()` is being changed, we need to change it manually in the IDA. As the source is input and the format of the flag is `n1ctf{xxx}`, the first 5 bytes are definitely the `n1ctf`, thus we can just simply fix the `sub_400A69()` with IDA python:

```python
import idc

s = 'n1ctf'

for i in range(0x400A69, 0x400A69 + 10):
    c = idc.get_db_byte(i)
    c ^= ord(s[(i - 0x400A69) % 5])
    idc.patch_byte(i, c)
```

Now the begining of `sub_400A69()` is regular:

![image.png](https://s2.loli.net/2023/07/14/5nN7fUmPOxT9yRu.png)

But we still can't use `F5` directly because there're some junk codes below, here we'd just patch the instruction at `0x400AC4` to `nop`:

```c
.text:0000000000400AC0                 jz      short loc_400AC9
.text:0000000000400AC2                 jnz     short loc_400AC9
.text:0000000000400AC4                 jmp     near ptr 801AC9h
.text:0000000000400AC9 ; ---------------------------------------------------------------------------
```

Here comes the junk code again, just fix it as what we did before:

```c
.text:0000000000400B0E                 call    loc_400B16
.text:0000000000400B0E ; ---------------------------------------------------------------------------
.text:0000000000400B13                 db 0E8h
.text:0000000000400B14                 db 0EBh
.text:0000000000400B15                 db  12h
.text:0000000000400B16 ; ---------------------------------------------------------------------------
.text:0000000000400B16
.text:0000000000400B16 loc_400B16:                             ; CODE XREF: sub_400A69+A5↑j
.text:0000000000400B16                 pop     rax
.text:0000000000400B17                 add     rax, 1
.text:0000000000400B1B                 push    rax
.text:0000000000400B1C                 mov     rax, rsp
.text:0000000000400B1F                 xchg    rax, [rax]
.text:0000000000400B22                 pop     rsp
.text:0000000000400B23                 mov     [rsp+40h+var_40], rax
.text:0000000000400B27                 retn
.text:0000000000400B27 ; ---------------------------------------------------------------------------
.text:0000000000400B28                 db 0B8h
```

Now the `sub_400A69()` can be discompiled now, which is the core logic of this challenge. The first param is the content of `/proc/version`, and the second param is our input after `nictf`:

```c
__int64 __fastcall sub_400A69(__int64 a1, __int64 a2)
{
  __int64 v2; // rbp
  int i; // [rsp+14h] [rbp-2Ch]
  char v5[24]; // [rsp+18h] [rbp-28h] BYREF
  unsigned __int64 v6; // [rsp+30h] [rbp-10h]
  __int64 v7; // [rsp+38h] [rbp-8h]

  v7 = v2;
  v6 = __readfsqword(0x28u);
  qmemcpy(v5, "5-\x11\x1AI}\x11\x14+;>=<_", 14);
  for ( i = 0; i <= 13; ++i )
  {
    if ( v5[i] != ((*(char *)(i + a1) + 2) ^ *(char *)(i + a2)) )
      return 0LL;
  }
  return 1LL;
}
```

## Solution

As the first 14 bytes of `/proc/version` is definitely the `"Linux version "`, we can easily get the flag now:

```python
s = "5-\x11\x1AI}\x11\x14+;>=<_"
b = "Linux version "
ans = ""

for i in range(14):
    ans += chr(ord(s[i]) ^ (ord(b[i]) + 2))
print(ans)
```

Here comes the flag:

![image.png](https://s2.loli.net/2023/07/14/FTlYCB2tacILnD1.png)
