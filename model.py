from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel, ConfigDict


class BaseEventPayload(BaseModel):
    model_config = ConfigDict(extra="allow")


PayloadT = TypeVar("PayloadT", bound=BaseEventPayload)


class Author(BaseModel):
    name: str
    email: str


class Commit(BaseModel):
    sha: str
    message: str
    author: Author
    url: str
    distinct: bool


class Actor(BaseModel):
    id: int
    login: str
    display_login: str
    gravatar_id: str
    url: str
    avatar_url: str


class Repository(BaseModel):
    id: int
    name: str
    url: str


class Organization(BaseModel):
    id: Optional[int] = None
    login: Optional[str] = None
    gravatar_id: Optional[str] = None
    url: Optional[str] = None
    avatar_url: Optional[str] = None


class CreateEventPayload(BaseEventPayload):
    ref: Optional[str] = None
    ref_type: str
    master_branch: str
    description: Optional[str] = None
    pusher_type: str


class WatchEventPayload(BaseEventPayload):
    action: str


class PushEventPayload(BaseEventPayload):
    repository_id: int
    push_id: int
    size: int
    distinct_size: int
    ref: str
    head: str
    before: str
    commits: List[Commit]


class Event(BaseModel, Generic[PayloadT]):
    id: int
    type: str
    actor: Actor
    repo: Repository
    payload: PayloadT
    public: bool
    created_at: str
    org: Optional[Organization] = None
