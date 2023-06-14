from enum import Enum
import re

#///////////////////////////////////////////////
# Toolset to identify definitions and wordtypes
#///////////////////////////////////////////////

# Finding word types
noun_regex = r'(\(([^a-z\(]*n(|,[^\)]+)|adv)\))'
godan_regex = r'(\(v5.(|,[^)]+)\))'
ichidan_regex = r'(\(v1.?(|,[^)]+)\))'
naAdj_regex = r'(\([^(]+,adj-na,[^)]+\)|\([^(]+,adj-na\)|\(adj-na(\)|,?[^)]+\)))'
iAdj_regex = r'(\(adj-i(|,[^)]+)\))'
dunno_regex = r'(\(dunno\))'

wordtypes_regex = {'noun': noun_regex,\
    'godan': godan_regex,\
    'ichidan': ichidan_regex,\
    'naAdj': naAdj_regex,\
    'iAdj': iAdj_regex,\
    'dunno': dunno_regex}

# Getting the definition with word type
final_regex = r'(?P<definition>(' +\
    noun_regex + r'|' +\
    godan_regex + r'|' +\
    ichidan_regex + r'|' +\
    naAdj_regex + r'|' +\
    iAdj_regex + r')' +\
    r'.+?(?=' + \
    noun_regex + r'|' +\
    godan_regex + r'|' +\
    ichidan_regex + r'|' +\
    naAdj_regex + r'|' +\
    iAdj_regex + r'|$))'

class NoMoreHits(Exception):
    def __init__(self, word) -> None:
        self.message = "No more " + word + " could be found"
        super().__init__(self.message)

class NoHits(Exception):
    def __init__(self, word) -> None:
        self.message = word + " could not be found AT ALL..."
        super().__init__(self.message)

class WordType(Enum):
    noun = 0
    iAdj = 1
    naAdj = 2
    godanVerb = 3
    ichidanVerb = 4
    dunno = 5

# Clean up unnecessary data
class HitResult:
    def __init__(self, hittype: WordType, definition: str, transitivness: str = None) -> None:
        self.type = hittype
        self.transitivness = HitResult.cleanup_transitivness(transitivness)
        self.definition = HitResult.clean_up_definition(definition)
    
    # From iitt to 他動詞と自動車
    def cleanup_transitivness(transitivness):
        if transitivness is None:
            return ''
        if len(re.findall(r'i', transitivness)) > 0 and len(re.findall(r't', transitivness)) > 0:
            return '他動詞と自動車'
        elif len(re.findall(r'i', transitivness)) > 0:
            return '自動車'
        elif len(re.findall(r't', transitivness)) > 0:
            return '他動詞'
        else:
            return ''


    def clean_up_definition(definition: str) -> str:
        # Getting rid of the pesky stuff in parenthesis
        patterns = [
            r'\(See [^)]+\)',
            r'\(uk\)',
            r'\(P\)',
            r'\(abbr\)',
            r'\[P\]',
            r'\(pn\)'
        ]
        for p in patterns:
            definition = re.sub(p, '', definition)

        definition_ind = re.search(r'\([\d]+\)', definition)
        if definition_ind:
            definition_ind = definition[definition_ind.span()[0] + 1  : definition_ind.span()[1] - 1]
            definition = re.sub(re.compile("\(" + definition_ind + "\)"), '- ', definition)
            definition = re.sub(r'\([\d]+\)', '\n- ', definition)
        
        # Cleaning up messy whitespaces
        definition = re.sub(r' +', ' ', definition)
        definition = re.sub(r'^ ', '', definition)

        print("_________________________________")
        print(definition)
        
        return definition
