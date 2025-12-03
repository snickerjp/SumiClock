import uvicorn
from src.logging_config import setup_logging

logger = setup_logging()

if __name__ == "__main__":
    logger.info("Starting SumiClock API server")
    uvicorn.run("src.api:app", host="0.0.0.0", port=8000, reload=True)