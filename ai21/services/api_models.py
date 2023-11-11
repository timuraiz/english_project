import requests
import ast

from ai21.services.models import Model
from config.config import cfg


class TextImprover:
    _url: str = None
    _api_key: str = cfg.API_KEY
    text: str = None
    _payload: dict = {'text': text}
    _headers = {
        'accept': 'application/json',
        'content-type': 'application/json',
        'Authorization': f'Bearer {_api_key}'
    }
    _not_allowed_to_override = ['url', 'api_key', 'headers', 'payload']
    _action_type: str = None

    def __init__(self, **attrs):
        for attr, val in attrs.items():
            if attr in self._not_allowed_to_override:
                raise ValueError('This attribute defined. You aren\'t allowed to override it.')
            setattr(self, f'{attr if attr == "text" else "_" + attr}', val)
        self._payload['text'] = self.text

    @classmethod
    def _parse(cls, response_dict):
        return Model(response_dict, cls._action_type)

    @staticmethod
    def _make_bold(sub_text):
        return f'<i><b>{sub_text}</b></i>'

    def _request(self) -> dict:
        text = requests.post(self._url, json=self._payload, headers=self._headers).text
        return ast.literal_eval(text)

    def _format_ans(self, model: Model) -> [str, int]:
        corrected_text = self.text
        for curr_action in reversed(model.actions):
            corrected_text = (
                    corrected_text[:curr_action.start_index] +
                    TextImprover._make_bold(curr_action.action) +
                    corrected_text[curr_action.end_index:]
            )
        return corrected_text, len(model.actions)

    def process(self):
        api_response = self._request()
        model = self._parse(api_response)
        return self._format_ans(model)


class GrammarImprover(TextImprover):
    _url = 'https://api.ai21.com/studio/v1/gec'
    _action_type = 'corrections'


class VocabularyImprover(TextImprover):
    _url = 'https://api.ai21.com/studio/v1/improvements'
    _payload = {
        "types": [
            "fluency", "vocabulary/specificity",
            "vocabulary/variety", "clarity/short-sentences",
            "clarity/conciseness"
        ]
    }
    _action_type = 'improvements'

    def reduce_bolds(self):
        self.text = self.text.replace('<b>', '').replace('</b>', '').replace('<i>', '').replace('</i>', '')

    def _format_ans(self, model: Model) -> [str, int]:
        corrected_text = self.text
        for curr_action in reversed(model.actions):
            corrected_text = (
                    corrected_text[:curr_action.start_index] +
                    TextImprover._make_bold(curr_action.action[0]) +
                    corrected_text[curr_action.end_index:]
            )
        return corrected_text, len(model.actions)
