from src.states.state import BlogState

class BlogNode:
    def __init__(self, llm):
        self.llm = llm

    def title_creation(self, state:BlogState):
        if "topic" in state and state["topic"]:
            prompt_template = """You are an
                                expert blog content writer.
                                Use markdown formatting
                                Generate blog title for the topic {topic}.
                                This title should be creative and SEO friendly.
                                """
            system_message = prompt_template.format(topic=state["topic"])
            response = self.llm.invoke(system_message)
            return {"blog":{"title":response.content}}

    def content_creation(self, state:BlogState):
        if "topic" in state and state["topic"]:
            system_prompt = """
                            You are an expert Blog writer.
                            Use markdown formatting.
                            Generate detailed blog content with detailed
                            breakdown for the {topic}
                            """
            system_message = system_prompt.format(topic=state["topic"])
            response = self.llm.invoke(system_message)
            return {"blog": {"title":state["blog"]["title"],
                             "content":response.content
                    }}
