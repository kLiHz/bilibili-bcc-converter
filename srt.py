from io import TextIOWrapper
import sys

def timeStrToSeconds(t: str) -> float:
    h  = int(t[ :2])
    m  = int(t[3:5])
    s  = int(t[6:8])
    ms = int(t[9: ])
    return (ms / 1000) + s + (60 * m) + (60 * 60 * h)


def secondsToTimeStr(t: float) -> str:
    ms = int(t * 1000) % 1000
    s = int(t)
    m = s // 60
    h = m // 60
    m %= 60
    s %= 60
    return '{:0>2}:{:0>2}:{:0>2},{:0>3}'.format(h, m, s, ms)


def composeUsage(path: str) -> str:
    return \
'''SRT Tool v0.0.1

Usage:
    python3 {} <command> [in] [out] [...args]

Commands:

    shift   Shift the subtitle timestamp, in seconds.
    renum   Re-numbering the subtitle parts.
'''\
    .format(path)


def parseCommandLineOptions(argv: list[str]) -> dict:
    if "-h" in argv or "--help" in argv:
        return { 'command': 'help' }
    elif len(argv) < 4 or argv[1] not in ['shift', 'renum']:
        return { 'command': 'invalid' }
    else:
        return {
            'command': argv[1],
            'in': argv[2],
            'out': argv[3],
            'rest': argv[4:],
        }


def readItem(f: TextIOWrapper) -> list[str]:
    l = [f.readline() for i in range(3)]
    while line := f.readline() != '\n':
        l.append(line)
    return l


def readSubtitles(filePath: str):
    with open(filePath) as f:
        cnt = 0
        item = list()
        for line in f:
            cnt += 1
            item.append(line)
            if cnt > 3 and line == '\n':
                cnt = 0
                yield item
                item = list()
                continue
        if len(item) > 0:
            yield item


def reNumberSRT(inFilePath: str, outFilePath: str):
    l = []
    cnt = 1
    for i in readSubtitles(inFilePath):
        i[0] = f'{cnt}\n'
        l += i
        cnt += 1
    with open(outFilePath, 'w') as f:
        f.writelines(l)


def shiftTimeStr(s: str, seconds: float):
    return secondsToTimeStr(timeStrToSeconds(s) + seconds)


def shiftTimePeriodStr(s: str, seconds: float) -> str:
    ARROW = ' --> '
    l = s.split(ARROW)
    return shiftTimeStr(l[0], seconds) + ARROW + shiftTimeStr(l[1], seconds)


def shiftSRT(inFilePath: str, outFilePath: str, seconds: float):
    l = []
    for i in readSubtitles(inFilePath):
        i[1] = shiftTimePeriodStr(i[1][:-1], seconds) + '\n'
        l += i
    with open(outFilePath, 'w') as f:
        f.writelines(l)


if __name__ == "__main__":
    
    r = parseCommandLineOptions(sys.argv)

    match r['command']:
        case 'shift':
            if len(r['rest']) < 1:
                print('Missing arguments.\n\n{}'.format(composeUsage(sys.argv[0])))
            else:
                arg = float(r['rest'][0])
                print('Shifting srt file "{}" to "{}" for {} seconds.'.format(r['in'], r['out'], arg))
                shiftSRT(r['in'], r['out'], arg)
                print('Done.')
        case 'renum':
            print('Re-numbering srt file "{}" to "{}".'.format(r['in'], r['out']))
            reNumberSRT(r['in'], r['out'])
            print('Done.')
        case 'invalid':
            print('Invalid options.\n\n{}'.format(composeUsage(sys.argv[0])))
        case 'help':
            print(composeUsage(sys.argv[0]))
        case _:
            print('Unexpected.')
