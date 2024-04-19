import shutil
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from crossvals.translate.translate import TranslateCrossValidator
from crossvals.healthcare.healthcare import HealthcareCrossval
from crossvals.textprompting.text import TextPromtingCrossValidator
from crossvals.image_aichemy.aichemy import ImageAIchemyCrossVal
from crossvals.sybil.sybil import SybilCrossVal
from crossvals.openkaito.openkaito import OpenkaitoCrossVal
from crossvals.itsai.itsai import ItsaiCrossVal
from crossvals.wombo.wombo import WomboCrossVal
from crossvals.wombo.protocol import ImageGenerationClientInputs
from crossvals.fractal.fractal import FractalCrossVal
from crossvals.audiogen.audiogen import AudioGenCrossVal
from crossvals.llm_defender.llm_defender import LLMDefenderCrossVal
from crossvals.transcription.transcription import TranscriptionCrossVal
from crossvals.hivetrain.hivetrain import HivetrainCrossVal

from fastapi import UploadFile, File, HTTPException, Body
import asyncio
from pydantic import BaseModel
from typing import List, Annotated

app = FastAPI()

# Enable all cross-origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# healthcare_crossval.run_background_thread()

class TranlsateItem(BaseModel):
    text: str
    source_lang: str = "en"
    target_lang: str = "es"
    timeout: int = None
class TextPropmtItem(BaseModel):
    roles: list[str] = ["user", "assistant"]
    messages: list[str] = [
        "What's the weather like today?",
        "The weather is sunny with a high of 25 degrees.",
        "Could you set a reminder for me to take my umbrella tomorrow?",
        "Reminder set for tomorrow to take your umbrella.",
        "Thank you! What time is my first meeting tomorrow?",
        "Your first meeting tomorrow is at 9 AM.",
        "Can you play some music?",
        "Playing your favorite playlist now.",
        "How's the traffic to work?",
        "Traffic is light, it should take about 15 minutes to get to work."
    ]

class ImageItem(BaseModel):
    imageText: str
class SybilItem(BaseModel):
    sources: str
    query: str

class OpenkaitoItem(BaseModel):
    query: str

class ItsaiItem(BaseModel):
    texts: List[str]

class WomboItem(BaseModel):
    watermark: bool
    prompt: str

class FractalItem(BaseModel):
    query: str

class AudiogenItem(BaseModel):
    type: str
    prompt: str

class LLMDefenderItem(BaseModel):
    analyzer: str

class TranscriptionItem(BaseModel):
    type: str
    audio_url: str
    audio_sample: bytes

class HivetrainItem(BaseModel):
    run_id: str
    batch_size: int
    local_gradient: int 

@app.get("/")
def read_root():
    return translate_crossval.run("Hello, how are you?")

@app.post("/translate/")
def tranlsate_item(item: TranlsateItem):
    
    translate_crossval.setLang(item.source_lang, item.target_lang)
    if item.timeout:
        translate_crossval.setTimeout(item.timeout)
    return translate_crossval.run(item.text)

@app.post("/image-aichemy/")
def image_generate(item: ImageItem):
    return imageaichemy_crossval.run(item.imageText)

@app.post("/sybil/")
def sybil_search(item: SybilItem):
    return sybil_crossval.run({'sources': item.sources, 'query': item.query})

@app.post("/openkaito/")
async def openkaito_search(item: OpenkaitoItem):
    return await openkaito_crossval.run(item.query)

@app.post("/itsai/")
async def llm_detection(item: ItsaiItem):
    return await itsai_crossval.run(item.texts)

@app.post("/wombo/")
async def generate(item: WomboItem):
    print(item)
    return await wombo_crossval.run(ImageGenerationClientInputs(prompt=item.prompt, watermark=item.watermark))

@app.post("/fractal")
def fractal_research(item: FractalItem):
    return fractal_crossval.run(item.query)

@app.post("/audiogen")
async def audio_generation(item: AudiogenItem):
    return await audiogen_crossval.run(item.type, item.prompt)

@app.post("/llm-defender")
def llm_defender(item: LLMDefenderItem):
    return llmdefender_crossval.run({"analyzer": item.analyzer})

@app.post("/transcription/")
def transcription(item: TranscriptionItem):
    return transcription_crossval.run({"type": item.type, "audio_url": item.audio_url, "audio_sample": item.audio_sample})

@app.post("/hivetrain/")
def hivetrain(item: HivetrainItem):
    return hivetrain_crossval.run(item)


class ImageUpload(BaseModel):
    file: UploadFile = File(...)

# @app.post("/healthcare/")
# async def analyze_healthcare_image(image: ImageUpload):
#     print(image.file.filename)
#     file_location = f"images/{image.file.filename}"
#     with open(file_location, "wb+") as file_object:
#         file_object.write(await image.file.read())
#     result = healthcare_crossval.run(file_location)
#     return {"result": result}

@app.post("/healthcare/")
async def upload_image(image: UploadFile = File(...)):
    try:
        # Save the file to disk or process it
        with open(f"{image.filename}", "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
            result = healthcare_crossval.run(image.filename)
            # print(result)     
        # You can process the file here, and then return a response
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/text-prompting/")
def text_prompting(item: TextPropmtItem):
    return textpromtingCrossval.run(item.roles, item.messages)

# @app.websocket("/textprompting")
# async def text_prompting(websocket: WebSocket):
#     print("sdf")
#     await websocket.accept()
#     # data = await websocket.receive_text()
#     streamingResponse = textpromtingCrossval.run()
#     while True:
#         print("tread_running...")
#         data = await streamingResponse[0].__anext__()
#         await websocket.send_json({"message": data})
#         print(data)
#         await asyncio.sleep(1)


translate_crossval = TranslateCrossValidator()
healthcare_crossval = HealthcareCrossval(netuid = 31, topk = 1)
textpromtingCrossval = TextPromtingCrossValidator()
imageaichemy_crossval = ImageAIchemyCrossVal()
sybil_crossval = SybilCrossVal()
openkaito_crossval = OpenkaitoCrossVal()
itsai_crossval = ItsaiCrossVal()
wombo_crossval = WomboCrossVal()
fractal_crossval = FractalCrossVal()
audiogen_crossval = AudioGenCrossVal()
llmdefender_crossval = LLMDefenderCrossVal()
transcription_crossval = TranscriptionCrossVal()
hivetrain_crossval = HivetrainCrossVal()