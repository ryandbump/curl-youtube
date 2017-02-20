import sys
import re
import subprocess
import os

if len(sys.argv) > 2:
    sys.exit()

fileType = 'mp4'
resolution = ['itag=22', 'tag=18']

url = str(sys.argv[1])

html = subprocess.check_output('curl -sS -L --compressed -A "Mozilla/5.0 (compatible)" "%s"' % url, shell=True)
# print html

title = re.search('(?<=<title>)(.*)(?=<\/title>)', html).group(0)

title = re.sub('&[0-9#]*;', '', title)

title = re.sub('[-()]', '', title)

title = title.replace('YouTube', '')

title = "-".join(title.split())

print title
# #
download = re.search('(?<=url_encoded_fmt_stream_map)(.*)(?=<\/script>)', html).group(0)

urls = download.split(',')

def parse(urls):
    for val in urls:
        # print val
        # print "\n\n"
        if re.search(fileType, val):
            # print val + "\n\n"
            for res in resolution:
                if re.search(res, val):
                    # print val + "\n\n"
                    return val
                     # download = val

download = parse(urls)

download = download.replace('%252C', ',')

pattern = re.compile('\%([A-Fa-f0-9]{2})')
matches = pattern.findall(download)

for match in matches:
    char = match.decode('hex')
    download = download.replace('%' + match, char)

download = download.replace('\u0026', '&')
download = re.search('(?<=url\=)(.*)', download).group(0)
print download

command = 'curl -sSRL -A "Mozilla/5.0 (compatible)" -o "{0}" --retry 5 -C - "{1}"'.format(title + "." + fileType, download)

pid = os.fork()

if pid == 0:
    os.system(command)
    print 'Download Completed\n'
    exit()

else:
    print 'Parent Exiting\n'
    exit()