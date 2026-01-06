from typing import TypedDict
from pydantic import BaseModel, Field

class Blog(BaseModel):
    """
    This is for maintaining structure for the output
    """
    title:str=Field(description="the title of blog post")
    content:str=Field(description="the main content of the post")

class BlogState(TypedDict):
    """
    This is actual state that will be passed in between nodes in the graph
    """
    topic:str
    blog:Blog
    current_language:str