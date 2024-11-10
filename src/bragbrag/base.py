from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
import pathlib
import json
import logging.config
import logging.handlers
import importlib.resources as pkg_resources
import bragbrag.logging_configs

from pydantic import BaseModel
from typing import List, Dict, Optional
import time

from mlc_llm import MLCEngine


def settup_logging():
    """Settup logging from a json config file."""

    # config_file = pathlib.Path("./logging_configs/config.json")
    # with open(config_file) as f_in:
    with pkg_resources.open_text(bragbrag.logging_configs, "config.json") as f_in:
        config = json.load(f_in)

    # Determine the project directory (where the config file is located)
    project_dir = pathlib.Path(__file__).resolve().parent

    # Set the absolute paths for the file handlers
    log_file_path = project_dir / "logs" / "bragbrag.log"
    json_log_file_path = project_dir / "logs" / "bragbrag.log.jsonl"
    config["handlers"]["file"]["filename"] = str(log_file_path)
    config["handlers"]["jsonfile"]["filename"] = str(json_log_file_path)
    # Create log directory if it doesn't exist
    log_file_path.parent.mkdir(parents=True, exist_ok=True)

    logging.config.dictConfig(config)


logger = logging.getLogger("bragbrag")
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://nwtracker.braymoll.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Initialize the MLCEngine (adjust parameters as needed)
engine = MLCEngine(
    model="/home/bkm82/Llama-3.1-8B-Instruct_MLC",  # TODO make this it configurable
    model_lib="/home/bkm82/Llama-3.1-8B-Instruct_MLC/Llama-3.1-8B-Instruct-opencl.so",  # TODO make this configurable
    mode="local",
    device="opencl",
)


# Data model for requests
class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    model: str
    messages: List[Message]


class ChatResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: List[Dict[str, str]]


# Initialize conversation history
conversation_history = [
    {
        "role": "system",
        "content": "This is a conversation history for context. Use prior messages as context, and respond only to the latest user prompt.",
    },
]


# Default route (route to /)
@app.get("/")
async def read_root():
    logger.debug("The root route was requested")
    return {"Message": "see the /docs route for more information"}


@app.post("/v1/chat/completions", response_model=ChatResponse)
async def chat_completions(request: ChatRequest):
    # Add all incoming messages to the conversation history
    for message in request.messages:
        conversation_history.append({"role": message.role, "content": message.content})

    # Generate a response
    assistant_response = ""
    try:
        for response in engine.chat.completions.create(
            messages=conversation_history,
            model=request.model,
            stream=True,
        ):
            for choice in response.choices:
                assistant_response += choice.delta.content

        # Append the assistant's response to the conversation history
        conversation_history.append(
            {"role": "assistant", "content": assistant_response}
        )

    except Exception as e:
        logger.error(f"Error generating response: {e}")
        raise HTTPException(status_code=500, detail="Error generating response")

    # Construct response payload
    return ChatResponse(
        id="unique_id",
        object="chat.completion",
        created=int(time.time()),
        model=request.model,
        choices=[{"role": "assistant", "content": assistant_response}],
    )


@app.get("/v1/models")
async def get_models(authorization: Optional[str] = Header(None)):

    # Define the model response
    response = {
        "object": "list",
        "data": [
            {
                "id": "Llama-3.1-8B-Instruct_MLC",
                "object": "model",
                "created": int(time.time()),
                "owned_by": "Meta",
            }
        ],
    }
    return response


@app.on_event("shutdown")
def shutdown_event():
    engine.terminate()
