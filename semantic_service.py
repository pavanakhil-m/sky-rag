from enum import Enum

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from key_rotation import keystore
from settings import configs

load_dotenv()


class ModelType(Enum):
    CHAT = "chat"
    EMBED = "embed"


def get_llm_model(model_type: ModelType = ModelType.CHAT):
    LLM_MODEL = configs.get("LLM_MODEL", "gpt-4o")
    EMBEDDING_MODEL = configs.get("EMBEDDING_MODEL", "text-embedding-3-large")
    API_BASE = configs.get("BASE_URL", "https://gw.api-dev.de.comcast.com/openai/v1")
    OPENAI_API_KEY = keystore.get_api_key()

    if model_type == ModelType.CHAT:
        model = ChatOpenAI(
            model=LLM_MODEL,
            openai_api_base=API_BASE,
            api_key=OPENAI_API_KEY,
            streaming=False,
        )
    elif model_type == ModelType.EMBED:
        model = OpenAIEmbeddings(
            model=EMBEDDING_MODEL, openai_api_base=API_BASE, api_key=OPENAI_API_KEY
        )
    else:
        raise ValueError(f"Unsupported model type: {model_type}")

    return model
