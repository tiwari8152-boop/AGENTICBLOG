from src.states.state import BlogState
from langchain_core.messages import HumanMessage
from src.states.state import Blog

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
        
    def translation(self, state:BlogState):
        print("entering in translation node")
        print("checking for current language in translation", state["current_language"])
        title_prompt =      """
                                Translate the following content into {current_language}.
                                -   Maintain the original tone, style and formatting.
                                -   Adapt cultural references and idioms to be appropriate for {current_language}.

                                ORIGINAL CONTENT:
                                {title_content}

                             """    
        translation_prompt = """
                                Translate the following content into {current_language}.
                                -   Maintain the original tone, style and formatting.
                                -   Adapt cultural references and idioms to be appropriate for {current_language}.

                                ORIGINAL CONTENT:
                                {blog_content}

                             """
        blog_content = state["blog"]["content"]
        title_content = state["blog"]["title"]
        current_language = state["current_language"]
        title_msg = [
            HumanMessage(
                title_prompt.format(current_language=current_language,
                                    title_content=title_content)
            )
        ]
        message = [
            HumanMessage(
                translation_prompt.format(current_language=current_language,
                                            blog_content=blog_content)
            )
        ]
        translation_title = self.llm.invoke(title_msg)
        translation_content = self.llm.invoke(message)
        # print("translation done successfully !", translation_content)
        return {"blog": {"title":translation_title.content,
                             "content":translation_content.content
                    }}
        
    def route(self, state:BlogState):
        return {"current_language": state["current_language"]}
    
    def route_decision(self, state:BlogState):
        if state["current_language"]=="hindi":
            print("route decision returning", state["current_language"])
            return "hindi"
        elif state["current_language"]=="french":
            print("route decision returning", state["current_language"])
            return "french"
        else:
            return state["current_language"]
            

