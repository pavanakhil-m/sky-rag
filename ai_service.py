from datetime import datetime
from enum import Enum

from langchain.prompts import PromptTemplate

from database import VectorStore
from semantic_service import ModelType, get_llm_model
from utils.data_utils import extract_context_json, extract_json_str


class TemplateType(Enum):
    BASE = "base"
    FINAL = "final"


class AIServices:

    def get_prompt_template(self, template_type: TemplateType) -> PromptTemplate:

        if template_type == TemplateType.BASE:
            prompt = PromptTemplate(
                template="""
                You are a helpful news assistant.
                Answer ONLY from the provided transcript context.
                If the context is insufficient, just say you don't know.
                If some context is not related to the question, ignore it.

                {context}
                Question: {question}
                """,
                input_variables=["context", "question"],
            )
        return prompt

    def prepare_context(self, results: list) -> str:

        json_array = [extract_json_str(doc) for doc in results[0]]
        context_array = [extract_context_json(json_str) for json_str in json_array]

        context_data = "\n".join(context_array)

        return context_data

    def get_article_ids(self, results: list) -> list:
        # Extract article IDs from json or metadata.
        articels = [101, 102, 103]
        return articels

    def create_response(self, summary: str, articles: list):
        response = {
            "summary": summary,
            "articles": articles,
        }
        return response

    def generate_summary(self, query: str):

        start_time = datetime.now()
        model = get_llm_model(ModelType.CHAT)
        vectore_store = VectorStore()
        results = vectore_store.get_semantic_data(query, n_results=3)
        context_data = self.prepare_context(results)
        prompt = self.get_prompt_template(TemplateType.BASE)
        final_prompt = prompt.format(context=context_data, question=query)
        summary = model.invoke(final_prompt)
        article_ids = self.get_article_ids(results)
        response = self.create_response(summary.content, article_ids)
        response["metadata"] = {"processing_time": str(datetime.now() - start_time)}
        return response
