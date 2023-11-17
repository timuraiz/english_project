from aiohttp import ClientSession
from random import choice

from ai21.services.models import Model
from ai21.services.models.models import Action
from bot import logging
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
    _logger = logging.getLogger(__name__)

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
        return f'<u><i><b>{sub_text}</b></i></u>'

    @staticmethod
    def _choose_action(action: Action):
        return action.action

    async def _request(self) -> dict | None:
        async with ClientSession() as session:
            try:
                async with session.post(self._url, json=self._payload, headers=self._headers, ssl=False) as response:
                    response_data = await response.json()
                    response.raise_for_status()
                    self._logger.info(f"Request successful. Response: {response_data}")
                    return response_data
            except Exception as e:
                self._logger.exception(f"An error occurred during the request: {e}")
                return None

    def _format_ans(self, model: Model) -> [str, int]:
        corrected_text = self.text
        for curr_action in reversed(model.actions):
            corrected_text = (
                    corrected_text[:curr_action.start_index] +
                    self._make_bold(self._choose_action(curr_action)) +
                    corrected_text[curr_action.end_index:]
            )
        return corrected_text, len(model.actions)

    def _process(self, response_dict: dict):
        model = self._parse(response_dict)
        return self._format_ans(model)

    async def process(self) -> tuple[dict, int] | tuple[None, None]:
        try:
            response_dict = await self._request()
            return self._process(response_dict)
        except Exception as e:
            self._logger.exception(f"An error occurred during processing: {e}")
            return None, None


class GrammarImprover(TextImprover):
    _url = 'https://api.ai21.com/studio/v1/gec'
    _action_type = 'corrections'


class VocabularyImprover(TextImprover):
    _url = 'https://api.ai21.com/studio/v1/improvements'
    _payload = {
        "types": [
            "fluency",
            "vocabulary/specificity",
            "vocabulary/variety",
            "clarity/short-sentences",
            "clarity/conciseness"
        ]
    }
    _action_type = 'improvements'

    @staticmethod
    def _choose_action(action: Action):
        return choice(action.action)
