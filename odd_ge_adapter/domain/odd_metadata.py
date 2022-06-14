from typing import Optional, List

import pydantic


class ODDMetadata(pydantic.BaseModel):
    dataset_list: Optional[List[str]] = None
    bucket: Optional[str]
    prefix: Optional[str]
    regex: Optional[str] = None
