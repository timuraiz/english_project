from enum import Enum


class Action:
    action: str | list[str] = None
    start_index: int
    end_index: int
    original_text: str
    __specific_attrs = ['suggestions', 'suggestion']

    @classmethod
    def correct_attr(cls, attr_name: str) -> str:
        result = [attr_name[0].lower()]

        for char in attr_name[1:]:
            if char.isupper():
                result.extend(['_', char.lower()])
            else:
                result.append(char)

        prepared_attr = ''.join(result)
        return prepared_attr if prepared_attr not in cls.__specific_attrs else 'action'

    def __init__(self, **kwargs):
        for attr_name, attr_val in kwargs.items():
            attr_name = self.correct_attr(attr_name)
            setattr(self, attr_name, attr_val)


class Correction(Action):
    class CorrectionType(Enum):
        SPELLING = 'Spelling'
        GRAMMAR = 'Grammar'

    action: str
    correction_type: CorrectionType


class Improvements(Action):
    class ImprovementType(Enum):
        FLUENCY = 'fluency'

    action: list[str]
    improvement_type: ImprovementType


class ActionType:
    improvements = Improvements
    corrections = Correction


class Model:
    _id: str
    actions: list[Action]

    def __init__(self, response_dict: dict, type_action: str):
        self._id = response_dict.pop('id')
        action_class = getattr(ActionType, type_action)
        self.actions = [action_class(**action) for action in response_dict[type_action]]
