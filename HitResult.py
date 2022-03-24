from enum import Enum
import re

noun_regex = r'(\(((n(|,[^)]+))|aux)\))'
godan_regex = r'(\(v5.(|,[^)]+)\))'
ichidan_regex = r'(\(v1.(|,[^)]+)\))'
naAdj_regex = r'(\([^\(]*,adj-na\)|\(adj-na(\)|,?[^)]+\)))'
iAdj_regex = r'(\(adj-i(|,[^)]+)\))'

wordtypes_regex = {'noun': noun_regex,\
    'godan': godan_regex,\
    'ichidan': ichidan_regex,\
    'naAdj': naAdj_regex,\
    'iAdj': iAdj_regex}

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

class HitResult:
    def __init__(self, hittype: WordType, definition: str) -> None:
        self.type = hittype
        self.definition = HitResult.clean_up_definition(definition)
    
    def clean_up_definition(definition: str) -> str:
        patterns = [
            r'\([\d]+\)',
            r'\(See [^)]+\)',
            r'\(uk\)',
            r'\(P\)',
            r'\(abbr\)'
        ]
        for p in patterns:
            definition = re.sub(p, '', definition)
        
        definition = re.sub(r' +', ' ', definition)
        definition = re.sub(r'^ ', '', definition)
        
        return definition
