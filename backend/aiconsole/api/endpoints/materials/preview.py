# The AIConsole Project
#
# Copyright 2023 10Clouds
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from datetime import datetime

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from aiconsole.core.assets.agents.agent import AICAgent
from aiconsole.core.assets.materials.content_evaluation_context import (
    ContentEvaluationContext,
)
from aiconsole.core.assets.materials.material import Material
from aiconsole.core.assets.types import AssetLocation
from aiconsole.core.chat.types import Chat
from aiconsole.core.gpt.consts import SPEED_GPT_MODE

router = APIRouter()


def create_user_agent():
    return AICAgent(
        id="user",
        name="You",
        usage="",
        usage_examples=[],
        system="",
        defined_in=AssetLocation.AICONSOLE_CORE,
        override=False,
    )


@router.post("/preview")
async def materials_preview(material: Material):
    content_context = ContentEvaluationContext(
        chat=Chat(
            id="chat",
            name="",
            last_modified=datetime.now(),
            title_edited=False,
            message_groups=[],
        ),
        agent=create_user_agent(),
        gpt_mode=SPEED_GPT_MODE,
        relevant_materials=[],
    )

    rendered_material = await material.render(content_context)

    return JSONResponse(rendered_material.model_dump(exclude_none=True))
