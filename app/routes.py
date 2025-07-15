from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from .ticTacToe import TicTacToe
from .main import app
import random

router = APIRouter()

@router.get("/api/health")
async def health_check():
    return {"status": "healthy"}

@router.get("/api/example")
async def example_route():
    return {"message": "This is an example route"}

###################################
## Routes for a tic-tac-toe game ##
###################################
# In-memory game instance (resets on server restart)
gameDict = {}

@router.get("/api/tictactoe/start")
async def tictactoe_start(ai_player: str = Query("X", regex="^[XO]$"), opponent_player: str = Query("O", regex="^[XO]$"), starting_player: str = Query("X", regex="^[XO]$"), difficulty: str = Query("medium", regex="^(easy|medium|hard|impossible)$")):
    key = random.randint(1000, 9999)
    # Ensure this key is unique
    while key in gameDict:
        key = random.randint(1000, 9999)
    gameDict.update({key: TicTacToe(ai_player=ai_player, opponent_player=opponent_player, starting_player=starting_player, difficulty=difficulty)})
    if len(gameDict) > 100:
        # Limit the number of games stored in memory
        for key in list(gameDict.keys()):
            value = gameDict[key]
            if value.get_state()["winner"] is not None:
                del gameDict[key]
                break
    return {"key": key, **gameDict[key].get_state()}

@router.get("/api/tictactoe/state")
async def tictactoe_state(key: int = Query(..., ge=1000, le=9999)):
    if key not in gameDict:
        return JSONResponse({"error": "Game not found"}, status_code=404)
    game = gameDict[key]
    return game.get_state()

@router.get("/api/tictactoe/move")
async def tictactoe_move(key: int = Query(..., ge=1000, le=9999), position: int = Query(..., ge=0, le=8)):
    if key not in gameDict:
        return JSONResponse({"error": "Game not found"}, status_code=404)
    game = gameDict[key]
    if game.make_move(position):
        return game.get_state()
    else:
        return JSONResponse({"error": "Invalid move"}, status_code=400)

@router.get("/api/tictactoe/ai-move")
async def tictactoe_ai_move(key: int = Query(..., ge=1000, le=9999)):
    if key not in gameDict:
        return JSONResponse({"error": "Game not found"}, status_code=404)
    game = gameDict[key]
    move = game.ai_move()
    return {"move": move, **game.get_state()}

@router.get("/api/tictactoe/reset")
async def tictactoe_reset(key: int = Query(..., ge=1000, le=9999)):
    if key not in gameDict:
        return JSONResponse({"error": "Game not found"}, status_code=404)
    game = gameDict[key]
    game.reset()
    return game.get_state()

###############################

# Register the router with the FastAPI app
app.include_router(router)