import sys
import json

def composeUsage(path):
    return \
'''BCC to SRT converter v0.0.1

Usage:
    python3 {} <command> [in] [out]

Commands:

    bcc     Convert bcc subtitle in file [in] to srt format.
    srt     Generate bcc from srt subtitle in file [in].
'''\
    .format(path)


def parseCommandLineOption(argv):
    if "-h" in argv or "--help" in argv:
        return {
            'command': 'help',
        }
    elif len(argv) != 4 or argv[1] not in ['bcc', 'srt']:
        return {
            'command': 'invalid',
        }
    else:
        return {
            'command': argv[1],
            'in': argv[2],
            'out': argv[3],
        }


def secondsToTimeStr(t):
    ms = int(t * 1000) % 1000
    s = int(t)
    m = s // 60
    h = m // 60
    m %= 60
    s %= 60
    return '{:0>2}:{:0>2}:{:0>2},{:0>3}'.format(h, m, s, ms)


def bccToSrt(bccFilePath, srtFilePath):

    with open(bccFilePath, 'r') as f:
        data = json.loads(f.read())

    with open(srtFilePath, 'w') as o:
        count = 1
        f = secondsToTimeStr
        for item in data['body']:
            o.write('{}\n'.format(count))
            o.write('{} --> {}\n'.format(f(item['from']), f(item['to'])))
            o.write('{}\n\n'.format(item['content']))
            count += 1


r = parseCommandLineOption(sys.argv)

if r['command'] == 'bcc':
    print('Converting bcc file "{}" to srt file "{}".'.format(r['in'], r['out']))
    bccToSrt(r['in'], r['out'])
    print('Done.')
elif r['command'] == 'srt':
    print('Converting srt file "{}" to bcc file "{}".'.format(r['in'], r['out']))
    print('Sorry, this is not implemented yet.')
elif r['command'] == 'invalid':
    print("Invalid options.\n\n{}".format(composeUsage(sys.argv[0])))
elif r['command'] == 'help':
    print(composeUsage(sys.argv[0]))
