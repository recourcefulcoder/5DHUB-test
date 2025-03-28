from pydantic import BaseModel
from pydantic.networks import AnyUrl


class LinkContent(BaseModel):
    link: AnyUrl
