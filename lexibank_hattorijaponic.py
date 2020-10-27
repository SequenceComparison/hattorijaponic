from pathlib import Path
import lingpy as lp

from clldutils.misc import slug
from pylexibank import Dataset as BaseDataset
from pylexibank.util import getEvoBibAsBibtex
from pylexibank import progressbar
from pylexibank import Concept, Language
import attr

@attr.s
class CustomConcept(Concept):
    Number = attr.ib(default=None)

class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = 'hattorijaponic'
    concept_class = CustomConcept

    def cmd_makecldf(self, args):
    
        concepts = {}
        for concept in self.conceptlists[0].concepts.values():
            idx = '{0}_{1}'.format(concept.number, slug(concept.english))
            args.writer.add_concept(
                    ID=idx,
                    Number=concept.number,
                    Name=concept.english,
                    Concepticon_ID=concept.concepticon_id,
                    Concepticon_Gloss=concept.concepticon_gloss,
                    )
            concepts[concept.english] = idx
        concepts['saliva (splits)'] = concepts['saliva (spit)']
        concepts['gras'] = concepts['grass']
        
        languages = args.writer.add_languages(
                lookup_factory="Name")
        
        args.writer.add_sources()
        wl = lp.Wordlist(self.raw_dir.joinpath('JAP.csv').as_posix())
        for idx in wl:
            lexeme = args.writer.add_form(
                    Language_ID=languages[wl[idx, 'language']],
                    Parameter_ID=concepts[wl[idx, 'concept']],
                    Value=wl[idx, 'ipa'],
                    Form='.'.join(wl[idx, 'tokens']),
                    Source='Hattori1973'
                    )
            args.writer.add_cognate(
                    lexeme=lexeme,
                    Cognateset_ID=wl[idx, 'cogid'],
                    Cognate_Detection_Method='expert',
                    Source=['Hattori1973']
                    )        
