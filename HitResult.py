from enum import Enum
import re
from tkinter.messagebox import NO

noun_regex = r'(\(((n(|,[^)]+))|aux)\))'
godan_regex = r'(\(v5.(|,[^)]+)\))'
ichidan_regex = r'(\(v1.(|,[^)]+)\))'
naAdj_regex = r'(\([^\(]*,adj-na\)|\(adj-na(\)|,?[^)]+\)))'
iAdj_regex = r'(\(adj-i(|,[^)]+)\))'
dunno_regex = r'(\(dunno\))'

wordtypes_regex = {'noun': noun_regex,\
    'godan': godan_regex,\
    'ichidan': ichidan_regex,\
    'naAdj': naAdj_regex,\
    'iAdj': iAdj_regex,\
    'dunno': dunno_regex}

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
    def __init__(self, hittype: WordType, definition: str, transitivness: str = None) -> None:
        self.type = hittype
        self.transitivness = HitResult.cleanup_transitivness(transitivness)
        self.definition = HitResult.clean_up_definition(definition)
    
    def cleanup_transitivness(transitivness):
        if transitivness is None:
            return None
        if len(re.findall(r'i', transitivness)) > 0 and len(re.findall(r't', transitivness)) > 0:
            return '他動詞と自動車'
        elif len(re.findall(r'i', transitivness)) > 0:
            return '自動車'
        elif len(re.findall(r't', transitivness)) > 0:
            return '他動詞'

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
