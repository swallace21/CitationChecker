import os

line_num = 1
start_doc_check = r'begin{document}'
start_doc = False
cite_check = '\cite{'

citations = {}

def is_line_active(line):
    global start_doc
    if start_doc:
        if line[:1] != '%' and len(line) > 0 and cite_check in line:
            return True
        else:
            return False
    elif start_doc_check in line:
        start_doc = True
        return False

def keep_reading_line(c,l,c_num):
    #one_forward = c_num + 1
    one_behind  = c_num - 1
    if (c == '%') and (l[one_behind:c_num] != '\\'):  # \
        return False
    else:
        return True

def add_citation(citation):
    if citation in citations:
        citations[citation]['count'] += 1
        citations[citation]['line_nums'].append(line_num)
    else:
        citations[citation] = {'count': 1, 'line_nums':[line_num]}

def parse_citations(citation):
    left = cite_check
    right = '}'
    cites = citation[citation.index(left)+len(left):citation.index(right)]
    for citation in [c.strip() for c in cites.split(',')]:
        add_citation(citation)
    
####### MAIN
with open('paste_latex_here', 'r') as file:
    for line in file.read().splitlines():
        if is_line_active(line):
            c_num = 0
            for c in line:
                if keep_reading_line(c,line,c_num):
                    if line[c_num:(c_num+6)] == cite_check:
                        parse_citations(line[c_num:])
                else:
                    break
                c_num += 1
        line_num += 1

### PRINT FINAL STATS
tot_citations = 0
for k in sorted(citations, key=str.lower):
    v = citations[k]
    tot_citations += v['count']
    print('\n' + k,'\n   count =',v['count'],'  line_nums =',v['line_nums'])

print('\n')
print('### TOTALS ###')
print('   Unique Citations    =',len(citations.keys()))
print('   Frequency Citations =',tot_citations)
