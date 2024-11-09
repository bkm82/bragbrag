from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pathlib
import json
import logging.config
import logging.handlers
import uvicorn
import importlib.resources as pkg_resources
import bragbrag.logging_configs


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


# Default route (route to /)
@app.get("/")
async def read_root():
    logger.debug("The root route was requested")
    return {"Message": "see the /docs route for more information"}


if __name__ == "__main__":
    settup_logging()
    logger.info("Starting app")
    uvicorn.run(app, host="0.0.0.0", port=8000)
