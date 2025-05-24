from itertools import chain
from multiprocessing import Process
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from google.cloud import firestore

from whiteboardlm import UIDPayload
from whiteboardlm import get_logger, get_token, slack_start, discord_start

logger = get_logger(__name__)

slack_process = dict()
discord_process = dict()
db = firestore.Client()


def terminate_process(process, timeout=3):
    if process.is_alive():
        process.terminate()
        process.kill()
        process.join(timeout)
        if process.is_alive():
            logger.error("Failed to kill process")
            raise HTTPException(status_code=500, detail="Failed to kill process")


@asynccontextmanager
async def lifespan(app: FastAPI):
    global slack_process, discord_process

    logger.info('Server Start')
    yield

    for v in chain(slack_process.values(), discord_process.values()):
        terminate_process(v)

    logger.info('Server Stop')


server = FastAPI(lifespan=lifespan)
server.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@server.post('/slack_bot/run')
def slack_run(data: UIDPayload):
    global slack_process

    if data.uid in slack_process:
        raise HTTPException(status_code=400)
    slack_token, app_token = get_token(db, data.uid, 'tokens_slack')

    p = Process(target=slack_start, args=(slack_token, app_token, data.uid))
    slack_process[data.uid] = p
    p.start()

    logger.info(f'Slack Bot Start : {data.uid}')

    return JSONResponse(
        status_code=200,
        content={"message": "Slack bot started successfully"}
    )


@server.post('/slack_bot/stop')
def slack_stop(data: UIDPayload):
    global slack_process

    if data.uid not in slack_process:
        raise HTTPException(status_code=400)
    terminate_process(slack_process[data.uid])
    del slack_process[data.uid]

    logger.info(f'Slack Bot Stop : {data.uid}')

    return JSONResponse(
        status_code=200,
        content={"message": "Slack bot stopped successfully"}
    )


@server.post('/discord_bot/run')
def discord_run(data: UIDPayload):
    global discord_process

    if data.uid in discord_process:
        raise HTTPException(status_code=400)
    discord_token = get_token(db, data.uid, 'tokens_discord')

    p = Process(target=discord_start, args=(discord_token, data.uid))
    discord_process[data.uid] = p
    p.start()

    logger.info(f'Discord Bot Start : {data.uid}')

    return JSONResponse(
        status_code=200,
        content={"message": "Discord bot started successfully"}
    )


@server.post('/discord_bot/stop')
def discord_stop(data: UIDPayload):
    global discord_process

    if data.uid not in discord_process:
        raise HTTPException(status_code=400)
    terminate_process(discord_process[data.uid])
    del discord_process[data.uid]

    logger.info(f'Discord Bot Stop : {data.uid}')

    return JSONResponse(
        status_code=200,
        content={"message": "Discord bot stopped successfully"}
    )


@server.post('/get_token')
def present_token(data: UIDPayload):
    slacks = None
    discords = None
    slack_tokens = get_token(db, data.uid, 'tokens_slack')
    if slack_tokens is not None:
        slacks = {
            'slack': slack_tokens[0][:7] + '*' * (len(slack_tokens[0]) - 7),
            'app': slack_tokens[1][:7] + '*' * (len(slack_tokens[1]) - 7)
        }
    discord_token = get_token(db, data.uid, 'tokens_discord')
    if discord_token is not None:
        discords = discord_token[:7] + '*' * (len(discord_token) - 7)

    return JSONResponse(
        status_code=200,
        content={'message': 'success', 'slacks': slacks, 'discords': discords}
    )
