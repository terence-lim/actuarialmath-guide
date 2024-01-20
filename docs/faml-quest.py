with open('faml-quest.txt') as infile, open('faml-quest.md', 'wt') as outfile:
    for line in infile:
        if line and line[0] == '>':
            line = line[1:]
        outfile.write(line)

        
