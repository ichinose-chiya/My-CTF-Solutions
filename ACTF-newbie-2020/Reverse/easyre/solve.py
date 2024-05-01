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
