import argparse
import json

from client import AutomodClient
from logger import get_logger

import sys
import traceback

logger = get_logger(__name__)

def parse():
    parser = argparse.ArgumentParser(description='Automod is a configurable NLP powered Discord Moderator.', usage='automod [arguments]')

    parser.add_argument(
        '--config',
        help='Path to the config file.',
        type=str,
        default='config/discord_example.json',
        required=False
    )

    return parser.parse_args()

def config(args):
    with open(args.config, encoding='utf-8') as f:
        return json.load(f)

def main():
    logger.info('Initializing Automod...')
    logger.info('Loading config...')
    modconfig = config(parse())

    bot = None
    exit_code = 0

    try:
        logger.info('Initializing Discord Client...')
        bot = AutomodClient(**modconfig)
        logger.info('Starting Discord Client...')
        bot.run()
    except KeyboardInterrupt:
        logger.info('Exiting...')
    except Exception as e:
        logger.error(e)
        if bot:
            bot.close()
        logger.error('An error occured while running the bot. Exiting...')
        traceback.print_exc()
        logger.error(traceback.format_exc())
        exit_code = 1
    finally:
        if bot:
            bot.close()
        sys.exit(exit_code)

if __name__ == '__main__':
    main()
