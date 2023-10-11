from fastapi import FastAPI, HTTPException, status, Response
from models import Whisky  # Certifique-se de importar o modelo de dados Whisky

whiskies = {
    1: {
        "name": "Old Parr",
        "age": 12,
        "type": "Blended Whisk"
    },
    2: {
        "name": "White Horse",
        "age": 4,
        "type": "Scoot Whisk"
    },
    3: {
        "name": "Black Label",
        "age": 12,
        "type": "Scoot Whisk"
    },
    4: {
        "name": "Jamesom",
        "age": 8,
        "type": "Maltado"
    },

}

app = FastAPI()

@app.get('/whiskies')
async def get_whiskies():
    return whiskies

@app.get('/whiskies/{whisky_id}')
async def get_whisky(whisky_id: int):
    try:
        whisky = whiskies[whisky_id]
        whisky.update({"id": whisky_id})
        return whisky
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Whisky not found')

@app.post('/whiskies', status_code=status.HTTP_201_CREATED)
async def post_whisky(whisky: Whisky):
    last_key = sorted(whiskies.keys())[-1]
    next_key = last_key + 1
    whisky.id = next_key
    whiskies[next_key] = whisky
    return whisky

@app.put('/whiskies/{whisky_id}')
async def put_whisky(whisky_id: int, whisky: Whisky):
    if whisky_id in whiskies:
        whiskies[whisky_id] = whisky
        return whisky
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This whisky doesn't exist")

@app.delete('/whiskies/{whisky_id}')
async def delete_whisky(whisky_id: int):
    if whisky_id in whiskies:
        del whiskies[whisky_id]
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This whisky doesn't exist")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host='localhost', port=8000, reload=True)
