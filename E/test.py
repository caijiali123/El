import re


def pattern_match(str):
    type = ['NT1VDR','CDCFE','NT2EDMS','AIS','EDMS','NT2VDR','SRMS']
    for pattern in type:
        while re.search(pattern, str):
            if pattern=='NT2EDMS':
                type.remove('EDMS')
            list = re.findall(r"%s-+[0-9.\-+_]+"%(pattern), str)

            break


