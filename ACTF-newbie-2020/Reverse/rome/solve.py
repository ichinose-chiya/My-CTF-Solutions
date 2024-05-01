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
