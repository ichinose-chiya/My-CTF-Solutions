import base64

def main():
    s = b"fiAGBkgXN3McFy9hAHRfCwYaIjQCRDFsXC8ZYBFmEDU="
    b = b"TcR@3t_3hp_5_G1H"
    s = base64.b64decode(s)
    for i in range(len(s)):
        print(chr(s[i] ^ b[i % 16]), end = '')
    print("")

if __name__ == '__main__':
    main()
