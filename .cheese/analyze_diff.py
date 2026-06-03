import sys, collections
counts = collections.Counter()
for line in sys.stdin:
    parts = line.strip().split('\t')
    if len(parts) >= 2 and parts[0] in ('A','M') and 'force-app/main/default/' in parts[1]:
        path = parts[1].split('force-app/main/default/')[-1]
        mtype = path.split('/')[0]
        counts[mtype] += 1
for mtype, n in counts.most_common():
    print(f'{n:4d} {mtype}')
