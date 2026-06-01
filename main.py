import asyncio
import logging

from app.business.image_service import ImageService
from app.agent.image_reader_agent import ImageReaderAgent

logger = logging.getLogger(__name__)

async def main():
    logger.info("El programa ha iniciado correctamente.")
    
    image_reader_agent = ImageReaderAgent()
    image_service = ImageService(image_reader_agent)

    await image_service.trigger_image_processing_runner()

    logger.info("El programa ha finalizado correctamente.")

if __name__ == "__main__":
    asyncio.run(main())
