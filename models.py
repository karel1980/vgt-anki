
import genanki
from enum import IntEnum

class Model(IntEnum):
  WORD_TO_SIGN=1
  SIGN_TO_WORD=2
  BIDIRECTIONAL=3


descriptions = dict()

descriptions[Model.WORD_TO_SIGN]= "Word to sign"
descriptions[Model.SIGN_TO_WORD]= "Sign to word",
descriptions[Model.BIDIRECTIONAL]= "Word to sign and back"

def create_model(model):
    templates = []

    if model in [ Model.WORD_TO_SIGN, Model.BIDIRECTIONAL ]:
        templates.append({
          'name': 'Word to sign',
          'qfmt': '{{Question}}<br/>{{Regions}}',
          'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
        })

    if model in [ Model.SIGN_TO_WORD, Model.BIDIRECTIONAL ]:
        templates.append({
          'name': 'Sign to word',
          'qfmt': '{{Regions}}{{Answer}}',
          'afmt': '{{FrontSide}}<hr id="answer">{{Question}}',
        })

    return genanki.Model(
      20230832000 + model,
      descriptions[model],
      fields=[
        {'name': 'Question'},
        {'name': 'Answer'},
        {'name': 'Category'},
        {'name': 'Regions'}
      ],
      templates=templates
      )

WORD_TO_SIGN = create_model(Model.WORD_TO_SIGN)
SIGN_TO_WORD = create_model(Model.SIGN_TO_WORD)
BIDIRECTIONAL = create_model(Model.BIDIRECTIONAL)

