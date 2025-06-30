from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from .ticTacToe import TicTacToe
from .main import app

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
game = TicTacToe()

@router.get("/api/tictactoe/state")
async def tictactoe_state():
    return game.get_state()

@router.get("/api/tictactoe/move")
async def tictactoe_move(position: int = Query(..., ge=0, le=8)):
    if game.make_move(position):
        return game.get_state()
    else:
        return JSONResponse({"error": "Invalid move"}, status_code=400)

@router.get("/api/tictactoe/ai-move")
async def tictactoe_ai_move():
    move = game.ai_move()
    return {"move": move, **game.get_state()}

@router.get("/api/tictactoe/reset")
async def tictactoe_reset():
    game.reset()
    return game.get_state()

###############################

# Register the router with the FastAPI app
app.include_router(router)