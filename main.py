from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel, validator
import tasks

app = FastAPI()

languages = ['English', 'French', 'German', 'Romanian']

class Translation(BaseModel):
  text: str
  base_lang: str
  final_lang: str

  @validator('base_lang', 'final_lang')
  def valid_lang(cls, lang):
    if lang not in languages:
      raise ValueError('Invalid Language')
    return lang

#Index Route: Test if everything is working properly
@app.get("/")

def root():
  return {"message": "Hello World"}


#Translation Route: Take a translation request store in a db and return a tralation id
@app.post('/translate')
def post_translation(t: Translation, backgroud_task: BackgroundTasks):
  t_id = tasks.store_translation(t)

  backgroud_task.add_task(tasks.run_translation, t_id)

  return{'task_id', t_id}


#Results Route: Take a translation id and retur the text
@app.get('/results')
def get_translation(t_id: int ):
  return{'translation': tasks.find_translation(t_id)}