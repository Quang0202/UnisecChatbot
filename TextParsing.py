from rasa.nlu.components import Component
import typing
from typing import Any, Optional, Text, Dict

if typing.TYPE_CHECKING:
    from rasa.nlu.model import Metadata


    class DeleteSymbols(Component):

        provides = ["text"]
        #requires = []
        defaults = {}
        language_list = None

        def __init__(self, component_config=None):
            super(DeleteSymbols, self).__init__(component_config)

        def train(self, training_data, cfg, **kwargs):
            pass

        def process(self, message, **kwargs):
            mt =  message.text
            message.text = mt.translate(mt.maketrans('', '', '$%&(){}^'))

        def persist(self, file_name: Text, model_dir: Text) -> Optional[Dict[Text, Any]]:
            pass

        @classmethod
        def load(
            cls,
            meta: Dict[Text, Any],
            model_dir: Optional[Text] = None,
            model_metadata: Optional["Metadata"] = None,
            cached_component: Optional["Component"] = None,
            **kwargs: Any
        ) -> "Component":
            """Load this component from file."""

            if cached_component:
                return cached_component
            else:
                return cls(meta)